from fastapi import APIRouter

from icecream import ic

from Collections import InfoChangePublicCol, InfoChangePrivateCol

# Creating a new router to the API
router = APIRouter()


# updates the avalability of a given user to except updates - when logged out no need to send updates
@router.post('/post/{user_id}/{login_logout}')
def MDB_Post_LoginLogout(user_id: str, login_logout: str):
    info_change_dict = {"tasks_values_changed": [], "removed_tasks": [], "added_tasks": [],
                        "tree_branches_values_changed": [], "removed_tree_branches": [], "added_tree_branches": [],
                        "check_list_values_changed": [], "add_check_list_item": [], "removed_check_list_item": []}

    # makes sure that the info_change_dict of the user is empty
    InfoChangePrivateCol.find_one_and_update({"_id": user_id}, {"$set": info_change_dict})
    InfoChangePublicCol.find_one_and_update({"_id": user_id}, {"$set": info_change_dict})

    # using "$addToSet" operator to be sure that a user id is not inserted twice
    if login_logout == "login":
        operator = "$addToSet"
    # using $pull operator to be sure to pull all ocorences of the user id in the "UsersToUpdate" list
    else:
        operator = "$pull"

    # updates that the user is active and ready to except updates
    InfoChangePrivateCol.find_one_and_update({"_id": "UsersToUpdate"}, {operator: {"users": user_id}})
    InfoChangePublicCol.find_one_and_update({"_id": "UsersToUpdate"}, {operator: {"users": user_id}})

    # setting the user`s tasks that except check list updates
    # when login and logout the list of the user_id should be empty
    InfoChangePrivateCol.find_one_and_update({"_id": "UsersToUpdateCheckList"}, {"$set": {user_id: []}})
    InfoChangePublicCol.find_one_and_update({"_id": "UsersToUpdateCheckList"}, {"$set": {user_id: []}})
