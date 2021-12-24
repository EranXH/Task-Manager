from pymongo import MongoClient


client = MongoClient('localhost', 27017)


# adding mongoDB client
InfoChangePublicCol = client["Public"].InfoChange
InfoChangePrivateCol = client["Private"].InfoChange

TasksPublicCol = client["Public"].Tasks
TasksPrivateCol = client["Private"].Tasks

AuthenticationCol = client.Users_Authentication_DB.Users_Authentication

UsersPublicCol = client["Public"].Users
UsersPrivateCol = client["Private"].Users

CheckListItemsPublicCol = client["Public"].CheckListItems
CheckListItemsPrivateCol = client["Private"].CheckListItems

TreeBranchesPublicCol = client["Public"].TreeBranches
TreeBranchesPrivateCol = client["Private"].TreeBranches