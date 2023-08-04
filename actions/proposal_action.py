import os
import json
import logging
import openai
from typing import Any

default = """I have read through your project description,\
I can help you complete the project. I will be looking forward to hearing from you \
to discuss it further."""


class ProposalAction:
    def __init__(self) -> None:
        open_ai_org_key: str = str(os.environ.get("OPEN_AI_ORG_KEY"))
        open_ai_api_key: str = str(os.environ.get("OPEN_AI_API_KEY"))
        openai.organization = open_ai_org_key
        openai.api_key = open_ai_api_key

    def get_proposal(self, description) -> str:
        hint = str(
            f"""
            I can help you complete your  project stated as follows 
            {description}

            """
        )
        try:
            res: Any = openai.Completion.create(
                model="text-davinci-003",
                prompt=hint,
                max_tokens=200,
                temperature=0.7,
            )
            response_text = res.choices[0].text
            if not response_text.strip() or len(response_text) < 100:
                return default
            return response_text.strip()
        except Exception as e:
            logging.exception("Error creating proposal with OPENAI")
            return hint
        
    def read_bid_cache(self):
        with open("bid_cache.json", "r+") as f:
            try:
                json_file = json.load(f)
            except Exception:
                json_file = {}
        return json_file


    def update_bid_cache(self, link, proposal):
        bid_cache = self.read_bid_cache()
        with open("bid_cache.json", "w+") as f:
            bid_cache.update({link:proposal})
            json.dump(bid_cache, f, indent=4)

    
    def check_proposal_in_cache_for_link(self, link):
       bid_cache = self.read_bid_cache()
       if link in bid_cache:
           return bid_cache["link"]
       return None
