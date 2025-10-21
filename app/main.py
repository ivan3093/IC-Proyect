from fastapi import FastAPI, HTTPException, status, Header, UploadFile, File
    #FastAPI is the principal applciation class
    #HTTPException to trigger HTTP errors like 404,401,403,etc
    #for automatic header extraction
    #status for legible HTTP status codes
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
    #pydantic BaseModel for model data validation.
from src.iolayer.validators import validate_txt_file
from src.service.analyze import analyze_from_upload
from src.schemas.responses import AnalysisSuccess, AnalysisError
from src.utils.errors import (AppBaseError,DecodeError,IOErrorApp,FormatError,UnknownLevel,ValidationError,)
from typing import Optional
    #importing Optional to be able to use None as a datatype
from datetime import datetime, timedelta
    #to be able to add datetimes and timedeltas(time periods)
import time
    #for timestamps
from git import Repo
from git.exc import InvalidGitRepositoryError
import os


app = FastAPI(
     title="FastAPI server",
    description="Mock server for testing authentication and user validation and log analizing",
    version="2.0.4"
)

# Montar carpeta de artefactos estáticos (reportes HTML/PNGs)
STATIC_BASE = Path("static")
REPORTS_BASE = STATIC_BASE / "reports"
REPORTS_BASE.mkdir(parents=True, exist_ok=True)
app.mount("/reports", StaticFiles(directory=str(REPORTS_BASE)), name="reports")

#directories to simulate memory status
valid_tokens = {}
token_expirations = {}

mock_users = [
        {"userId": "usr_12345", "email": "user@example.com", "status": "active"},
        {"userId": "usr_67890", "email": "admin@example.com", "status": "suspended"}
    ]

#Config
VALID_API_KEY = "ic-valid-api-key-123"
VALID_CREDENTIALS = {
    "client_1": "secret_123",
    "client_2": "secret_456"
}
TOKEN_DURATION = 600  # segundos para demo rápida

###MODELS###

#using None as a datatype so the user doesnt have to input both userID and email
class UserValidationRequest(BaseModel):
    userId: Optional[str] = None
    email: Optional[str] = None

#defines the body to generate tokens
class TokenRequest(BaseModel):
    client_id: str
    client_secret: str

#Basic Model for HelloResponse Primarly for testing
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

@app.get("/gitstats")
def git_stats():
    try:
        # Cargar el repositorio en el directorio actual
        repo = Repo(os.path.join(os.path.dirname(os.path.abspath(__file__)),  '..'))
        
        # 1. Verificar si existe el remoto 'origin'
        origin = repo.remotes.origin
        remote_url = origin.url
        
        # 2. Verificar que la URL sea de GitHub (opcional pero lo que buscas)
        is_github = 'github.com' in remote_url

        return {
            "status": "OK",
            "linked_to_origin": True,
            "linked_to_github": is_github,
            "remote_url": remote_url
        }
    
    except InvalidGitRepositoryError:
        return {
            "status": "Error",
            "linked": False,
            "message": "El directorio no es un repositorio Git.",
        }, 500
    except AttributeError:
        # Esto ocurre si el repositorio existe pero NO tiene un remoto llamado 'origin'
        return {
            "status": "OK",
            "linked": False,
            "message": "Es un repositorio Git, pero no tiene configurado el remoto 'origin'."
        }
    
@app.post("/api/v1/auth/token")
async def get_token(request: TokenRequest):
    """
    get a new token (simulates credentals refresh)
    """
    # Verify creds
    if (request.client_id not in VALID_CREDENTIALS or 
        VALID_CREDENTIALS[request.client_id] != request.client_secret):
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid client credentials",
                "code": 401,
                "debug_info": {
                    "available_clients": list(VALID_CREDENTIALS.keys()),
                    "example_request": {
                        "client_id": "client_1", 
                        "client_secret": "secret_123"
                    }
                }
            }
        )
    
    # Generate new token
    token = f"token_{int(time.time())}_{request.client_id}"
    valid_tokens[token] = {
        "client_id": request.client_id,
        "issued_at": datetime.now().isoformat()
    }
    token_expirations[token] = time.time() + TOKEN_DURATION
    
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": TOKEN_DURATION,
        "issued_at": valid_tokens[token]["issued_at"],
        "expires_at": datetime.fromtimestamp(token_expirations[token]).isoformat()
    }

