from icecream import ic

from Collections import InfoChangePublicCol, InfoChangePrivateCol


def MDB_UpdateUsersCheckListIDs(public_private: str, check_list_id: int, user_id: str, delete_or_add: str):
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    # using "$addToSet" operator to be sure that a user id is not inserted twice
    if delete_or_add == "add":
        operator = "$addToSet"
    # using $pull operator to be sure to pull all ocorences of the user id in the "UsersToUpdate" list
    else:
        operator = "$pull"

    collection.find_one_and_update({"_id": "UsersToUpdateCheckList"}, {operator: {user_id: check_list_id}})


def MDB_UsersIDsForUpdate(collection, document_name, related_users_ids, task_id=0) -> list[str]:
    document_dict = list(collection.find({"_id": document_name}))[0] #"UsersToUpdateCheckList"})

    if document_name == "UsersToUpdateCheckList":
        users_to_update = []
        for user_id in related_users_ids:
            try:
                if task_id in document_dict.get(user_id):
                    users_to_update.append(user_id)
            except TypeError:
                pass

    else:   # if document_name == "UsersToUpdate":
        users_to_update: list[str] = document_dict["users"]
        users_to_update = list(set(related_users_ids).intersection(set(users_to_update)))

    return users_to_update


def MDB_CheckListValuesChanged(public_private: str, old_check_list_dict: dict, check_list_items: dict,
                               related_users_ids: list):
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    task_id = old_check_list_dict["_id"]

    check_list_diff = {}
    for item_id, item_values in check_list_items.items():
        if old_check_list_dict.get(item_id) != item_values:
            check_list_diff[item_id] = item_values

    check_list_diff["_id"] = task_id

    users_to_update = MDB_UsersIDsForUpdate(collection, "UsersToUpdateCheckList", related_users_ids, task_id)
    ic(users_to_update)
    ic(check_list_diff)

    collection.update_many({"_id": {"$in": users_to_update}, "check_list_values_changed": {"$nin": [check_list_diff]}},
                           {"$addToSet": {"check_list_values_changed": check_list_diff}})


def MDB_TasksValuesChanged(public_private: str, old_task_dict: dict, task_dict: dict, user_id: str):
    task_diff_dict = GetDictsDiff(old_task_dict, task_dict)

    if len(task_diff_dict) >= 2:
        # set the collection, to the private collection or the public collection base on the input
        collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

        # get all the related users ids
        related_users_ids = list({*task_dict["incharge_users"], *task_dict["assigned_users"]})
        related_users_ids.remove(user_id)

        task_id = old_task_dict["_id"]
        users_to_update = MDB_UsersIDsForUpdate(collection, "UsersToUpdate", related_users_ids)

        # update all the "tasks values changed" where "_id" is equal to one of the ids in the list
        # and task_dict doesn't already exsist there
        collection.update_many({"_id": {"$in": users_to_update}, "tasks_values_changed": {"$nin": [task_diff_dict]}},
                               {"$addToSet": {"tasks_values_changed": task_diff_dict}})


def MDB_RemovedTasks(public_private: str, task_id: int, related_users_ids: list[str], user_id: str):
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    related_users_ids.remove(user_id)
    users_to_update = MDB_UsersIDsForUpdate(collection, "UsersToUpdate", related_users_ids)

    # update all the "field"s where "_id" is equal to one of the ids in the list
    # and "task_id" doesn't already exsist there
    collection.update_many({"_id": {"$in": users_to_update}, "removed_tasks": {"$nin": [task_id]}},
                           {"$addToSet": {"removed_tasks": task_id}})

def MDB_AddedTasks(public_private: str, task_dict: dict, user_id: str):
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    # get all the related users ids
    related_users_ids = list({*task_dict["incharge_users"], *task_dict["assigned_users"]})
    related_users_ids.remove(user_id)
    users_to_update = MDB_UsersIDsForUpdate(collection, "UsersToUpdate", related_users_ids)
    ic(users_to_update)
    ic(task_dict)
    # update all the "field"s where "_id" is equal to one of the ids in the list
    # and "task_id" doesn't already exsist there
    collection.update_many({"_id": {"$in": users_to_update}, "added_tasks": {"$nin": [task_dict]}},
                           {"$addToSet": {"added_tasks": task_dict}})


def MDB_AddedAndRemovedTreeBranches(public_private: str, delete_or_add: str, task_id: int, users_ids: list[str]):
    # set the collection, to the private collection or the public collection base on the input
    collection = InfoChangePublicCol if public_private == "Public" else InfoChangePrivateCol

    # using "$addToSet" operator to be sure that a user id is not inserted twice
    if delete_or_add == "add":
        field = "added_tasks"   # the field name
    # using $pull operator to be sure to pull all ocorences of the user id in the "Users" list
    else:
        field = "removed_tasks"

    # update all the "field"s where "_id" is equal to one of the ids in the list
    # and "task_id" doesn't already exsist there
    collection.update_many({"_id": {"$in": users_ids}, field: {"$nin": [task_id]}},
                           {"$addToSet": {field: task_id}})


def GetDictsDiff(old_dict: dict, new_dict: dict) -> dict:
    # covernt all list object to tuple because set cannot except list
    old_dict = {key: (tuple(value) if isinstance(value, list) else value)
                for key, value in old_dict.items()}

    new_dict = {key: (tuple(value) if isinstance(value, list) else value)
                for key, value in new_dict.items()}

    diff_dict = {key: value for (key, value) in set(new_dict.items()) - set(old_dict.items())}
    # the new and the old task have the same id, but for the new task dict the _id has been deleted in the previues function
    diff_dict["_id"] = old_dict["_id"]

    return diff_dict
