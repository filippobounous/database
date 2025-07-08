import os
from dotenv import load_dotenv
import uvicorn

from app.main import app

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
