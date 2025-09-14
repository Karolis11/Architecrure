# python -m uvicorn app:app --reload

import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.clients import router as clients_router
from routers.client_router import router as html_router 

app = FastAPI(title="Demo")
app.include_router(clients_router, prefix="/api")

@app.get("/")
def root():
  return RedirectResponse("/clients")

app.include_router(html_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
