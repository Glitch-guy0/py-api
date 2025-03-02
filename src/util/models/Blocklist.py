from pydantic import BaseModel

from datetime import datetime

class Session(BaseModel):
    token: str
    expiry: datetime


class IP(BaseModel):
    ip: str
    expiry: datetime
