import numpy

import requests
import pandas as pd
from icecream import ic


ServerIP = "45.32.144.224:8000"

# (post -> create | put -> update)


# Update a private or public check list items by a given task id (RPost - post request from fastapi)
# Update a private or public task by it`s id (RPost - post request from fastapi)
# Send one requset for both
def RPost_ForFoldableTask(public_or_private: str, is_folding: bool, task_dict: dict, check_list_items_dict: dict,
                          user_id: str):
    # when terning the code executable strange behaver accores
    # bool turns to numpy.bool_ and int turns into numpy.int64
    new_vla = []
    for val in task_dict.values():
        if type(val) == numpy.bool_:
            new_vla.append(bool(val))
        elif type(val) == numpy.int64:
            new_vla.append(int(val))
        else:
            new_vla.append(val)

    task_dict = dict(zip(task_dict.keys(), new_vla))

    check_list_items_dict["user_id"] = user_id

    body_dict = {"task_dict": task_dict, "check_list_items_dict": check_list_items_dict, "is_folding": is_folding}

    url = f"http://{ServerIP}/post/save/for_foldable_task/{public_or_private}"

    api_response = requests.post(url, json=body_dict)

    # analyze the response from the api in the form of the user check_list_items
    api_json = api_response.json()


# sending the updated (or new) task after editing to the server
def RPost_AfterEditingTask(public_or_private, body_dict):
    url = f"http://{ServerIP}/post/save/after_editing_task/{public_or_private}"

    api_response = requests.post(url, json=body_dict)

    api_json = api_response.json()


# sending the new user, signing up details
def RPost_Signup(email: str, user_name: str, password: str):
    url = f"http://{ServerIP}/post/sign_up/{email}/{user_name}/{password}"

    try:
        api_response = requests.post(url)
        response = api_response.json()

    except requests.ConnectionError:
        response = {'response': 'Failed to connect to the server'}

    return response


# updating the server that the user has logged out
def RPost_Logout(user_id: str):
    url = f"http://{ServerIP}/post/{user_id}/logout"

    try:
        api_response = requests.post(url)

    except requests.ConnectionError:
        pass
