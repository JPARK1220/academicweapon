from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )

exception_handlers = {404: not_found}

app = FastAPI(exception_handlers=exception_handlers, openapi_url="")


@app.get("/")
async def root():
  return {"message": "hello world"}