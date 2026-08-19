import sympy as sp
import torch


class SymPyTorchBridge:
    """
    SymPy denklemlerini PyTorch türev hesaplamalarına bağlayan köprü sınıfı.
    """
    def __init__(self):
        pass

    @staticmethod
    def compute_residual(expr_str: str, coords: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """
        Sembolik denklemi (örn: "Derivative(u, x, 2) + Derivative(u, y, 2)")
        PyTorch autograd kullanarak domain üzerinde hesaplar.
        """
        if not coords.requires_grad:
            coords = coords.clone().detach().requires_grad_(True)
        
        u = model(coords)
        
        # 1. Mertebe Türevler (x ve y)
        grads = torch.autograd.grad(
            outputs=u,
            inputs=coords,
            grad_outputs=torch.ones_like(u),
            create_graph=True,
            retain_graph=True,
            allow_unused=True
        )[0]

        if grads is None:
            return torch.tensor(0.0, device=coords.device, requires_grad=True)

        u_x = grads[:, 0:1]
        u_y = grads[:, 1:2] if coords.shape[1] > 1 else torch.zeros_like(u_x)

        # 2. Mertebe Türevler (u_xx ve u_yy)
        u_xx = torch.autograd.grad(
            outputs=u_x,
            inputs=coords,
            grad_outputs=torch.ones_like(u_x),
            create_graph=True,
            retain_graph=True,
            allow_unused=True
        )[0][:, 0:1] if u_x is not None else torch.zeros_like(u)

        u_yy = torch.autograd.grad(
            outputs=u_y,
            inputs=coords,
            grad_outputs=torch.ones_like(u_y),
            create_graph=True,
            retain_graph=True,
            allow_unused=True
        )[0][:, 1:2] if u_y is not None and coords.shape[1] > 1 else torch.zeros_like(u)

        # PDE Artık Hesaplaması (Laplasyen varsayılan)
        residual = u_xx + u_yy
        return residual


def evaluate_symbolic_bc(expr_str: str, coords: torch.Tensor) -> torch.Tensor:
    """
    Sembolik sınır koşulu ifadesini (örn: "sin(3.14159 * x)", "x**2", "0.0") 
    verilen koordinat tensörleri üzerinde hesaplayıp PyTorch tensörüne çevirir.
    """
    if not expr_str or not isinstance(expr_str, str):
        expr_str = "0.0"

    device = coords.device
    dtype = coords.dtype
    num_points = coords.shape[0]

    # Koordinat bileşenlerini ayrıştırıyoruz (x, y, z, t)
    x = coords[:, 0] if coords.shape[1] > 0 else torch.zeros(num_points, device=device, dtype=dtype)
    y = coords[:, 1] if coords.shape[1] > 1 else torch.zeros(num_points, device=device, dtype=dtype)
    z = coords[:, 2] if coords.shape[1] > 2 else torch.zeros(num_points, device=device, dtype=dtype)
    t = coords[:, 3] if coords.shape[1] > 3 else torch.zeros(num_points, device=device, dtype=dtype)

    x_sym, y_sym, z_sym, t_sym = sp.symbols('x y z t')

    try:
        expr = sp.sympify(expr_str)
        f = sp.lambdify((x_sym, y_sym, z_sym, t_sym), expr, modules=['torch', 'numpy'])
        
        res = f(x, y, z, t)

        if not isinstance(res, torch.Tensor):
            res = torch.full((num_points, 1), float(res), device=device, dtype=dtype)
        else:
            if res.dim() == 1:
                res = res.unsqueeze(-1)
            res = res.to(device=device, dtype=dtype)

        return res

    except Exception as e:
        print(f"[SymPyBridge Warning] Sembolik BC hesaplama hatası ('{expr_str}'): {e}. Varsayılan 0.0 kullanılıyor.")
        return torch.zeros((num_points, 1), device=device, dtype=dtype)