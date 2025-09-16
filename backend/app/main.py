import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.server:app", host="192.168.18.33", port=8080, reload=True)
