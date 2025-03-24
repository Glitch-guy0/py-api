from models.user import Login_Info, Login_Data, User

class Login_Manager:
  @staticmethod
  async def verify_login_data(login_data: Login_Data)-> Login_Info:
    user = await User.get_user_by_email(login_data.email)
    return user