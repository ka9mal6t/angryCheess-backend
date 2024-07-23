from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.users.router import router as user_router
from app.recovery.router import router as recovery_router
from app.statistics.router import router as statistic_router
from app.search.router import router as search_router
from app.match_history.router import router as match_history_router

app = FastAPI()


app.include_router(user_router)
app.include_router(statistic_router)
app.include_router(search_router)
app.include_router(recovery_router)
app.include_router(match_history_router)

origins = [
    "http://localhost:3000",
    "https://ka9mal6t.github.io",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Cookie for front end
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)
