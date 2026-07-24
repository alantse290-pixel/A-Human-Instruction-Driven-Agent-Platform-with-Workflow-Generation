# workflow 生成邏輯

"""
Workflow 生成服務：串接 LLM + 驗證 + 修復
"""

import json
from app.services.llm_service import LLMService
from app.services.workflow_validator import WorkflowValidator
from app.prompts.workflow_prompts import WORKFLOW_SYSTEM_PROMPT, WORKFLOW_REPAIR_PROMPT
from app.schemas.workflow_schema import WorkflowDefinition


class WorkflowService:
    def __init__(self):
        self.llm = LLMService()
        self.validator = WorkflowValidator()
        self.max_retries = 2

    async def generate(self, user_instruction: str) -> dict:
        """
        主流程：自然語言 → Workflow JSON
        包含驗證和自動修復機制
        """
        # Step 1: 用 LLM 生成初始 JSON
        raw_json = await self.llm.generate_json(
            user_message=user_instruction,
            system_prompt=WORKFLOW_SYSTEM_PROMPT,
        )

        # Step 2: 驗證
        is_valid, workflow, errors = self.validator.validate(raw_json)

        if is_valid:
            return {
                "success": True,
                "workflow": json.loads(raw_json),
                "retries": 0,
            }

        # Step 3: 自動修復（最多重試 max_retries 次）
        for attempt in range(1, self.max_retries + 1):
            repair_prompt = WORKFLOW_REPAIR_PROMPT.format(
                errors="\n".join(f"- {e}" for e in errors),
                json=raw_json,
            )

            raw_json = await self.llm.generate_json(
                user_message=repair_prompt,
                system_prompt="You fix JSON. Return ONLY valid JSON. No explanations.",
            )

            is_valid, workflow, errors = self.validator.validate(raw_json)

            if is_valid:
                return {
                    "success": True,
                    "workflow": json.loads(raw_json),
                    "retries": attempt,
                }

        # Step 4: 修復失敗，回傳錯誤但附帶不完美的 JSON
        return {
            "success": False,
            "workflow": json.loads(raw_json) if self._is_json(raw_json) else None,
            "errors": errors,
            "retries": self.max_retries,
        }

    def _is_json(self, text: str) -> bool:
        try:
            json.loads(text)
            return True
        except (json.JSONDecodeError, TypeError):
            return False