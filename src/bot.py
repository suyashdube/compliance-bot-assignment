import openai

from utils.prompt import CustomPromptTemplate
from utils.parser import CustomOutputParser
from utils.fetcher import CustomWebpageFetcher
from utils.constants import FORMAT_INSTRUCTIONS, USER_PROMPT_TEMPLATE, SYSTEM_PROMPT_TEMPLATE

from config.constants import OPEN_AI
from config.config import logger

class ComplianceBot:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=OPEN_AI.get("api_key"),
        )

        self.fetcher = CustomWebpageFetcher()

        self.prompt_template = CustomPromptTemplate(
            system_prompt_template = SYSTEM_PROMPT_TEMPLATE,
            format_instructions = FORMAT_INSTRUCTIONS,
            user_prompt_template = USER_PROMPT_TEMPLATE
        )

        self.output_parser = CustomOutputParser(
            pattern=r'\{.*?\}'
        )

    def run(self, url):
        webpage = self.fetcher.fetch_one(url)
        if not webpage:
            return { "err": "could not fetch web page" }

        prompt = self.prompt_template.generate_prompt(webpage)

        try:
            response = self.client.chat.completions.create(
                messages = prompt,
                model = OPEN_AI.get("model_name"),
            )
        except openai.APIConnectionError as e:
            logger.error({
                "msg": "failed to connect to openai api",
                "err": str(e)
            })
            return { "err": "failed to connect to bot" }
        except openai.RateLimitError as e:
            logger.error({
                "msg": "openai api rate limited exceeded",
                "err": str(e)
            })
            return { "err": "rate limit exceeded" }
        except openai.APIError as e:
            logger.error({
                "msg": "openai api error",
                "err": str(e)
            })
            return { "err": "api error" }

        parsed_response = self.output_parser.parse_llm_output(response)
        if parsed_response == None:
            return { "err": "invalid response" }

        return { "compliance_issues": parsed_response }