import torch
import torch.optim as optim
from .schemas_v2 import ProblemSpecV2
from .pinn_v2 import DynamicPINN
from .sympy_bridge_v2 import evaluate_symbolic_bc

# Derlenen V2 C++ çekirdeğini güvenli şekilde yüklüyoruz
try:
    import openphys_core_v2
    CPP_CORE_AVAILABLE = True
except ImportError:
    CPP_CORE_AVAILABLE = False


class OpenPhysSolverV2:
    def __init__(self, spec: ProblemSpecV2):
        self.spec = spec
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DynamicPINN(spec).to(self.device)
        
        # Optimizasyon Stratejisi
        params = self.spec.solver_strategy.parameters if self.spec.solver_strategy else {}
        self.lr = params.get("lr", 1e-3)
        self.adam_epochs = params.get("adam_epochs", 2000)
        self.lbfgs_epochs = params.get("lbfgs_epochs", 500)
        
        self.optimizer_adam = optim.Adam(self.model.parameters(), lr=self.lr)
        self.optimizer_lbfgs = optim.LBFGS(
            self.model.parameters(), 
            max_iter=20, 
            tolerance_grad=1e-5, 
            tolerance_change=1e-9
        )

    def train_step(self, coords_domain, coords_boundary):
        """Tek bir eğitim adımı (Loss hesaplama)"""
        self.optimizer_adam.zero_grad()
        
        # 1. Fiziksel Kayıp (PDE Residual)
        if self.spec.residuals and len(self.spec.residuals) > 0:
            pde_expr = self.spec.residuals[0].symbolic_expression
            loss_pde = self.model.compute_dynamic_loss(coords_domain, pde_expr)
        else:
            loss_pde = torch.tensor(0.0, device=self.device, requires_grad=True)
        
        # 2. Sınır Koşulu Kaybı (Boundary Condition Loss) - Dinamik Sembolik Ayrıştırma
        if self.spec.conditions and len(self.spec.conditions) > 0 and coords_boundary.numel() > 0:
            loss_bc = torch.tensor(0.0, device=self.device, requires_grad=True)
            
            for cond in self.spec.conditions:
                bc_expr = cond.symbolic_expression if cond.symbolic_expression else "0.0"
                u_bnd_true = evaluate_symbolic_bc(bc_expr, coords_boundary)
                
                cond_type = cond.type.lower() if cond.type else "dirichlet"
                
                if cond_type == "dirichlet":
                    u_bnd_pred = self.model(coords_boundary)
                    loss_bc = loss_bc + torch.mean((u_bnd_pred - u_bnd_true) ** 2)
                    
                elif cond_type in ["neumann", "robin"]:
                    # Neumann türevsel sınır koşulu (du/dn = g)
                    coords_bnd_grad = coords_boundary.clone().detach().requires_grad_(True)
                    u_bnd_pred = self.model(coords_bnd_grad)
                    
                    grads = torch.autograd.grad(
                        outputs=u_bnd_pred,
                        inputs=coords_bnd_grad,
                        grad_outputs=torch.ones_like(u_bnd_pred),
                        create_graph=True
                    )[0]
                    
                    # Normal türevi temsil etmek için koordinat gradyanının ilk bileşeni esas alınır
                    du_dx = grads[:, 0:1]
                    loss_bc = loss_bc + torch.mean((du_dx - u_bnd_true) ** 2)
                else:
                    # Varsayılan Dirichlet
                    u_bnd_pred = self.model(coords_boundary)
                    loss_bc = loss_bc + torch.mean((u_bnd_pred - u_bnd_true) ** 2)
        else:
            loss_bc = torch.tensor(0.0, device=self.device, requires_grad=True)
        
        loss_total = loss_pde + loss_bc
        loss_total.backward()
        
        return loss_total

    def solve(self, domain_data, boundary_data):
        desc = getattr(self.spec, "description", "Auto-generated spec")
        print(f"[{desc}] Çözüm başlatılıyor... (Cihaz: {self.device})")
        if CPP_CORE_AVAILABLE:
            print(" -> C++ Çekirdeği (openphys_core_v2) aktif.")
        
        # Verileri cihaza taşı (Tensor)
        coords_domain = torch.tensor(domain_data, dtype=torch.float32, device=self.device)
        coords_boundary = torch.tensor(boundary_data, dtype=torch.float32, device=self.device)

        # Adam Optimizasyonu
        for epoch in range(self.adam_epochs):
            loss = self.train_step(coords_domain, coords_boundary)
            self.optimizer_adam.step()
            
            if epoch % 500 == 0:
                print(f"Adam Epoch {epoch}/{self.adam_epochs} - Loss: {loss.item():.6e}")

        print("Çözüm tamamlandı.")
        return self.model