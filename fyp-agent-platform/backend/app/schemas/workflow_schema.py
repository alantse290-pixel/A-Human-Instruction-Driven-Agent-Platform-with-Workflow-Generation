"""
Workflow JSON Schema 定義
一個 workflow 包含：
- metadata（名稱、描述）
- nodes（節點列表，每個節點代表一個動作或判斷）
- edges（連線，定義節點之間的執行順序）
"""

from __future__ import annotations
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


# ─── 節點類型 ───────────────────────────────────────────────

class NodeType(str, Enum):
    START = "start"
    END = "end"
    ACTION = "action"
    CONDITION = "condition"
    LOOP = "loop"


class ActionType(str, Enum):
    """ACTION 節點支援的具體操作"""

    HTTP_REQUEST = "http_request"
    SEND_EMAIL = "send_email"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    DATA_TRANSFORM = "data_transform"
    LLM_CALL = "llm_call"
    WAIT = "wait"
    LOG = "log"
    CUSTOM = "custom"


# ─── 節點參數 ───────────────────────────────────────────────

class HttpRequestParams(BaseModel):
    method: str = Field(description="HTTP method: GET, POST, PUT, DELETE")
    url: str = Field(description="Request URL")
    headers: Optional[dict] = None
    body: Optional[dict] = None


class SendEmailParams(BaseModel):
    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")


class LLMCallParams(BaseModel):
    prompt: str = Field(description="The prompt to send to LLM")
    model: Optional[str] = Field(default=None, description="Model override")
    temperature: Optional[float] = Field(default=0.7)


class DataTransformParams(BaseModel):
    operation: str = Field(description="e.g., filter, map, reduce, sort")
    expression: str = Field(description="Transform expression or logic")


class LogParams(BaseModel):
    message: str = Field(description="Log message content")
    level: str = Field(default="info", description="Log level: info, warn, error")


class WaitParams(BaseModel):
    duration_seconds: int = Field(description="Wait time in seconds")


class CustomParams(BaseModel):
    description: str = Field(description="Description of custom action")
    code: Optional[str] = Field(default=None, description="Optional code snippet")


# ─── 條件節點 ───────────────────────────────────────────────

class ConditionParams(BaseModel):
    expression: str = Field(description="Boolean expression to evaluate")
    true_branch: str = Field(description="Node ID to go if true")
    false_branch: str = Field(description="Node ID to go if false")


# ─── Loop 節點 ───────────────────────────────────────────────

class LoopParams(BaseModel):
    loop_type: str = Field(description="for_each, while, or count")
    iterable: Optional[str] = Field(default=None, description="Data source to iterate")
    condition: Optional[str] = Field(default=None, description="While loop condition")
    count: Optional[int] = Field(default=None, description="Number of iterations")
    body_node: str = Field(description="First node ID inside loop body")


# ─── 節點定義 ───────────────────────────────────────────────

class WorkflowNode(BaseModel):
    id: str = Field(description="Unique node identifier, e.g. node_1, node_2")
    type: NodeType = Field(description="Node type")
    label: str = Field(description="Human-readable node name")
    description: Optional[str] = Field(default=None, description="What this node does")
    action_type: Optional[ActionType] = Field(default=None, description="Only for ACTION nodes")
    params: Optional[dict] = Field(default=None, description="Node parameters")
    position: Optional[dict] = Field(default=None, description="UI position {x, y}")


# ─── 連線定義 ───────────────────────────────────────────────

class WorkflowEdge(BaseModel):
    id: str = Field(description="Unique edge identifier, e.g. edge_1")
    source: str = Field(description="Source node ID")
    target: str = Field(description="Target node ID")
    label: Optional[str] = Field(default=None, description="Edge label, e.g. 'yes', 'no'")
    condition: Optional[str] = Field(default=None, description="Condition for this path")


# ─── 完整 Workflow ──────────────────────────────────────────

class WorkflowDefinition(BaseModel):
    name: str = Field(description="Workflow name")
    description: str = Field(description="What this workflow does")
    version: str = Field(default="1.0")
    nodes: list[WorkflowNode] = Field(description="All nodes in the workflow")
    edges: list[WorkflowEdge] = Field(description="All connections between nodes")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Daily Report Generator",
                "description": "Fetch data from API, process it, and send email report",
                "version": "1.0",
                "nodes": [
                    {"id": "node_1", "type": "start", "label": "Start"},
                    {
                        "id": "node_2",
                        "type": "action",
                        "label": "Fetch Sales Data",
                        "action_type": "http_request",
                        "params": {"method": "GET", "url": "https://api.example.com/sales"},
                    },
                    {
                        "id": "node_3",
                        "type": "action",
                        "label": "Format Report",
                        "action_type": "data_transform",
                        "params": {"operation": "map", "expression": "format as table"},
                    },
                    {
                        "id": "node_4",
                        "type": "action",
                        "label": "Send Report Email",
                        "action_type": "send_email",
                        "params": {
                            "to": "manager@company.com",
                            "subject": "Daily Sales Report",
                            "body": "{{previous_output}}",
                        },
                    },
                    {"id": "node_5", "type": "end", "label": "End"},
                ],
                "edges": [
                    {"id": "edge_1", "source": "node_1", "target": "node_2"},
                    {"id": "edge_2", "source": "node_2", "target": "node_3"},
                    {"id": "edge_3", "source": "node_3", "target": "node_4"},
                    {"id": "edge_4", "source": "node_4", "target": "node_5"},
                ],
            }
        }
