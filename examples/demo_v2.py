import numpy as np
from src.openphys.openaire_agent_v2 import OpenAIREAgentV2
from src.openphys.solver_v2 import OpenPhysSolverV2
from src.openphys.visualizer_v2 import VisualizerV2

def generate_mock_mesh():
    domain_coords = np.random.rand(2000, 2)
    boundary_coords = np.concatenate([
        np.column_stack([np.random.rand(100), np.zeros(100)]),
        np.column_stack([np.random.rand(100), np.ones(100)]),
        np.column_stack([np.zeros(100), np.random.rand(100)]),
        np.column_stack([np.ones(100), np.random.rand(100)])
    ])
    return domain_coords, boundary_coords

def main():
    print("=== OpenPhys V2 - Academic RAG Physics Engine ===\n")

    agent = OpenAIREAgentV2()

    # Önemli Değişiklik: Sorgunun içine 'aluminum' (Alüminyum) kelimesini ekledik!
    user_query = "Solve 2D heat equation for aluminum with boundary condition u = x**2"
    print(f"Kullanıcı Sorgusu: '{user_query}'")

    spec = agent.enrich_problem(user_query)
    
    print("--- Motor Parametreleri ---")
    print(f"  Fizik Modeli    : {spec.residuals[0].physics_model}")
    print(f"  Sembolik Denklem: {spec.residuals[0].symbolic_expression}")

    domain_data, boundary_data = generate_mock_mesh()

    solver = OpenPhysSolverV2(spec)
    trained_model = solver.solve(domain_data, boundary_data)

    visualizer = VisualizerV2(trained_model, spec)
    visualizer.plot_field_2d(save_path="solution_result.png")
    visualizer.export_to_vtk(save_path="solution_result.vtk")

if __name__ == "__main__":
    main()