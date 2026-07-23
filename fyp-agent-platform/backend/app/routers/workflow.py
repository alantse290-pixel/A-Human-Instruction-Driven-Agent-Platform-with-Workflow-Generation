# workflow API

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import LLMService
import json

router = APIRouter()
llm_service = LLMService()


class GenerateRequest(BaseModel):
    instruction: str

class WorkflowNode(BaseModel):
    id: str
    type: str
    label: str
    config: dict = {}

class WorkflowEdge(BaseModel):
    from_node: str  # 注意: JSON 裡的 key 是 "from"
    to_node: str    # JSON 裡的 key 是 "to"

@router.get("/health")
async def workflow_health():
    return {"status": "workflow router is ready"}

# 生成工作流程的 API 端點,驗證JSON 結構化輸出是否穩定
@router.post("/generate")
async def generate_workflow(request: GenerateRequest):
    result = await llm_service.generate_json(
        user_message=request.instruction,
        system_prompt=WORKFLOW_SYSTEM_PROMPT,
    )

    try:
        workflow = json.loads(result)

        # 基本結構驗證
        assert "nodes" in workflow, "Missing 'nodes'"
        assert "edges" in workflow, "Missing 'edges'"
        assert len(workflow["nodes"]) > 0, "No nodes generated"

        return {
            "success": True,
            "workflow": workflow,
        }
    except (json.JSONDecodeError, AssertionError) as e:
        return {
            "success": False,
            "error": str(e),
            "raw": result,
        }

WORKFLOW_SYSTEM_PROMPT = """You are a workflow generator. Given a user instruction,
generate a workflow as JSON with this exact structure:
{
  "name": "workflow name",
  "description": "brief description of what this workflow does",
  "nodes": [
    {"id": "node_1", "type": "agent_type", "label": "what this node does", "config": {}}
  ],
  "edges": [
    {"from": "node_1", "to": "node_2"}
  ]
}

Rules:
- Each node must have a unique id like "node_1", "node_2", etc.
- edges define the execution order, "from" runs before "to"
- Available agent types: search_agent, filter_agent, download_agent, llm_qa_agent, retrieval_agent

Available agent descriptions:
- search_agent: searches for papers/articles given a query
- filter_agent: filters results by criteria (year, relevance, etc.)
- download_agent: downloads papers/files
- llm_qa_agent: uses LLM to answer questions or summarize
- retrieval_agent: retrieves relevant chunks from a knowledge base

Always return valid JSON. No extra explanation outside the JSON."""