# get a simulated expired token
@app.post("/api/v1/auth/token-expired")
async def get_expired_token():
    """
    Get an expired token (for testing) - VERSIÓN CORREGIDA
    """
    token = f"expired_token_{int(time.time())}"
    
    # GUARDAR el token en valid_tokens (esto faltaba)
    valid_tokens[token] = {
        "client_id": "test_client",
        "issued_at": datetime.now().isoformat()
    }
    # Token que expira en el pasado (10 segundos atrás)
    token_expirations[token] = time.time() - 10
    
    print(f" Token expirado generado: {token}")
    print(f" Guardado en valid_tokens: {token in valid_tokens}")
    print(f" Tiempo de expiración: {token_expirations[token]} (ahora es: {time.time()})")
    
    return {
        "access_token": token,
        "token_type": "Bearer", 
        "expires_in": -10,
        "note": "This token is already expired for testing purposes",
        "debug_info": {
            "token_stored": token in valid_tokens,
            "expiration_set": token in token_expirations
        }
    }

@app.post("/api/v1/debug-test")
async def debug_test(x_api_key: Optional[str] = Header(None)):
    """
    Endpoint for debugging 
    """
    return {
        "server_expected_key": VALID_API_KEY,
        "client_sent_key": x_api_key,
        "keys_match": x_api_key == VALID_API_KEY,
        "key_lengths": {
            "expected": len(VALID_API_KEY),
            "received": len(x_api_key) if x_api_key else 0
        },
        "key_types": {
            "expected": type(VALID_API_KEY).__name__,
            "received": type(x_api_key).__name__ if x_api_key else "None"
        }
    }

