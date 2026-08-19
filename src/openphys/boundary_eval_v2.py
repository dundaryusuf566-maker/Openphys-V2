import sympy as sp
import torch
import numpy as np

class BoundaryConditionEvaluator:
    def __init__(self, variables_dict: dict):
        self.local_dict = variables_dict # {'x': sp.Symbol('x'), 'y': sp.Symbol('y')}

    def evaluate_expression(self, expression_str: str, boundary_coords: torch.Tensor) -> torch.Tensor:
        """
        "x**2 + y" gibi string ifadelerini tensör koordinatlarında sayısal hedeflere çevirir.
        """
        # Hızlı sayısal değerlendirme için lambdify kullanıyoruz
        parsed_expr = sp.sympify(expression_str, locals=self.local_dict)
        
        # x ve y sembollerini al
        x_sym = self.local_dict.get('x', sp.Symbol('x'))
        y_sym = self.local_dict.get('y', sp.Symbol('y'))
        
        # SymPy fonksiyonunu hızlı bir NumPy fonksiyonuna çevir
        num_func = sp.lambdify((x_sym, y_sym), parsed_expr, modules=['numpy'])
        
        # Koordinatları NumPy'ye çevirip hesapla
        x_val = boundary_coords[:, 0].detach().cpu().numpy()
        y_val = boundary_coords[:, 1].detach().cpu().numpy()
        
        target_vals = num_func(x_val, y_val)
        
        # Sabit sayılar (örn: expression="0.0") dizi yerine tek sayı dönebilir, bunu düzelt
        if isinstance(target_vals, (int, float)):
            target_vals = np.full(shape=(boundary_coords.shape[0],), fill_value=target_vals)
            
        # Sonucu PyTorch tensörüne çevir
        target_tensor = torch.tensor(target_vals, dtype=torch.float32, device=boundary_coords.device).unsqueeze(1)
        return target_tensor