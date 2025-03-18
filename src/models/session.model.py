
import datetime
from typing import Annotated
from beanie import Document, Indexed

class Session(Document):
  """
    Collection name: sessions
  """
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: str
  expires_at: Annotated[datetime, Indexed(expire_after_seconds=0)]

  @classmethod
  def __init__(self, session_token, user_id):
    self.session_token = session_token
    self.user_id = user_id
    self.expires_at = datetime.datetime.now()