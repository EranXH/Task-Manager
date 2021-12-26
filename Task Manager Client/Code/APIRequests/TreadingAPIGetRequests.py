import requests
import queue

from icecream import ic

ServerIP = "45.32.144.224:8000"


# used from the updated pusher tread - get updates from the server and push them to the user
def Tread_RGet_UserInfoChanged(public_or_private: str, user_id: str, function):
    while True:
        # public_or_private = queue_user_tasks_change.get()[1]
        # user_id = queue_user_tasks_change.get()[1]
        # user_tasks_ids = queue_user_tasks_change.get()[1]

        # requests for user check_list_items
        url = f"http://{ServerIP}/get/user_info_change/{public_or_private}/{user_id}"

        try:
            api_response = requests.get(url)
            # analyze the response from the api in the form of the user check_list_items
            api_json = api_response.json()

            # if "api_json" (the api response) contain any change calling the "UpdatesPusher" function in "MainUI.py"
            if len(api_json) and list(api_json.values()).count([]) != len(api_json):
                function(api_json)

        except requests.ConnectionError:
            continue


