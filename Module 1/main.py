from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return 'hello world'

@app.get("/about")
def about():
    return 'Hello from about page..'