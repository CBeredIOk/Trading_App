
from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import Field, BaseModel

app = FastAPI(
    title='Trading App'
)

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "user", "name": "Alice"},
    {"id": 3, "role": "moderator", "name": "John"},
    {"id": 4, "role": "user", "name": "Sarah"},
    {"id": 5, "role": "admin", "name": "David"},
    {"id": 6, "role": "user", "name": "Emily"},
    {"id": 7, "role": "moderator", "name": "Michael"},
    {"id": 8, "role": "admin", "name": "Olivia"},
    {"id": 9, "role": "user", "name": "Daniel"},
    {"id": 10, "role": "user", "name": "Sophia", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]}
]

trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in users if user.get('id') == user_id]


@app.post('/trades')
def add_trades(trades_from_user: List[Trade]):
    trades.extend(trades_from_user)
    return {'status': 200, 'data': trades}
