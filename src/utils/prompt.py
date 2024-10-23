from langchain_core.documents.base import Document
from typing import List

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.constants import GUIDELINES

# Set up a prompt template
class CustomPromptTemplate:
    def __init__(self, system_prompt_template: str, format_instructions: str, user_prompt_template: str):
        self.system_prompt_template = system_prompt_template
        self.format_instructions = format_instructions
        self.user_prompt_template = user_prompt_template

    # generate prompt given a webpage and guidelines(optional, defaults to stripe guidelines at https://docs.stripe.com/treasury/marketing-treasury)
    def generate_prompt(self, webpage: Document, guidelines: str = GUIDELINES) -> List[dict]:
        system_prompt = self.system_prompt_template.format(guidelines=guidelines, format_instructions=self.format_instructions)
        user_prompt = self.user_prompt_template.format(content=webpage.page_content, source=webpage.metadata["source"])
        prompt = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]

        return prompt
