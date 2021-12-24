from fastapi import APIRouter

from icecream import ic

from Collections import InfoChangePublicCol, InfoChangePrivateCol

# Creating a new router to the API
router = APIRouter()


# Return updates for an online user, called by a thread (from the clinet) that listen to updateds
@router.get('/get/user_info_change/{public_private}/{user_id}')
def MDB_Get_UserInfoChange(public_private: str, user_id: str) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    user_info_change: dict = list(collection.find({"_id": user_id}, {"_id": 0}))[0]

    if list(user_info_change.values()).count([]) == len(user_info_change):
        return {}

    else:
        collection.find_one_and_update({"_id": user_id},
                                       {"$set": {"tasks_values_changed": [], "removed_tasks": [],  "added_tasks": [],
                                                 "tree_branches_values_changed": [], "removed_tree_branches": [],
                                                 "added_tree_branches": [], "check_list_values_changed": [],
                                                 "add_check_list_item": [], "removed_check_list_item": []}})

        user_info_change = {key: (list(value) if isinstance(value, tuple) else value)
                                    for key, value in user_info_change.items()}
        ic(user_info_change)
        return user_info_change