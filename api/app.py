import os
import sys

from starlette.responses import Response

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from core.main import authenticate, generate_id
from core.response_handler import response_formatter
from core.schemas import Auth
from fastapi import FastAPI

app = FastAPI(root_path="/api", docs_url="/")


@app.post("/authenticate")
def authenticate(
    auth: Auth,
):
    try:
        authenticated = authenticate(auth.username, auth.password)

        if authenticated:
            return response_formatter(
                200, message="Success", data={"Authenticated": True}
            )
        else:
            return response_formatter(
                401, message="Invalid credentials", data={"Authenticated": False}
            )
    except Exception as e:
        return response_formatter(500, message=str(e), data={})


@app.post("/barcode_id")
def generate_barcode(
    auth: Auth,
):
    try:
        barcode_id = generate_id(auth.username, auth.password)

        return response_formatter(
            200, message="Success", data={"barcode_id": barcode_id}
        )
    except Exception as e:
        return response_formatter(500, message=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)