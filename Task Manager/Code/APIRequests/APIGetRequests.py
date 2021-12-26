import requests

# TODO: need to think about it - get requse another prosse or thred

ServerIP = "45.32.144.224:8000"


# get user information given his user_name_hash and password_hash from fastapi
# (RGet - get request from fastapi)
def RGet_Login(user_name, password_hash):
    # requests for user authentication
    url = f"http://{ServerIP}/get/login/{user_name}"
    files = {'password_hash': password_hash}

    # get a response in the form of the user tasks data
    try:
        api_response = requests.get(url, params=files)
        user_info = api_response.json()
    except requests.ConnectionError:
        user_info = {'Error': 'Failed to connect to the server'}

    return user_info


# requests the check-list-items of a spacific task_id from the server
def RGet_CheckListItems(public_or_private: str, task_id: int, user_id: str):
    # requests for user check_list_items
    url = f"http://{ServerIP}/get/task_checklist/{public_or_private}/{task_id}/{user_id}"

    api_response = requests.get(url)

    # analyze the response from the api in the form of the user check_list_items
    task_check_list_items = api_response.json()

    return task_check_list_items


# requests all the leaves of a branche - send a branche ids list
def RGet_TreeBranches(public_or_private, Branches):
    url = f"http://{ServerIP}/get/tree_branches/{public_or_private}"
    files = {'Branches': Branches}

    api_response = requests.get(url, params=files)
    tree_branches = api_response.json()
    return tree_branches


# requests an available task id - when a new task is created
def RGet_AvailableID(public_or_private):
    url = f"http://{ServerIP}/get/available_id/{public_or_private}"

    api_response = requests.get(url)

    available_id = api_response.json()
    return available_id
