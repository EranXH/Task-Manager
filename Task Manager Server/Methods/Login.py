from Collections import AuthenticationCol

from Methods.UserInformation import GetUserInformation, GetAllUsersIDs
from Methods.Tasks import TypesListByTaskIDs, TasksByIDsList
from Methods.TreeBranches import GetUserTreeBranches


# return the user ID given a right username and password hash
def UserAuthenticator(user_name_hash, password_hash):
    user = list(AuthenticationCol.find({"_id": user_name_hash, 'password': password_hash}))

    try:
        return user[0]["user_ID"]
    except IndexError:
        return None


# return the user information, the public and the private tasks list given the user id
def ArrangeUserInformation(user_ID: str) -> dict:
    user_public_information = GetUserInformation('Public', user_ID)
    user_private_information = GetUserInformation('Private', user_ID)

    # Arrange the public and private user tree
    public_user_tree = GetUserTreeBranches("Public", user_ID, user_public_information["tasks"])
    user_public_information["tree"] = public_user_tree
    private_user_tree = GetUserTreeBranches("Private", user_ID, user_private_information["tasks"])
    user_private_information["tree"] = private_user_tree

    # Arrange the types each user has in his private and public tasks
    user_public_information["types"] = TypesListByTaskIDs("Public", user_public_information["tasks"])
    user_private_information["types"] = TypesListByTaskIDs("Private", user_private_information["tasks"])

    user_public_information["assign"] = GetAllUsersIDs()
    user_public_information["incharge"] = GetAllUsersIDs()
    user_private_information["assign"] = GetAllUsersIDs()
    user_private_information["incharge"] = GetAllUsersIDs()

    public_tasks = TasksByIDsList('Public', user_public_information['tasks'])
    private_tasks = TasksByIDsList('Private', user_private_information['tasks'])

    return_dict = {'public_user_info': user_public_information, 'private_user_info': user_private_information,
                   'public_tasks': public_tasks, 'private_tasks': private_tasks}

    return return_dict
