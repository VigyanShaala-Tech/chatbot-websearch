from fastapi import Body, Depends, FastAPI, Request

from app.routers import websearch, files
from app.core.security import get_api_key
from app.core.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

app = FastAPI(title="Glific Websearch & File Analysis Bot")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(websearch.router, tags=["Websearch"], dependencies=[Depends(get_api_key)])
app.include_router(files.router, tags=["File Analysis"], dependencies=[Depends(get_api_key)])


@app.post("/hi", tags=["Hi"], dependencies=[Depends(get_api_key)])
@limiter.limit("500/minute")
async def hi(request: Request, message: str = Body(..., embed=True)):
    return {"reply": "hi"}


@app.get("/health")
async def health():
    return {"status": "ok"}

