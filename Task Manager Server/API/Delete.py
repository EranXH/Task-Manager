from fastapi import APIRouter

from Methods.Tasks import DeleteTask, TasksRelatedUsers, ReturnUnusedID
from Methods.CheckListItems import DeleteCheckList
from Methods.TreeBranches import DeleteAllExistingTasksBranches
from Methods.UserInformation import UpdateUserTasks
from Methods.UpdateInfoChange import MDB_RemovedTasks

# Creating a new router to the API
router = APIRouter()

# delete an exsisting task - called by clicking the delete button (in the client)
@router.delete('/delete/task/{public_private}/{task_name}/{task_id}/{user_id}')
def Delete_Task(public_private: str, task_name: str, task_id: int, user_id: str) -> dict:
    # get a dict of the a realation type and a list of users_id
    related_users_ids = TasksRelatedUsers(public_private, [task_id])[task_id]
    # rearanging the dict into a list (after passing it first throuh a set to delete duplicates)
    # to get a list of all of the related uses (no mater what type)
    related_users_ids = list({*related_users_ids["incharge_users"], *related_users_ids["assigned_users"]})
    # updates the users task - deleting the task_id from the list of task_ids that they can see
    UpdateUserTasks(public_private, "delete", task_name, task_id, related_users_ids)

    # updating the online users documents to tell them a spasific task had been deleted
    MDB_RemovedTasks(public_private, task_id, related_users_ids, user_id)

    # deleting the actual task
    DeleteTask(public_private, task_id)
    # return the unused task_id
    ReturnUnusedID(public_private, task_id)

    # deleting the task check_lists_items
    DeleteCheckList(public_private, task_id)

    # deleting all the related branches to the task id
    DeleteAllExistingTasksBranches(public_private, task_id, task_name)

    return {}

