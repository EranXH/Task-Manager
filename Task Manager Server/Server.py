from fastapi import FastAPI
import uvicorn

from API import CheckListItems, Delete, InfoChange, Login, Save, Signup, Tasks, TreeBranches, UpdateInfoChange

ServerAPI = FastAPI()


# adding routes
ServerAPI.include_router(CheckListItems.router)
ServerAPI.include_router(Delete.router)
ServerAPI.include_router(InfoChange.router)
ServerAPI.include_router(Login.router)
ServerAPI.include_router(Save.router)
ServerAPI.include_router(Signup.router)
ServerAPI.include_router(Tasks.router)
ServerAPI.include_router(TreeBranches.router)
ServerAPI.include_router(UpdateInfoChange.router)


if __name__ == "__main__":
    uvicorn.run("Server:ServerAPI", host="45.32.144.224", port=8000, log_level="debug")
