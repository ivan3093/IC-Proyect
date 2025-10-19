from fastapi import FastAPI


app = FastAPI()



@app.get("/helloWorld")
def hello_world():

    return "Hello Worlds"

@app.get("/gitstats")
def git_stats():

    return "git connected"

@app.post("/helloUser")
def create_user():

    return "Hello new User"  



