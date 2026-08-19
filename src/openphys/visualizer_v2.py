import numpy as np
import matplotlib.pyplot as plt
import torch


class VisualizerV2:
    def __init__(self, model, spec):
        """
        Eğitilmiş PINN modelini ve problem spesifikasyonunu alır.
        """
        self.model = model
        self.spec = spec
        self.device = next(model.parameters()).device

    def plot_field_2d(self, resolution: int = 100, save_path: str = "solution_result.png"):
        """
        2D uzayda düzenli bir ızgara (grid) oluşturup model tahminlerini hesaplar
        ve Matplotlib ile ısı haritası (.png) olarak kaydeder.
        """
        self.model.eval()

        # [0, 1] x [0, 1] aralığında düzenli ızgara
        x = np.linspace(0, 1, resolution)
        y = np.linspace(0, 1, resolution)
        X, Y = np.meshgrid(x, y)

        coords = np.column_stack([X.ravel(), Y.ravel()])
        coords_tensor = torch.tensor(coords, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            u_pred = self.model(coords_tensor).cpu().numpy().reshape(resolution, resolution)

        plt.figure(figsize=(8, 6))
        contour = plt.contourf(X, Y, u_pred, levels=50, cmap="viridis")
        plt.colorbar(contour, label="Alan Değeri (u)")

        phys_name = self.spec.residuals[0].physics_model if self.spec.residuals else "Fizik Simülasyonu"
        bc_expr = self.spec.conditions[0].symbolic_expression if self.spec.conditions else "0"

        plt.title(f"OpenPhys V2 Çözüm Alanı: {phys_name}\n(Sınır Koşulu: BC = {bc_expr})", fontsize=11)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True, linestyle="--", alpha=0.3)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[VisualizerV2] 2D Isı Haritası başarıyla kaydedildi -> {save_path}")

    def export_to_vtk(self, resolution: int = 50, save_path: str = "solution_result.vtk"):
        """
        ParaView ve VisIt gibi 3D görselleştirme araçlarında açılabilen
        ASCII VTK Structured Grid dosyası üretir.
        """
        self.model.eval()

        x = np.linspace(0, 1, resolution)
        y = np.linspace(0, 1, resolution)
        X, Y = np.meshgrid(x, y)

        coords = np.column_stack([X.ravel(), Y.ravel()])
        coords_tensor = torch.tensor(coords, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            u_pred = self.model(coords_tensor).cpu().numpy().ravel()

        with open(save_path, "w") as f:
            f.write("# vtk DataFile Version 3.0\n")
            f.write("OpenPhys V2 Field Output\n")
            f.write("ASCII\n")
            f.write("DATASET STRUCTURED_GRID\n")
            f.write(f"DIMENSIONS {resolution} {resolution} 1\n")
            f.write(f"POINTS {resolution * resolution} float\n")

            for i in range(coords.shape[0]):
                f.write(f"{coords[i, 0]:.6f} {coords[i, 1]:.6f} 0.000000\n")

            f.write(f"\nPOINT_DATA {resolution * resolution}\n")
            f.write("SCALARS u_field float 1\n")
            f.write("LOOKUP_TABLE default\n")

            for val in u_pred:
                f.write(f"{val:.6f}\n")

        print(f"[VisualizerV2] ParaView VTK dosyası başarıyla kaydedildi -> {save_path}")