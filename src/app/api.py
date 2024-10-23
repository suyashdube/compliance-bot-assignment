from pydantic import BaseModel
from typing import Union
import uvicorn
from http import HTTPStatus
from datetime import datetime
from functools import wraps
from fastapi import FastAPI, Request, BackgroundTasks

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from bot import ComplianceBot
from config.config import logger

app = FastAPI(
    title="Compliance Bot - Sei",
    description="Webpage compliance checker",
    version="0.1",
)


class WebpageURL(BaseModel):
    url: str


def construct_response(f):
    """Construct a JSON response for an endpoint's results."""

    @wraps(f)
    async def wrap(request: Request, *args, **kwargs):
        results = await f(request, *args, **kwargs)

        # Construct response
        response = {
            "message": results["message"],
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }

        # Add data
        if "data" in results:
            response["data"] = results["data"]

        return response

    return wrap


@app.get("/")
@construct_response
def _index(request: Request):
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response


@app.on_event("startup")
async def _init_bot():
    global bot

    bot = ComplianceBot()

@app.post("/inference/")
@construct_response
async def _infer(request: Request, webpage_url: WebpageURL) -> dict:
    """Get inference from the Compliance bot."""

    logger.info({
        "msg": "compliance check request received",
        "event": {
            "data": webpage_url,
        },
    })

    result = bot.run(webpage_url.url)

    if "err" in list(result.keys()):
        response =  {
            "message": HTTPStatus.BAD_REQUEST.phrase,
            "status-code": HTTPStatus.BAD_REQUEST,
            "data": result
        }
    else:
        response = {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": result
        }

    logger.info({
        "msg": "compliance check request completed",
        "event": {
            "data": webpage_url,
            "response": response
        },
    })

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
