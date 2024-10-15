import datetime
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str
    # 공백 금지
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int    #기존 질문으로 돌아가기 위해
    modify_date: datetime.datetime | None
    voter: list[User] = []

class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int

class AnswerVote(BaseModel):
    answer_id: int