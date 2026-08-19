import torch
import numpy as np

class EvaluatorV2:
    @staticmethod
    def compute_l2_error(u_pred: torch.Tensor, u_exact: torch.Tensor) -> float:
        """Bağıl (Relative) L2 Hata Normunu hesaplar."""
        error = torch.norm(u_exact - u_pred, 2)
        norm_exact = torch.norm(u_exact, 2)
        
        if norm_exact == 0:
            return torch.norm(u_pred, 2).item()
            
        return (error / norm_exact).item()

    @staticmethod
    def compute_mse_mae(u_pred: torch.Tensor, u_exact: torch.Tensor):
        mse = torch.mean((u_pred - u_exact)**2).item()
        mae = torch.mean(torch.abs(u_pred - u_exact)).item()
        return mse, mae