from fastapi import FastAPI


app = FastAPI()



@app.get("/helloWorld")
def hello_world():

    return "Hello Worlds"

@app.post("/helloUser")
def create_user():

    return "Hello new User"  



