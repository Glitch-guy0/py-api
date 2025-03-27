from models.user import Login_Info, Login_Data, User
from lib.auth.validations import Validations
from .crypto import Crypto
from lib.logger import logger

class Account_Manager:

  @staticmethod
  async def create_user(user_data:User)-> None:
    logger.debug(f"user create request: {user_data}")
    logger.info("user create request")
    await User.create_user(user_data)


  @staticmethod
  async def verify_user_login(login_data: Login_Data)-> Login_Info:
    logger.debug(f"user login request for email: {login_data.email}")
    Validations.password_validator(login_data.password)
    user = await User.get_user_by_email(login_data.email)
    Crypto.verify_password(login_data.password, user.password)
    logger.info('user login successful')
    return user