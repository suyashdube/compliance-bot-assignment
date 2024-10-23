import json
import re
from typing import List, Union
from openai.types.chat.chat_completion import ChatCompletion

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.config import logger

class CustomOutputParser:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def _get_llm_response(self, llm_output: ChatCompletion) -> Union[str, None]:
        if not llm_output.choices:
            logger.error({
                "msg": "llm output not found",
            })
            return None

        return llm_output.choices[0].message.content

    def _extract_json_blobs(self, text: str) -> Union[List[str], None]:
        json_blobs = re.findall(self.pattern, text)
        if not json_blobs:
            logger.error({
                "msg": "no json blobs found",
            })
            return None

        return json_blobs

    def _parse_json_blobs(self, blobs: List[str]) -> List[dict]:
        parsed_blobs = []
        for blob in blobs:
            _blob = json.loads(blob)
            if _blob != {}:
                parsed_blobs.append(_blob)

        return parsed_blobs

    def parse_llm_output(self, llm_output: ChatCompletion) -> Union[List[dict], None]:
        llm_response = self._get_llm_response(llm_output)
        if not llm_response:
            return None

        stringified_json_blobs = self._extract_json_blobs(llm_response)
        if not stringified_json_blobs:
            return None

        parsed_output = self._parse_json_blobs(stringified_json_blobs)
        return parsed_output