import uvicorn
from fastapi import FastAPI

from src.api.config_api import isay_route

app = FastAPI(title="isay")

app.include_router(
    isay_route,
    prefix="/api/isay",
    tags=["isay"],
)


@app.get("/health/check", summary="健康检查")
def health_check():
    """
    监控检查
    """
    return {"msg": "I'm very good"}


async def main():
    config = uvicorn.Config("main:app", port=3000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())






