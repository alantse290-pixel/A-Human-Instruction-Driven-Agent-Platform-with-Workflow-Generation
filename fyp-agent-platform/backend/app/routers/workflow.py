# workflow API

from fastapi import APIRouter
from pydantic import BaseModel, Field
from ..services.llm_service import LLMService
from ..services.workflow_service import WorkflowService
import json

#router = APIRouter()
router = APIRouter(prefix="/api/workflow", tags=["workflow"])
#llm_service = LLMService()
workflow_service = WorkflowService()


class GenerateRequest(BaseModel):
    instruction: str = Field(
        description="Natural language instruction describing the workflow",
        examples=["Send a welcome email when a new user signs up"],
    )
class GenerateResponse(BaseModel):
    success: bool
    workflow: dict | None = None
    errors: list[str] | None = None
    retries: int = 0

class ValidateRequest(BaseModel):
    workflow: dict


class ValidateResponse(BaseModel):
    valid: bool
    errors: list[str] = []

class WorkflowNode(BaseModel):
    id: str
    type: str
    label: str
    config: dict = {}

class WorkflowEdge(BaseModel):
    from_node: str  # 注意: JSON 裡的 key 是 "from"
    to_node: str    # JSON 裡的 key 是 "to"

@router.post("/generate", response_model=GenerateResponse)
async def generate_workflow(request: GenerateRequest):
    """從自然語言指令生成 workflow JSON"""
    result = await workflow_service.generate(request.instruction)
    return GenerateResponse(**result)


@router.post("/validate", response_model=ValidateResponse)
async def validate_workflow(request: ValidateRequest):
    """驗證一個 workflow JSON 是否合法"""
    from ..services.workflow_validator import WorkflowValidator
    import json

    validator = WorkflowValidator()
    raw_json = json.dumps(request.workflow)
    is_valid, _, errors = validator.validate(raw_json)

    return ValidateResponse(valid=is_valid, errors=errors)