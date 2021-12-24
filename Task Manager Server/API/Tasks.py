from fastapi import APIRouter

from icecream import ic

from Collections import TasksPrivateCol, TasksPublicCol

# Creating a new router to the API
router = APIRouter()


# get a new available task id - when a new task is created a new id is needed
@router.get("/get/available_id/{public_private}")
def MDB_Get_AvailableID(public_private: str) -> int:
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    info = collection.find({"_id": "GET ID"})

    get_id_dict = list(info)[0]

    if get_id_dict["unoccupied_ids"]:
        available_id = get_id_dict["unoccupied_ids"][0]
        _ = collection.find_one_and_update({"_id": "GET ID"}, {"$pull": {"unoccupied_ids": available_id}})

    else:
        available_id = get_id_dict["next_id"]
        _ = collection.find_one_and_update({"_id": "GET ID"}, {"$set": {"next_id": available_id+1}})

    return available_id
