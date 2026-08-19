__version__ = "2.0.0"

# Alt modüllerdeki ana bileşenleri dışarı aktarıyoruz
from .schemas_v2 import ProblemSpecV2, FieldDefV2 as FieldSpecV2, ConditionDefV2 as ConditionSpecV2, ResidualDefV2 as ResidualSpecV2
from .openaire_agent_v2 import OpenAIREAgentV2
from .solver_v2 import OpenPhysSolverV2
from .mesh_v2 import DynamicMesh
from .visualizer_v2 import VisualizerV2

__all__ = [
    "__version__",
    "ProblemSpecV2",
    "FieldSpecV2",
    "ConditionSpecV2",
    "ResidualSpecV2",
    "OpenAIREAgentV2",
    "OpenPhysSolverV2",
    "DynamicMesh",
    "VisualizerV2"
]