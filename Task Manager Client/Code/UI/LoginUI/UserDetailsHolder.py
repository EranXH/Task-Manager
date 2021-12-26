# a way to save the login information - using a simple object
class UserDetailsHolder (object):
    user_name_hash = None
    password_hash = None

    @classmethod
    def UpdateDetails(cls, user_name_hash, password_hash):
        cls.user_name_hash = user_name_hash
        cls.password_hash = password_hash
