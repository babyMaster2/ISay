from fastapi import FastAPI

from src.app.main import app as backend_app

app = FastAPI()

# 添加子应用程序
app.mount("src", backend_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
