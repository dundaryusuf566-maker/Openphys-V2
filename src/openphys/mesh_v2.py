import numpy as np

class DynamicMesh:
    def __init__(self, dim: int = 2):
        self.dim = dim
        
    def generate_domain_points(self, num_points: int, bounds: list) -> np.ndarray:
        """
        Belirtilen sınırlar (bounds) içerisinde rastgele iç bölge (domain) noktaları üretir.
        bounds = [(x_min, x_max), (y_min, y_max), ...]
        """
        points = []
        for d in range(self.dim):
            min_val, max_val = bounds[d]
            coords = np.random.uniform(min_val, max_val, num_points)
            points.append(coords)
        return np.column_stack(points).astype(np.float32)

    def generate_boundary_points(self, num_points_per_edge: int, bounds: list) -> np.ndarray:
        """
        Geometrinin dış sınırlarında noktalar üretir. 
        Sınır koşullarının (Dirichlet, Neumann) uygulanacağı koordinatlardır.
        """
        # Şimdilik 2D dikdörtgen sınırları için temel implementasyon
        x_min, x_max = bounds[0]
        y_min, y_max = bounds[1]
        
        # Kenarlar
        b_bottom = np.column_stack([np.linspace(x_min, x_max, num_points_per_edge), np.full(num_points_per_edge, y_min)])
        b_top = np.column_stack([np.linspace(x_min, x_max, num_points_per_edge), np.full(num_points_per_edge, y_max)])
        b_left = np.column_stack([np.full(num_points_per_edge, x_min), np.linspace(y_min, y_max, num_points_per_edge)])
        b_right = np.column_stack([np.full(num_points_per_edge, x_max), np.linspace(y_min, y_max, num_points_per_edge)])
        
        return np.vstack([b_bottom, b_top, b_left, b_right]).astype(np.float32)