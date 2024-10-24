import uvicorn

from app.api.facade import app

if __name__ == "__main__":
    uvicorn.run('app.api.facade:app', reload=True)

