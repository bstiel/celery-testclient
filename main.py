from fastapi import FastAPI
from worker import task1

app = FastAPI()


@app.get("/users")
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.post("/users")
async def create_user(payload: dict):
    async_result = task1.s(payload).delay()
    print(async_result)
    return payload


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
