from pathlib import Path

import fastapi
import uvicorn
from fastapi.responses import FileResponse

app = fastapi.FastAPI()

BASE_DIR = Path(__file__).parent


@app.get("/")
def read_root() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
