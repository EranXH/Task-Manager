import requests
import pandas as pd
from icecream import ic

ServerIP = "ServerIP:Port"

# requests to delete a task from the server - happend on clicking the delete button
def RDelete_Task(public_or_private: str, task_name: str, task_id: int, user_id: str) -> dict:
    url = f"http://{ServerIP}/delete/task/{public_or_private}/{task_name}/{task_id}/{user_id}"

    try:
        api_response = requests.delete(url)

        # analyze the response from the api in the form of the user check_list_items
        response = api_response.json()

    except requests.ConnectionError:
        response = {'response': 'Failed to connect to the server'}

    return response
