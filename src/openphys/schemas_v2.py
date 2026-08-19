from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class FieldDefV2(BaseModel):
    name: str
    type: str = Field(..., description="scalar, vector, or tensor")
    dim: int
    function_space: str = "Pointwise"

class ResidualDefV2(BaseModel):
    id: str
    physics_model: str = Field(..., description="Name of the physics, e.g., Navier-Stokes, CustomHeat")
    form_type: str = "strong"
    required_fields: List[str]
    symbolic_expression: Optional[str] = Field(None, description="SymPy compatible equation string. e.g., 'Derivative(u, x, 2) + Derivative(u, y, 2) - f'")
    parameters: Dict[str, Any] = {}

class ConditionDefV2(BaseModel):
    id: str
    type: str = Field(..., description="Dirichlet, Neumann, Robin, etc.")
    region: str
    field_name: str
    symbolic_expression: str 

class SolverDefV2(BaseModel):
    id: str
    category: str
    parameters: Dict[str, Any]
    backend: str = "torch"

class ProblemSpecV2(BaseModel):
    description: str
    fields: List[FieldDefV2]
    residuals: List[ResidualDefV2]
    conditions: List[ConditionDefV2]
    solver_strategy: SolverDefV2
    use_pinn: bool = True
    data_loss_source: Optional[str] = None

# __init__.py ve eski/yeni modül uyumluluğu için takma ad tanımları
FieldSpecV2 = FieldDefV2
ResidualSpecV2 = ResidualDefV2
ConditionSpecV2 = ConditionDefV2
SolverSpecV2 = SolverDefV2