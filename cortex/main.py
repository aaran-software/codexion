from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from docs.bin.routes import router as docs_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Prefiq Backend")

# Attach docs routes
app.include_router(docs_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "running"}

# Serve favicon from cortex/assets/images/
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    icon_path = Path(__file__).parent / "assets" / "images" / "favicon.svg"
    return FileResponse(icon_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=False)
