from models.user import Login_Info, Login_Data, User
from lib.auth.validations import Validations
from .crypto import Crypto

class Login_Manager:
  @staticmethod
  async def verify_login_data(login_data: Login_Data)-> Login_Info:
    Validations.password_validator(login_data.password)
    user = await User.get_user_by_email(login_data.email)
    Crypto.verify_password(login_data.password, user.password)
    return user