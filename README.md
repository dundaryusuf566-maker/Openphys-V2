# OpenPhys V2: Agentic Physics-Informed Neural Network Engine with OpenAIRE Academic RAG

OpenPhys V2 is an agent-driven computational physics framework designed to solve Partial Differential Equations (PDEs) using Physics-Informed Neural Networks (PINNs). It seamlessly connects natural language problem descriptions to symbolic autograd computational graphs, enriched by real-time academic literature queries via the OpenAIRE Graph API.

---

## 🌟 Key Features

* **AI-Driven Spec Generation:** Translates natural language physics queries into structured JSON schemas (`ProblemSpecV2`) using Alien Intelligence MCP / OpenAI LLM APIs.
* **Academic Literature RAG:** Queries the OpenAIRE Graph API to fetch published thermophysical parameters (e.g., thermal conductivity $\alpha$) and dynamically injects them into symbolic equations.
* **Dynamic SymPy Autograd Bridge:** Converts string-based symbolic PDEs into PyTorch `autograd.grad` loss graphs at runtime without hand-coded derivatives.
* **C++ Simulation Core (`openphys_core_v2`):** Optional high-performance C++ backend compiled via CMake and Pybind11 for zero-copy domain mesh generation.
* **Multi-Format Export:** Automatically generates publication-ready 2D heatmaps (`.png`) and ASCII structured grid files (`.vtk`) for ParaView visualization.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python 3.10+
* CMake 3.20+ and C++17 compatible compiler (MSVC / GCC / Clang)

### 2. Virtual Environment Setup
```bash
# Clone the repository
git clone [https://github.com/KULLANICI_ADI/OpenPhys-V2.git](https://github.com/KULLANICI_ADI/OpenPhys-V2.git)
cd OpenPhys-V2

# Create and activate virtual environment
python -m venv venv

# Windows (CMD)
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
