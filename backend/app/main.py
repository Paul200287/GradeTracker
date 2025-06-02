from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router

from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware

def cstm_generate_unique_id(route: APIRoute) -> str:
  return f"{route.tags[0]}-{route.name}"

app = FastAPI(title=settings.PROJECT_NAME, 
              openapi_url=f"{settings.API_V1_STR}/openapi.json", 
              generate_unique_id_function=cstm_generate_unique_id)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Adjust as needed for production
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)