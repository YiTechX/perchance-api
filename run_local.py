import uvicorn
import os
import sys

# Ensure root dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Perchance OpenAI V1 API server at http://127.0.0.1:8000")
    print("API Docs: http://127.0.0.1:8000/docs")
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