@app.post("/api/v1/validateUser")
async def validate_user(
    request: UserValidationRequest,
    x_api_key: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """
    API Key Validation + Token Bearer + Expiration
    """
    print(" validateUser endpoint reached!")

    # Verificar API Key
    if not x_api_key:
        return {
            "error": "Missing API Key",
            "code": 401,
            "debug_info": {
                "issue": "x-api-key header is required",
                "solution": "Add header: x-api-key: your-api-key"
            }
        }

    if x_api_key != VALID_API_KEY:
        return {
            "error": "Invalid API Key", 
            "code": 401,
            "debug_info": {
                "issue": "The provided API key is incorrect",
                "solution": f"Use the valid key: {VALID_API_KEY}",
                "received_key": x_api_key
            }
        }

    # Verify Authorization Header
    if not authorization:
        return {
            "error": "Missing Authorization Header",
            "code": 401,
            "debug_info": {
                "issue": "Authorization header is required",
                "solution": "Add header: Authorization: Bearer <your-token>"
            }
        }

    # Verify that the Authorization header starts with "Bearer "
    if not authorization.startswith("Bearer "):
        return {
            "error": "Invalid Authorization Header",
            "code": 401,
            "debug_info": {
                "issue": "Authorization header must start with 'Bearer '",
                "solution": "Use format: Authorization: Bearer <token>",
                "received_header": authorization
            }
        }

    # Extract the token
    token = authorization.replace("Bearer ", "")

    # Verify the token in valid_tokens
    if token not in valid_tokens:
        return {
            "error": "Invalid Token",
            "code": 401,
            "debug_info": {
                "issue": "The provided token is not valid",
                "solution": "Obtain a valid token from /api/v1/auth/token",
                "received_token": token
            }
        }

    # Verify the token in token_expirations
    if token in token_expirations and token_expirations[token] < time.time():
        return {
            "error": "Token Expired",
            "code": 401,
            "debug_info": {
                "issue": "The provided token has expired",
                "solution": "Tokens expire after 10 minutes. Get a new one from /api/v1/auth/token",
                "token_issued_at": valid_tokens[token]["issued_at"],
                "expired_at": datetime.fromtimestamp(token_expirations[token]).isoformat()
            }
        }

    # basic Request body Validation
    if not request.userId and not request.email:
        return {
            "error": "Either userId or email is required",
            "code": 400,
            "received_data": {
                "userId": request.userId,
                "email": request.email
            }
        }

    # User search in mock_users
    user = None
    for u in mock_users:
        if u["userId"] == request.userId or u["email"] == request.email:
            user = u
            break

    if not user:
        return {
            "error": "User not found",
            "code": 404,
            "searched_for": {
                "userId": request.userId,
                "email": request.email
            }
        }

    # Successfull 200 response
    return {
        "success": True,
        "code": 200,
        "user_found": {
            "userId": user["userId"],
            "email": user["email"],
            "status": user["status"],
            "isValid": user["status"] == "active"
        },
        "debug": {
            "timestamp": datetime.now().isoformat(),
            "version": "with_api_key_bearer_and_expiration_validation",
            "Phase": "Fourth Phase"
        }
    }

@app.post(
    "/analyze-file",
    response_model=AnalysisSuccess,
    responses={
        400: {"model": AnalysisError},
        415: {"model": AnalysisError},
        422: {"model": AnalysisError},
    },
)
def analyze_file(file: UploadFile = File(...)):
    """
    Endpoint principal. Recibe un .txt vía multipart/form-data (campo 'file').
    Orquesta validación -> análisis -> reporte, devolviendo JSON + link a HTML.
    """
    try:
        validate_txt_file(file)  # extensión/MIME/tamaño
        result, metrics, report_path = analyze_from_upload(file)

        # Construir URL pública del reporte HTML (sirviéndose desde /reports)
        rel_report = report_path.relative_to(REPORTS_BASE)
        report_url_html = f"/reports/{rel_report.as_posix()}"

        payload = AnalysisSuccess(
            source_filename=file.filename or "unknown.txt",
            result=result,
            metrics=metrics,
            report_url_html=report_url_html,
        )
        return payload

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=AnalysisError(
                error_type="ValidationError",
                message=str(e),
            ).model_dump()
        )
    except DecodeError as e:
        raise HTTPException(
            status_code=415,
            detail=AnalysisError(
                error_type="DecodeError",
                message=str(e),
            ).model_dump()
        )
    except (FormatError, UnknownLevel) as e:
        # e debe traer contexto de línea fallida y última OK
        raise HTTPException(
            status_code=422,
            detail=AnalysisError(
                error_type=e.__class__.__name__,
                message=str(e),
                failed_line_number=getattr(e, "failed_line_number", None),
                failed_line_content=getattr(e, "failed_line_content", None),
                last_success_line_number=getattr(e, "last_success_line_number", None),
                last_success_line_content=getattr(e, "last_success_line_content", None),
            ).model_dump()
        )
    except IOErrorApp as e:
        raise HTTPException(
            status_code=400,
            detail=AnalysisError(
                error_type="IOError",
                message=str(e),
            ).model_dump()
        )
    except AppBaseError as e:
        # Salvaguarda para errores de app no clasificados
        raise HTTPException(
            status_code=400,
            detail=AnalysisError(
                error_type="AppError",
                message=str(e),
            ).model_dump()
        )
    except Exception as e:
        # Fallback genérico (no exponer stacktrace)
        raise HTTPException(
            status_code=500,
            detail=AnalysisError(
                error_type="InternalServerError",
                message="Unexpected error. Please try again later.",
            ).model_dump()
        )

