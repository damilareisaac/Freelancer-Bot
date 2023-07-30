import os
import openai
from typing import Any

default = """I have read through your project description,\
I can help you complete the project. I will be looking forward to hearing from you \
to discuss it further."""


class ProposalAction:
    def __init__(self, description) -> None:
        self.description = description
        open_ai_org_key: str = str(os.environ.get("OPEN_AI_ORG_KEY"))
        open_ai_api_key: str = str(os.environ.get("OPEN_AI_API_KEY"))
        openai.organization = open_ai_org_key
        openai.api_key = open_ai_api_key

    def get_proposal(self) -> str:
        hint = str(
            f"I can help you complete your  project stated as follows {self.description}"
        )
        try:
            res: Any = openai.Completion.create(
                model="text-davinci-003",
                prompt=hint,
                max_tokens=200,
                temperature=0.6,
            )
            response_text = res.choices[0].text
            if not response_text.strip() or len(response_text) < 100:
                return default
            return response_text
        except Exception as e:
            print(e)
            return hint
