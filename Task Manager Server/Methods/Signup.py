from Collections import AuthenticationCol

from icecream import ic


# called from Sinnup in the API folder
# check whether email address or username already exsist in the system
def CheckIdentifyingInfoDuplication(email: str, user_name: str) -> dict:
    # set the collection, to the private collection or the public collection base on the input
    email_dup = list(AuthenticationCol.find({"email": email}))
    user_name_dup = list(AuthenticationCol.find({"_id": user_name}))

    if not email_dup and not user_name_dup:
        return {"response": ""}      # this is a valid email address and user name
    if email_dup and not user_name_dup:
        return {"response": "this email address has already been used"}
    if not email_dup and user_name_dup:
        return {"response": "this user name has already been used"}
    if not email_dup and not user_name_dup:
        return {"response": "both email address and user name has already been used"}
