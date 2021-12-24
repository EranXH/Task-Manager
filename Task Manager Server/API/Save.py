from fastapi import APIRouter, Body
import copy

from Methods.TreeBranches import DeletOrAddTreeBraches, AddRelatedUsersIDs, EditExsistingTasksNames
from Methods.Tasks import UpdateOrCreateTask, TaskNameFromID
from Methods.CheckListItems import UpdateOrCreateCheckListItems
from Methods.UpdateInfoChange import MDB_UpdateUsersCheckListIDs
from Methods.UserInformation import TreeBranchesToUsersIDs, UpdateUserTasks
from Methods.UpdateInfoChange import MDB_RemovedTasks

# Creating a new router to the API
router = APIRouter()

# save a task - after editing an exsisitng one or after creating a new one
@router.post('/post/save/after_editing_task/{public_private}')
def Post_AfterEditingTask(public_private: str, body_dict: dict = Body(...)):
    # --- Arrange Importent Values --- #

    # assaining a dict value for butter understanding
    task_dict: dict = body_dict['task']
    # save the task id because when updating the task info the id will be removed from the "task" dict
    task_id: int = task_dict["_id"]
    # get the task name befor the task is update (if it is a new task -> task_previous_name = "")
    task_previous_name: str = TaskNameFromID(public_private, task_id)

    # --- Update A Task --- #
    user_id: str = body_dict["user_id"]
    UpdateOrCreateTask(public_private, user_id, task_dict)

    # --- Delete Tree Branches --- #
    branches_to_delete: list = body_dict['branches to delete']
    if branches_to_delete:
        _ = DeletOrAddTreeBraches("delete", public_private, branches_to_delete)

    # --- Add Tree Branches --- #
    # get the task name after the task was updated
    branches_to_add: list = body_dict['branches to add']

    if branches_to_add:
        _ = DeletOrAddTreeBraches("add", public_private, copy.deepcopy(branches_to_add))
        # getting the "users_ids_by_branche_id" dict -> {branche_id: users_ids_list}
        users_ids_by_branche_id: dict[str, list[str]] = TreeBranchesToUsersIDs(public_private, branches_to_add)
        # add to the related users to the correct branche
        AddRelatedUsersIDs(public_private, users_ids_by_branche_id)

    # --- Update Task Name In The Tree Branches --- #
    task_new_name = task_dict["name"]
    if task_previous_name != "" and task_previous_name != task_new_name:
        _ = EditExsistingTasksNames(public_private, task_previous_name, task_id, task_new_name)

    # --- Add Users to Tree Branches --- #
    users_ids: list = body_dict['relation to add']
    if users_ids:
        UpdateUserTasks(public_private, "add", task_new_name, task_id, users_ids)
        #MDB_AddedAndRemovedTasks(public_private, "add", task_id, users_ids)

    # --- Delete Users from Tree Branches --- #
    users_ids: list = body_dict['relation to delete']
    if users_ids:
        UpdateUserTasks(public_private, "delete", task_new_name, task_id, users_ids)
        MDB_RemovedTasks(public_private, task_id, users_ids, user_id)

    # --- Update Checklist Items --- #
    MDB_UpdateUsersCheckListIDs(public_private, task_id, user_id, "delete")

    check_list_items: dict = body_dict['check list items']
    UpdateOrCreateCheckListItems(public_private, check_list_items)

    return {}


# saving the task after it folds back
# saving only the thing that can be changed - the task (progress) and the check-list items
@router.post('/post/save/for_foldable_task/{public_private}')
def MDB_Post_ForFoldableTask(public_private: str, body_dict: dict = Body(...)) -> dict:
    task_dict = body_dict["task_dict"]
    task_id = task_dict["_id"]

    check_list_items_dict = body_dict["check_list_items_dict"]
    user_id: str = check_list_items_dict["user_id"]

    UpdateOrCreateTask(public_private, user_id, task_dict)

    if body_dict["is_folding"]:
        MDB_UpdateUsersCheckListIDs(public_private, task_id, user_id, "delete")

    UpdateOrCreateCheckListItems(public_private, check_list_items_dict)

    return {}
