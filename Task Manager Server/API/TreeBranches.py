from typing import List
from fastapi import APIRouter, Query

from Collections import TreeBranchesPublicCol, TreeBranchesPrivateCol

# Creating a new router to the API
router = APIRouter()


# return all the brache related tasks by a given list of branches IDs
# (MDB - MongoDB | Get - fastapi get function)
# operate as both MongoDB and fastapi function
@router.get('/get/tree_branches/{public_private}')
def MDB_Get_TreeBrachesByListID(public_private: str, Branches: List[str] = Query(None)) -> list:
    # set the collection, to the private collection or the public collection base on the input
    collection = TreeBranchesPublicCol if public_private == "Public" else TreeBranchesPrivateCol

    info = collection.find({"_id": {"$in": Branches}})

    return list(info)
