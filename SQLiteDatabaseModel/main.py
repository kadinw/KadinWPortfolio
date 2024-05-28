'''
main driver for a simple social network project
'''
import csv
from playhouse.dataset import DataSet
import socialnetwork_model as snm
import users
import user_status


def setUp(self):
    self.db = DataSet(':memory:')
    pass
def tearDown(self):
    pass


def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    u_collection = users.UserCollection()
    return u_collection


def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    s_collection = user_status.UserStatusCollection()
    return s_collection

def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    try:
        with snm.db.transaction():
            with open(filename, 'r') as csvfile:
                for row in csvfile:
                    emp_field = row.strip().split(',')
                    user_id, email, user_name, user_last_name = emp_field
                    if user_collection.add_user(user_id, email, user_name, user_last_name):
                        continue
                    else:
                        return False
            return True
    except Exception as e:
        print(f"User(s) cannot load: {e}")
        return False


def save_users(user_collection, filename):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    '''
    try:
        with open(filename, 'w', newline='') as csvfile:
            fields = ['user_id', 'user_name', 'user_last_name', 'user_email']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for user in user_collection.search_user():
                writer.writerow({
                    'user_id': user.user_id,
                    'user_name': user.user_name,
                    'user_last_name': user.user_last_name,
                    'user_email': user.user_email
                })
        return True
    except Exception as e:
        print(f"Error in saving: {e}")
        return False


def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    try:
        with snm.db.transaction():
            with open(filename, 'r') as csvfile:
                for row in csvfile:
                    status_field = row.strip().split(',')
                    user_id, status_id, status_text = status_field
                    if status_collection.add_status(user_id, status_id, status_text):
                        continue
                    else:
                        return False
            return True
    except Exception as e:
        print(f"Status(') cannot load: {e}")
        return False
    


def save_status_updates(filename, status_collection):
    '''
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    '''
    try:
        with open(filename, 'w', newline='') as csvfile:
            fields = ['status_id', 'user_id', 'status_text']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for status in status_collection.search_status():
                writer.writerow({
                    'status_id': status.status_id,
                    'user_id': status.user_id,
                    'status_text': status.status_text,
                })
        return True
    except Exception as e:
        print(f"Error in saving: {e}")
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    try:
        success = user_collection.add_user(user_id, email, user_name, user_last_name)
    except Exception as e:
        print(f"Error in adding: {e}")
        success = False
    return success


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    try:
        returner = user_collection.modify_user(user_id, email, user_name, user_last_name)
        return returner
    except Exception as e:
        print(f"An error has occured: {e}")
        return False


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    success = True
    try:
        if user_collection.search_user(user_id) is None:
            success = False
            print(f"User: {user_id} does not exist")
        else:
            user_collection.delete_user(user_id)
    except Exception as e:
        print(f"Error in user deletion: {e}")
        success = False
    return success


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    try:
        user1 = user_collection.search_user(user_id)
        if user1 is None:
            return None
        else:
            print("ID found.")
            return user1
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_status(user_id, status_id, status_text, status_collection, user_collection):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    if search_user(user_id, user_collection) is not None:
        try:
            success = status_collection.add_status(status_id, user_id, status_text)
        except Exception as e:
            print(f"Error in adding: {e}")
            success = False
    else:
        return False
    return success




def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    try:
        returner = status_collection.modify_status(status_id, user_id, status_text)
        return returner
    except Exception as e:
        print(f"An error has occured: {e}")
        return False



def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    success = True
    try:
        if status_collection.search_status(status_id) is None:
            success = False
            print(f"Status: {status_id} does not exist")
        else:
            status_collection.delete_status(status_id)
    except Exception as e:
        print(f"Error deleting: {e}")
        success = False
    return success


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    try:
        status1 = status_collection.search_status(status_id)
        if status1 is None:
            return None
        else:
            print("ID found.")
            return status1
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def search_status(user_id, status_collection):
    '''
    Searches for a statuses in status_collection attached to a user

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance and all others associated with a user.
    - Otherwise, it returns None.
    '''
    try:
        status1 = status_collection.search_status_uid(user_id)
        if status1 is None:
            return None
        else:
            print("ID found.")
            return status1
    except Exception as e:
        print(f"Error: {e}")
        return None