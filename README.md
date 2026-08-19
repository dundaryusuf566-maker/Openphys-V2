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
```
⚠️ Troubleshooting & Virtualization Notes (C++ / Venv Integration)
During C++ core compilation (openphys_core_v2) within a Python virtual environment, common path resolution or binary link issues may arise. Follow these solutions if encountered:

1. ModuleNotFoundError: No module named 'openphys_core_v2'
Cause: The compiled C++ binary (.pyd on Windows or .so on Linux) was generated outside the Python import path or virtual environment module directory.

Fix: Ensure CMake outputs the compiled library directly into src/openphys/ or run editable package installation:

Bash
```bash
pip install -e .
Alternatively, the engine automatically detects if C++ binaries are missing and gracefully falls back to optimized NumPy/PyTorch mesh generators.
```
2. MSVC / Ninja Compiler Mismatch on Windows
Cause: Building C++ extensions inside venv using standard pip may fail if Developer Command Prompt environment variables are not loaded.

Fix: Run VS Build Tools environment setup before building:

DOS
```bash
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
cmake -B build -G Ninja
cmake --build build
```
3. API Quota / Offline Fallback Mode
If no API key is provided or network requests fail, the system activates the internal Dual-Layer Fallback Manager. It processes queries using deterministic rule-based physics parsers and embedded academic lookup matrices without breaking execution.

🚀 Quick Start
Run the full end-to-end pipeline using the demonstration script:

Bash
```bash
# (Optional) Set Alien Intelligence API Key
set ALIEN_API_KEY=your_key_here
```
# Run the execution pipeline
python -m examples.demo_v2
📂 Project Structure
Plaintext
OpenPhys-V2/
├── src/
│   └── openphys/
│       ├── openaire_agent_v2.py # OpenAIRE Graph API RAG & LLM Parser
│       ├── solver_v2.py         # PyTorch PINN Adam/L-BFGS Solver Loop
│       ├── mesh_v2.py           # Dynamic Mesh & Normal Generator
│       ├── pinn_v2.py           # Dynamic MLP Neural Network
│       ├── sympy_bridge_v2.py   # SymPy to PyTorch Autograd Translation
│       ├── visualizer_v2.py    # Matplotlib Contour & ParaView VTK Exporter
│       └── schemas_v2.py       # Pydantic Schemas (ProblemSpecV2)
├── examples/
│   └── demo_v2.py               # End-to-end execution script
├── requirements.txt             # Python dependencies
├── CMakeLists.txt              # C++ Pybind11 build specification
└── README.md
📜 License
Distributed under the MIT License. Written documentation and submission materials are available under CC-BY 4.0.
