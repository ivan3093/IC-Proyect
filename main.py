from fastapi import FastAPI, HTTPException, status
#from fastapi import FastAPI,HTTPException, Depends, status
    #FastAPI is the principal applciation class
    #HTTPException to trigger HTTP errors like 404,401,403,etc
    #Depends for middlewate inyectable dependencies
    #status for legible HTTP status codes
#from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    #HTTPBearer for bearer tokens
    # HTTPAuthorizationCredentials to extract the credentials from the header 
from pydantic import BaseModel
    #pydantic BaseModel for model data validation.
from typing import Optional
    #importing Optional to be able to use None as a datatype
#from jose import JWTError, jwt
    #models for catching JWT errors
from datetime import datetime
#from datetime import datetime, timedelta
    #to be able to add datetimes and timedeltas(time periods)

app = FastAPI(
     title="FastAPI server",
    description="Mock server for testing authentication and user validation",
    version="1.0.0"
)

#security = HTTPBearer()
    # created a security bearer schema.
class HelloResponse(BaseModel):
    message: str
    timestamp: str
    success: bool


@app.get("/helloWorld")
def hello_world():
    return HelloResponse(
        message="Hello World",
        timestamp=datetime.now().isoformat(),
        success=True
    )

@app.post("/helloUser")
def create_user():
    return HelloResponse(
        message="Hello new User",
        timestamp=datetime.now().isoformat(), 
        success=True
    )  

@app.get("/gitstats")
def git_stats():

    return "git connected"

#Error Handling Endpoint tests 0 for error, the rest for success.
@app.get("/user/{user_id}")
def get_user(user_id: str):
    if user_id == "0":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return HelloResponse(
        message=f"Hello user {user_id}",
        timestamp=datetime.now().isoformat(),
        success=True
    )