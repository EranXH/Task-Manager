from fastapi import APIRouter

from API.UpdateInfoChange import MDB_Post_LoginLogout
from Methods.Login import UserAuthenticator, ArrangeUserInformation

from icecream import ic

# Creating a new router to the API
router = APIRouter()


# return the "user_info_dict" given a right username and a password hash
# (for now - a full hush sys is yet to be implemented)
# (Get - fastapi get function)
# user_info_dict - {(user_info (dict), public_tasks (dict), private_tasks (dict)}
@router.get('/get/login/{user_name_hash}')
def Get_Login(user_name_hash: str, password_hash: str) -> dict:
    user_ID = UserAuthenticator(user_name_hash, password_hash)

    if user_ID:
        user_info_dict = ArrangeUserInformation(user_ID)
        MDB_Post_LoginLogout(user_ID, "login")
    else:
        user_info_dict = {'Error': 'Incorrect User Name or Password'}

    return user_info_dict

