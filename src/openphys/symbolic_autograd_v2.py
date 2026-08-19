import sympy as sp
import torch

class SymbolicAutogradEngine:
    def __init__(self, variables: dict):
        self.variables = variables  # {'x': tensor_x, 'y': tensor_y, 'u': tensor_u}

    def evaluate_node(self, node, coords: torch.Tensor, u_pred: torch.Tensor) -> torch.Tensor:
        """
        SymPy ağacındaki her bir düğümü (node) PyTorch operasyonuna çevirir.
        """
        # Eğer düğüm bir sayıysa (örn: 4.0)
        if isinstance(node, sp.Number):
            return torch.full_like(u_pred, float(node))
            
        # Eğer düğüm bağımsız bir değişkense (x, y)
        elif node in self.variables.values():
            var_name = node.name
            if var_name == 'x': return coords[:, 0:1]
            elif var_name == 'y': return coords[:, 1:2]
            
        # Eğer düğüm ağın çıktısıysa (u)
        elif isinstance(node, sp.Function) or str(type(node)) == "<class 'sympy.core.function.AppliedUndef'>":
            return u_pred

        # Toplama işlemi
        elif isinstance(node, sp.Add):
            result = 0
            for arg in node.args:
                result += self.evaluate_node(arg, coords, u_pred)
            return result

        # Çarpma işlemi
        elif isinstance(node, sp.Mul):
            result = 1
            for arg in node.args:
                result *= self.evaluate_node(arg, coords, u_pred)
            return result

        # Türev alma işlemi (Kritik Nokta)
        elif isinstance(node, sp.Derivative):
            expr = node.expr # Nerenin türevi alınacak (örn: u)
            var = node.variables[0] # Neye göre (örn: x)
            order = len(node.variables) # Kaçıncı dereceden
            
            # İç ifadeyi hesapla
            val = self.evaluate_node(expr, coords, u_pred)
            
            for _ in range(order):
                val = torch.autograd.grad(
                    val, coords,
                    grad_outputs=torch.ones_like(val),
                    create_graph=True,
                    retain_graph=True
                )[0]
                # İlgili ekseni (x=0, y=1) seç
                axis = 0 if var.name == 'x' else 1
                val = val[:, axis:axis+1]
            return val
            
        else:
            raise NotImplementedError(f"Bu sembolik düğüm henüz desteklenmiyor: {type(node)}")

    def compute_residual(self, sympy_expr, coords: torch.Tensor, u_pred: torch.Tensor) -> torch.Tensor:
        return self.evaluate_node(sympy_expr, coords, u_pred)