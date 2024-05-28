'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
import socialnetwork_model as snm


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        pass

    def add_user(self, user_id1, email, user_name1, user_last_name1):
        '''
        Adds a new user to the collection
        '''
        try:
            with snm.db.transaction():
                check = snm.users_table.find_one(user_id=user_id1)
                if check is None:
                    new_user = snm.users_table.insert(user_id=user_id1, user_email=email, user_name=user_name1, user_last_name=user_last_name1)
                else:
                    return False
            return True
        except Exception as e:
            print(f"Error in creating: {e}")
            return False

    def modify_user(self, user_id1, email, user_name1, user_last_name1):
        '''
        Modifies an existing user
        '''
        success = True
        try:
            snm.users_table.update(user_id=user_id1, user_email=email, user_name=user_name1, user_last_name=user_last_name1, columns=['user_id'])
            return success
        except Exception as e:
            success = False
        return False
            

    def delete_user(self, user_id1):
        '''
        Deletes an existing user
        '''
        try:
            print("User Delete:")
            snm.users_table.delete(user_id=user_id1)
            print("Status Delete:")
            snm.status_table.delete(user_id=user_id1)
            return True
        except Exception as e:
            print(f"Error occured while deleting: {e}")
            return False

    def search_user(self, user_id1):
        '''
        Searches for user data
        '''
        try:
            user = snm.users_table.find_one(user_id=user_id1)
            return user
        except Exception as e:
            print(f"Error finding User: {e}")
            return None
