"""
驗證 LLM 生成的 workflow JSON 是否合法
"""

import json
from typing import Tuple

from app.schemas.workflow_schema import WorkflowDefinition, NodeType


class WorkflowValidator:
    def validate(self, raw_json: str) -> Tuple[bool, WorkflowDefinition | None, list[str]]:
        """
        驗證 workflow JSON
        回傳: (是否合法, 解析後的物件, 錯誤列表)
        """
        errors = []

        # 1. 嘗試解析 JSON
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError as e:
            return False, None, [f"Invalid JSON: {str(e)}"]

        # 2. 用 Pydantic 驗證 schema
        try:
            workflow = WorkflowDefinition(**data)
        except Exception as e:
            return False, None, [f"Schema validation failed: {str(e)}"]

        # 3. 語義驗證
        errors.extend(self._validate_structure(workflow))

        if errors:
            return False, workflow, errors

        return True, workflow, []

    def _validate_structure(self, workflow: WorkflowDefinition) -> list[str]:
        """語義層面的驗證"""
        errors = []
        node_ids = {node.id for node in workflow.nodes}

        # 檢查是否有 start 和 end 節點
        node_types = [node.type for node in workflow.nodes]
        if NodeType.START not in node_types:
            errors.append("Workflow must have at least one START node")
        if NodeType.END not in node_types:
            errors.append("Workflow must have at least one END node")

        # 檢查 start 節點只有一個
        start_count = node_types.count(NodeType.START)
        if start_count > 1:
            errors.append(f"Workflow should have exactly 1 START node, found {start_count}")

        # 檢查 edge 引用的 node 是否存在
        for edge in workflow.edges:
            if edge.source not in node_ids:
                errors.append(
                    f"Edge '{edge.id}' references non-existent source node '{edge.source}'"
                )
            if edge.target not in node_ids:
                errors.append(
                    f"Edge '{edge.id}' references non-existent target node '{edge.target}'"
                )

        # 檢查 node ID 唯一性
        if len(node_ids) != len(workflow.nodes):
            errors.append("Duplicate node IDs detected")

        # 檢查 edge ID 唯一性
        edge_ids = [edge.id for edge in workflow.edges]
        if len(set(edge_ids)) != len(edge_ids):
            errors.append("Duplicate edge IDs detected")

        # 檢查 ACTION 節點是否有 action_type
        for node in workflow.nodes:
            if node.type == NodeType.ACTION and not node.action_type:
                errors.append(f"ACTION node '{node.id}' missing action_type")

        # 檢查連通性：start 節點不應有入邊
        start_nodes = [n.id for n in workflow.nodes if n.type == NodeType.START]
        for edge in workflow.edges:
            if edge.target in start_nodes:
                errors.append(f"START node '{edge.target}' should not have incoming edges")

        # 檢查連通性：end 節點不應有出邊
        end_nodes = [n.id for n in workflow.nodes if n.type == NodeType.END]
        for edge in workflow.edges:
            if edge.source in end_nodes:
                errors.append(f"END node '{edge.source}' should not have outgoing edges")

        return errors
