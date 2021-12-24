from Methods.TreeBranches import UpdateUsersIDs
from Collections import UsersPublicCol, UsersPrivateCol


# for now -> return the list of all exsisting users ids
def GetAllUsersIDs():
    return UsersPublicCol.find().distinct('_id')


# get the private of public user information
def GetUserInformation(public_private: str, user_ID: str) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = UsersPublicCol if public_private == "Public" else UsersPrivateCol

    info = collection.find({"_id": user_ID})

    try:
        return list(info)[0]
    except IndexError:
        return {}


# get all the allowed tasks of a user (for a list of users_ids)
def UsersAllowedTasksIDs(public_private: str, users_ids: list[str]) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = UsersPublicCol if public_private == "Public" else UsersPrivateCol

    users_id_tasks_ids = list(collection.find({"_id": {"$in": users_ids}}, {"_id": 1, "tasks": 1}))

    user_allowed_tasks_ids = {each_user["_id"]: each_user["tasks"] for each_user in users_id_tasks_ids}

    return user_allowed_tasks_ids


# delete or add a task from a given list of users id`s
def UpdateUserTasks(public_private: str, delete_or_add: str, task_name: str, task_id: int, users_ids: list[str]):
    # set the collection, to the private collection or the public collection base on the input
    collection = UsersPublicCol if public_private == "Public" else UsersPrivateCol

    if delete_or_add == "add":
        operator = "$addToSet"
    else:
        operator = "$pull"

    authorized_tasks_ids_by_user_id = {}
    for user_id in users_ids:
        collection.update_many({"_id": user_id}, {operator: {"tasks": task_id}})

        authorized_tasks_ids = list(map(str, collection.find({"_id": user_id}).distinct("tasks")))

        authorized_tasks_ids_by_user_id[user_id] = authorized_tasks_ids

    UpdateUsersIDs(public_private, delete_or_add, task_name, task_id, authorized_tasks_ids_by_user_id)


# from a list of branches get for each branche a litt of users_ids that can see it
def TreeBranchesToUsersIDs(public_private: str, tree_branches: list[dict[str: int, str: str]]) -> dict[str: list[str]]:
    # set the collection, to the private collection or the public collection base on the input
    collection = UsersPublicCol if public_private == "Public" else UsersPrivateCol

    users_ids_by_branche_id: dict[str: list[str]] = {}
    for branch in tree_branches:
        del branch["users"]
        tasks_ids: list[int] = []
        for task_id_or_route in branch.values():
            # if the "task_id_or_route" it is a route
            if isinstance(task_id_or_route, str):
                # get a list from the branche route
                route_ids: list[str] = task_id_or_route.split('/')
                route_ids.remove("root") # removing the only real str from the list
                # turning all string numbers to int numbers and adding to tasks ids list
                tasks_ids = [*tasks_ids, *map(int, route_ids)]
            else:
                tasks_ids.append(task_id_or_route)

        tasks_ids = list(set(tasks_ids))

        elemMatch_eq: list[dict] = [{"tasks": {"$elemMatch": {"$eq": task_id}}} for task_id in tasks_ids]

        if elemMatch_eq:
            users_ids_by_branche_id[branch["_id"]] = collection.find({"$and": elemMatch_eq}).distinct('_id')

    return users_ids_by_branche_id