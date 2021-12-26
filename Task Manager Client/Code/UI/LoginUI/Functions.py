import pandas as pd


# gets user_name and user info and arrange the users options list
def ArrangeOptionsValues(UserInfo, user_name):
    keys_to_pop = ["_id", "tree", "tasks"]

    PublicUserOptions = UserInfo["public_user_info"].copy()
    list(map(PublicUserOptions.pop, keys_to_pop))

    PrivateUserOptions = UserInfo["private_user_info"].copy()
    list(map(PrivateUserOptions.pop, keys_to_pop))
    assign_incharge_dict = {"assign": [user_name], "incharge": [user_name]}
    PrivateUserOptions.update(assign_incharge_dict)

    # (PAP stands for: P - Public | A - And | P - Private)
    PAPUserOptions = (PublicUserOptions, PrivateUserOptions)

    return PAPUserOptions


# gets user_name and user info and arrange the users task and tree tuple of dataframes, also return the user_id
def ArrangeDFValues(UserInfo):
    PublicTasksDF = pd.DataFrame(UserInfo["public_tasks"])
    PrivateTasksDF = pd.DataFrame(UserInfo["private_tasks"])

    TasksDFs = (PublicTasksDF, PrivateTasksDF)

    PublicTreeDict = UserInfo["public_user_info"]["tree"]
    PublicTreeDF = pd.DataFrame({'URL': PublicTreeDict.keys(),
                                 'IDs': PublicTreeDict.values()})

    PrivateTreeDict = UserInfo["private_user_info"]["tree"]
    PrivateTreeDF = pd.DataFrame({'URL': PrivateTreeDict.keys(),
                                  'IDs': PrivateTreeDict.values()})

    TreeDFs = (PublicTreeDF, PrivateTreeDF)

    UserID = UserInfo['public_user_info']['_id']

    return TasksDFs, TreeDFs, UserID
