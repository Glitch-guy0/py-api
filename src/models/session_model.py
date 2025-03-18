
import datetime
from typing import Annotated
from beanie import Document, Indexed

class Session(Document):
  """
    Collection name: sessions
  """
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: str
  created_at: Annotated[datetime.datetime, Indexed(expireAfterSeconds=60*60*24)]

  @classmethod
  def __init__(self, session_token, user_id):
    self.session_token = session_token
    self.user_id = user_id
    self.created_at = datetime.datetime.now()