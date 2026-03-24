from fastapi import FastAPI

app = FastAPI(title="NAVI Agent API")

@app.get("/")
def read_root():
    return {"status": "NAVI Agent is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
