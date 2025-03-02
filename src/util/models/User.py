from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class Session(BaseModel):
    token: str
    expiry: datetime
    ip: str

class OAuth(BaseModel):
    token: str
    expiry: datetime



class User(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    oauth: OAuth
    session: Session


