'''
classes to manage the user status messages
'''
# pylint: disable=R0903
import socialnetwork_model as snm


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        #db.create_tables([Status], safe = True)
        pass

    def add_status(self, status_id1, user_id1, status_text1):
        '''
        add a new status message to the collection
        '''
        try:
            with snm.db.transaction():
                check = snm.users_table.find_one(user_id=user_id1)
                check2 = snm.status_table.find_one(status_id=status_id1)
                #print(check)
                if check is not None and check2 is None:
                    new_status = snm.status_table.insert(status_id=status_id1, user_id=user_id1, status_text=status_text1)
                else:
                    return False
            return True
        except Exception as e:
            print(f"Error in creating status: {e}")
            return False

    def modify_status(self, status_id1, user_id1, status_text1):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        success = True
        try:
            snm.status_table.update(status_id=status_id1, user_id=user_id1, status_text=status_text1, columns=['status_id'])
            #user = Users[user_id1]

            #query = Status[status_id1].update(
            #status_id = status_id1,
            #user_id = user_id1,
            #status_text = status_text1).where(Status.status_id == status_id1)
            #query.execute()
            return success
        except Exception as e:
            print(f"Error modifying status: {e}")
            success = False
        return False

    def delete_status(self, status_id1):
        '''
        deletes the status message with id, status_id
        '''
        try:
            snm.status_table.delete(status_id=status_id1)
            return True
        except Exception as e:
            print(f"Error deleting status: {e}")
            return False

    def search_status(self, status_id1):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        try:
            status = snm.status_table.find_one(status_id=status_id1)
            return status
        except:
            return None
        
    def search_status_uid(self, user_id1):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        try:
            status = snm.status_table.find(user_id=user_id1)
            return status
        except:
            return None

