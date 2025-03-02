from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

class IP(BaseModel):
  ip: str
  count: int = 0
  expiry: datetime = datetime.now(timezone.utc) + timedelta(days=1)