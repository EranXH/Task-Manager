from Collections import TreeBranchesPrivateCol, TreeBranchesPublicCol

from icecream import ic


# get all the tree branches that are related to the user
def GetUserTreeBranches(public_private: str, user_id: str, authorized_tasks_ids: list[int]) -> dict:
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    user_tree_branches = {}
    branches = list(collection.find({"users": {"$elemMatch": {"$eq": user_id}}}, {"users": 0}))

    for branche in branches:
        common_tasks_ids = list(set(branche.values()).intersection(set(authorized_tasks_ids)))
        if common_tasks_ids:
            user_tree_branches[branche["_id"]] = common_tasks_ids

    return user_tree_branches


# by a given task id and a task name get all ocuneses of the task in the branches
# SB - Sub Branches (a dict that the keys are branches ids where the task id apear
#                            and the values are the fitted branche leaves
# LR - Location Routes (a list of ids where the task id apeare as a leave
def Get_SB_LR(public_private: str, task_name: str, task_id: int) -> (dict[str, list[int]], list[str]):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    sub_branches_list: list[dict] = list(collection.find({"_id": {"$regex": str(task_id)}}))
    sub_branches_dict: dict[str, list[int]] = {}
    for branche in sub_branches_list:
        branche_id = branche["_id"]
        branche.pop("_id")
        branche.pop("users")
        sub_branches_dict[branche_id] = list(branche.values())

    location_routes = collection.find({task_name: task_id}).distinct("_id")
    return sub_branches_dict, location_routes


# function used for adding or deleting branches
def DeletOrAddTreeBraches(delete_or_add: str, public_private: str, branches_dicts: list[dict]):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    # input ex: (tasks names and id`s are not correct - just an example)
    '''branches_dicts: [{'Task 0': 1000000000, '_id': 'root'},
                        {'Task 0': 1000000000, '_id': 'root/1000000007'}]'''

    # create a dict that represent the info needed to edit each user tree
    all_sub_branches = set()
    for branche_dict in branches_dicts:
        branche_ID = branche_dict["_id"]
        del branche_dict["_id"]

        # if "delete" the remove the task id from the branch, aotherwise, add it
        if delete_or_add == "delete":
            edited_branche = collection.find_one_and_update({"_id": branche_ID}, {"$unset": branche_dict})
            # check if the brache is empty, if it dose, delete the branche
            if len(list(edited_branche)[0]) == 1:
                _ = collection.delete_one({'_id': branche_ID})
        # if "add", append the task to the brache
        else:  # delete_or_add == "add"
            _ = collection.find_one_and_update({"_id": branche_ID}, {"$set": branche_dict}, upsert=True)

        task_id: int = list(branche_dict.values())[0]

        # the complete route of the branche
        complete_route = f"{branche_ID}/{task_id}"

        # gets a list of all the branches id`s (urls) that contains the complete_route in them and turns it to a set object
        if delete_or_add == "delete":
            sub_branches = set(collection.find({"_id": {"$regex": complete_route}}).distinct('_id'))
            all_sub_branches = all_sub_branches.union(sub_branches)

        # when "add" there are no branches containing that route so no need to sherch

    # delete all branches by a list of there id`s
    if delete_or_add == "delete":
        collection.delete_many({'_id': {"$in": list(all_sub_branches)}})


# on every branche that the task apeare, change the task name to the new name
def EditExsistingTasksNames(public_private: str, task_previous_name: str, task_id: int, task_new_name: str):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    # change the name of the task for all the branches where the task apeare
    collection.update_many({task_previous_name: task_id}, {"$rename": {task_previous_name: task_new_name}})


# delete or add all the given tasks realetd users ids to all the task occurrences in the tree
def UpdateUsersIDs(public_private: str, delete_or_add: str, task_name: str, task_id: int,
                   authorized_tasks_ids_by_user_id: dict[str, list[str]]):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    # using "$addToSet" operator to be sure that a user id is not inserted twice
    if delete_or_add == "add":
        operator = "$addToSet"
    # using $pull operator to be sure to pull all ocorences of the user id in the "Users" list
    else:
        operator = "$pull"

    sub_branches_dict, location_routes = Get_SB_LR(public_private, task_name, task_id)
    # repeating the equlety to rpresent the types of each value
    location_routes: list[str] = location_routes
    sub_branches_dict: dict[str, list[int]] = sub_branches_dict

    # lambda function that check if a given list is a sublist of another given list
    is_sublist = lambda sub_list, perent_list: all(sub_list_val in perent_list for sub_list_val in sub_list)

    # loop throuh the items in the authorized_tasks_ids_by_user_id dict
    for user_id, authorized_tasks_ids in authorized_tasks_ids_by_user_id.items():
        related_branches_ids = []
        for route in location_routes:
            route_list = route.split("/")
            route_list.remove("root")
            if is_sublist(route_list, authorized_tasks_ids):
                related_branches_ids.append(route)

        for route, branche_tasks_ids in sub_branches_dict.items():
            if set(branche_tasks_ids).intersection(set(authorized_tasks_ids)):
                route_list = route.split("/")
                route_list.remove("root")
                if is_sublist(route_list, authorized_tasks_ids):
                    related_branches_ids.append(route)

        collection.update_many({"_id": {"$in": related_branches_ids}},
                               {operator: {"users": user_id}})


# when a new branche is added the list of all it`s related users need to be added
def AddRelatedUsersIDs(public_private: str, users_ids_by_branche_id: dict[str, list[str]]):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    for branche_id, users_ids_list in users_ids_by_branche_id.items():
        collection.find_one_and_update({"_id": branche_id},
                                       {"$addToSet": {"users": {"$each": users_ids_list}}})


# finds all the task related branches and do one of two things:
# 1: delete the branche if the id includes the task_id
# 2: remove the task from the branche, if the branche is empty, delete the branche too
def DeleteAllExistingTasksBranches(public_private: str, task_id: int, task_name: str):
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    sub_branches_dict, location_routes = Get_SB_LR(public_private, task_name, task_id)
    # repeating the equlety to rpresent the types of each value
    location_routes: list[str] = location_routes
    sub_branches_dict: dict[str, list[int]] = sub_branches_dict

    collection.delete_many({'_id': {"$in": list(sub_branches_dict.keys())}})

    for branche_id in location_routes:
        edited_branche = collection.find_one_and_update({"_id": branche_id}, {"$unset": {task_name: task_id}})
        if len(list(edited_branche)[0]) == 2:
            collection.delete_one({'_id': branche_id})
