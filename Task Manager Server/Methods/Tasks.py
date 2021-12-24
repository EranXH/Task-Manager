from Collections import TasksPublicCol, TasksPrivateCol
from Methods.UpdateInfoChange import MDB_TasksValuesChanged, MDB_AddedTasks


# return the tasks by a given list of IDs (MDB - MongoDB | Get - fastapi get function)
def TasksByIDsList(public_private: str, TasksIDs: list[int]) -> list:
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    info = collection.find({"_id": {"$in": TasksIDs}})

    return list(info)


# create or update a task in the datebass by a given task_dict and a sending user_id
def UpdateOrCreateTask(public_private: str, user_id: str, task_dict: dict):
    task_ID = task_dict["_id"]
    del task_dict["_id"]

    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    # getting the task dict before change
    # removing those two fields because they are not relevent for the TasksValuesChanged function
    # doing try except to check if the newly entered values are new task values or not
    try:
        old_task_dict = list(collection.find({"_id": task_ID}))[0]

    except IndexError:
        old_task_dict = {}

    collection.find_one_and_update({"_id": task_ID}, {"$set": task_dict}, upsert=True)

    # if an old task was found - the task is being updated
    # which means that all active related users should get an update
    if old_task_dict:
        MDB_TasksValuesChanged(public_private, old_task_dict, task_dict, user_id)
    # atherwize add a new task for all active users that are related to the new task
    else:
        task_dict["_id"] = task_ID
        MDB_AddedTasks(public_private, task_dict, user_id)


# get all the related users ids of a task by a given task id (this function gets a list of tasks_ids)
def TasksRelatedUsers(public_private: str, ids_list: list[int]) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    tasks = list(collection.find({"_id": {"$in": ids_list}}, {"_id": 1, "incharge_users": 1, "assigned_users": 1}))

    return {task["_id"]: dict(list(task.items())[1:]) for task in tasks}


# gets a task name from its id
def TaskNameFromID(public_private: str, task_id: int) -> str:
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    task_name = collection.find({"_id": task_id}).distinct("name")
    if task_name:
        return task_name[0]

    else:
        return ""


# get all the different types from a list of tasks ids
def TypesListByTaskIDs(public_private: str, tasks_ids: list[int]) -> list[str]:
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    types_list = collection.find({"_id": {"$in": tasks_ids}}).distinct('types')

    return types_list


# delete a task by its id
def DeleteTask(public_private: str, task_id: int):
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    collection.find_one_and_delete({'_id': task_id})


# return to the database an unused task id - when a task is removed or not used
def ReturnUnusedID(public_private: str, ID: int):
    # set the collection, to the private collection or the public collection base on the input
    collection = TasksPublicCol if public_private == "Public" else TasksPrivateCol

    next_id: int = collection.find({"_id": "GET ID"}).distinct("next_id")[0]

    if ID == next_id - 1:
        collection.find_one_and_update({"_id": "GET ID"}, {"$set": {"next_id": ID}})
    else:
        collection.find_one_and_update({"_id": "GET ID"}, {"$addToSet": {"unoccupied_ids": ID}})