from fastapi import APIRouter

from icecream import ic

from Methods.UpdateInfoChange import MDB_UpdateUsersCheckListIDs
from Collections import CheckListItemsPublicCol, CheckListItemsPrivateCol

# Creating a new router to the API
router = APIRouter()


# (MDB - MongoDB | Get - fastapi get function)
# return the tasks check_list_items from MongoDB given the task`s ID and whether it is public or private (Get - fastapi get function)
# operate as both MongoDB and fastapi function
@router.get('/get/task_checklist/{public_private}/{task_id}/{user_id}')
def MDB_Get_TaskCheckListItems(public_private: str, task_id: int, user_id: str) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = CheckListItemsPublicCol if public_private == "Public" else CheckListItemsPrivateCol

    check_list_items = collection.find({"_id": task_id})

    # tries to get the check-list items as a dict from a "task_id" - if except IndexError then nothing was found
    try:
        check_list_items = list(check_list_items)[0]
        # mark this task_id checklist as one that would except updates
        MDB_UpdateUsersCheckListIDs(public_private, task_id, user_id, "add")
        return check_list_items

    except IndexError:
        return {}
