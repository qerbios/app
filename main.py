from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import redis

r = redis.Redis(host="redis", port=6379, db=0)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/error")
def error():
    raise ValueError("Test error")

@app.get("/cache/{key}")
def get_from_cache(key: str):
    value = r.get(key)
    if value:
        return {"key": key, "value": value.decode("utf-8")}
    return {"error": "Key not found"}

@app.post("/cache/{key}/{value}")
def set_to_cache(key: str, value: str):
    r.set(key, value)
    return {"status": "saved", "key": key, "value": value}
