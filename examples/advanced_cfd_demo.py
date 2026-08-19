import torch
from src.openphys.openaire_agent_v2 import OpenAIREAgentV2
from src.openphys.solver_v2 import OpenPhysSolverV2
from src.openphys.mesh_v2 import DynamicMesh
from src.openphys.visualizer_v2 import VisualizerV2

def main():
    print("=== OpenPhys V2: Sembolik ve Dinamik PINN Motoru ===")
    
    # 1. LLM / Ajan Entegrasyonu
    # Not: Gerçek LLM entegrasyonu için OpenAIREAgentV2 içine API key girilmeli.
    agent = OpenAIREAgentV2(llm_api_key="YOUR_API_KEY")
    
    # Çoklu denklem gerektiren bir akışkan/ısı problemi
    query = "Solve the 2D steady-state Burgers' equation for fluid convection with a viscosity of 0.01. The domain is x in [-1, 1], y in [-1, 1]."
    print(f"\nKullanıcı Sorgusu: {query}")
    
    # Ajan, sorguyu SymPy denklemlerine çevirir (ProblemSpecV2)
    spec = agent.enrich_problem(query)
    print(f"\nAjanın Çıkardığı Denklem: {spec.residuals[0].symbolic_expression}")
    
    # 2. Veri/Ağ (Mesh) Üretimi
    mesh_gen = DynamicMesh(dim=2)
    domain_pts = mesh_gen.generate_domain_points(2000, bounds=[(-1.0, 1.0), (-1.0, 1.0)])
    boundary_pts = mesh_gen.generate_boundary_points(100, bounds=[(-1.0, 1.0), (-1.0, 1.0)])
    
    # 3. Dinamik Çözücü
    solver = OpenPhysSolverV2(spec)
    
    # Eğitimi başlat
    trained_model = solver.solve(domain_pts, boundary_pts)
    
    # 4. Sonuçları Görselleştir
    with torch.no_grad():
        test_pts = torch.tensor(domain_pts, dtype=torch.float32, device=solver.device)
        u_pred = trained_model(test_pts).cpu().numpy()
        
    VisualizerV2.plot_2d_solution(domain_pts, u_pred, title="Burgers' Equation PINN Solution")

if __name__ == "__main__":
    main()