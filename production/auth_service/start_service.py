import uvicorn

if __name__ == "__main__":
    uvicorn.run("auth_service.main:app", host="0.0.0.0", port=8000, workers=4)
