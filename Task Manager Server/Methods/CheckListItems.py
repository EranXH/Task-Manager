from Methods.Tasks import TasksRelatedUsers
from Methods.UpdateInfoChange import MDB_CheckListValuesChanged
from Collections import CheckListItemsPrivateCol, CheckListItemsPublicCol


# updates or create a document that represent the checklist items of a task
def UpdateOrCreateCheckListItems(public_private: str, check_list_items: dict) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    collection = CheckListItemsPublicCol if public_private == "Public" else CheckListItemsPrivateCol

    task_id = check_list_items["_id"]
    del check_list_items["_id"]

    user_id = check_list_items["user_id"]
    del check_list_items["user_id"]

    try:
        old_check_list_dict = list(collection.find({"_id": task_id}))[0]
    except IndexError:
        old_check_list_dict = {}

    # replace the content of a "check-list-items" document by an id (task_id)
    # if the id doesn't exsist insert a new one
    collection.find_one_and_replace({"_id": task_id}, check_list_items, upsert=True)

    # if an exsistign check list was updated, updates all the active related users that opend the checklist
    if old_check_list_dict:
        # get a dict of the "incharge_users" and the "assigned_users" of the task
        related_users_ids = TasksRelatedUsers(public_private, [task_id])[task_id]
        # turn the dict into a list and remove the id of the user how sent the update
        # first turning it to a set in order to deal with duplicates
        related_users_ids = list({*related_users_ids["incharge_users"], *related_users_ids["assigned_users"]})
        related_users_ids.remove(user_id)

        MDB_CheckListValuesChanged(public_private, old_check_list_dict, check_list_items, related_users_ids)

    return {}


# remove a check-list-items document by a given task id
def DeleteCheckList(public_private: str, task_id: int):
    # set the collection, to the private collection or the public collection base on the input
    collection = CheckListItemsPublicCol if public_private == "Public" else CheckListItemsPrivateCol

    collection.find_one_and_delete({'_id': task_id})