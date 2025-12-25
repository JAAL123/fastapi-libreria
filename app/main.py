from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Libreria",
    description="API para gestionar una libreria",
    version="0.0.1",    
)

@app.get("/")
def read_root():
    return {"message": "API arriba"}

    