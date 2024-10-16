from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router

# dash 연결을 위한 설정
from fastapi.middleware.wsgi import WSGIMiddleware
from domain.dash.dashapp import create_dash_app

app = FastAPI()

# 로컬에세 개발 하기 위해 CLOA 보안 정책 우회를 위한 설정
origins = "http://127.0.0.1:3000/"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

# Dash with Flask bind.
dash_app = create_dash_app(requests_pathname_prefix="/dash/")
app.mount("/dash", WSGIMiddleware(dash_app.server))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")