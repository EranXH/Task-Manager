from fastapi import APIRouter

from icecream import ic

from Collections import AuthenticationCol, UsersPublicCol, UsersPrivateCol, InfoChangePublicCol
from Methods.Signup import CheckIdentifyingInfoDuplication

# Creating a new router to the API
router = APIRouter()


# signup - for new users
@router.post("/post/sign_up/{email}/{user_name}/{password}")
def MDB_Post_Signup(email: str, user_name: str, password: str) -> dict:
    # verefing the signup and checking for email and user_name duplication
    check = CheckIdentifyingInfoDuplication(email, user_name)["response"]

    # if the response contains nothing it means that the ckeck went well
    if not check:
        AuthenticationCol.insert_one({"_id": user_name,
                                      "password": password,
                                      "email": email,
                                      "user_ID": user_name})

        UsersPublicCol.insert_one({"_id": user_name, "tasks": [],
                                   "assign": [], "incharge": []})

        UsersPrivateCol.insert_one({"_id": user_name, "tasks": []})

        # no need to update the private InfoChange because only the creating user can edit the task
        InfoChangePublicCol.insert_one({"_id": user_name}, {"tasks_values_changed": [], "removed_tasks": [],
                                                            "added_tasks": [], "tree_branches_values_changed": [],
                                                            "removed_tree_branches": [], "added_tree_branches": [],
                                                            "check_list_values_changed": [], "add_check_list_item": [],
                                                            "removed_check_list_item": []})

        return {"response": ""}

    # if the check has any respose
    else:
        return check