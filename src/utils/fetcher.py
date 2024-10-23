from typing import Union

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents.base import Document

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.config import logger

class CustomWebpageFetcher:
    def __init__(self):
        self.transformer = Html2TextTransformer()

    def fetch_one(self, url: str) -> Union[Document, None]:
        loader = AsyncHtmlLoader([url])
        try:
            _docs = loader.load()
        except Exception as e:
            logger.error({
                "msg": "error fetching web page",
                "err": str(e)
            })
            return None

        if not _docs:
            logger.error({
                "msg": "empty web page",
                "url": url
            })
            return None

        doc = self.transformer.transform_documents(_docs)[0]
        return doc