from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request

from db import Base, add_request_data, engine, get_user_request
from gemini import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield 

app = FastAPI(lifespan=lifespan)

@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_adress = request.client.host
    user_request = get_user_request(ip_adress=user_ip_adress)
    return user_request


@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True),
):
    user_ip_adress = request.client.host

    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_adress=user_ip_adress,
        prompt=prompt,
        response=answer,
    )
    return {"answer": answer}
    
