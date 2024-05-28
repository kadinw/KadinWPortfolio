'''
Provides a basic frontend
'''
import sys
from loguru import logger
import main

logger.add("debugging_notes.md", level = "TRACE", rotation="100 MB")

def load_users(user_collection, status_collection):
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)


def load_status_updates(user_collection, status_collection):
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user(user_collection, status_collection):
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user(user_collection, status_collection):
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if main.update_user(user_id, email, user_name, user_last_name, user_collection) is False:
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")

def search_user_advanced(user_collection, status_collection):
    '''
    Searches a user by specific traits and prints all
    '''
    print("Leave spaces blank if not applicable to your query.")
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.search_user_adv(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to look up a User")
    else:
        print("User found")


def search_user(user_collection, status_collection):
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"ID: {result}")



def delete_user(user_collection, status_collection):
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


def save_users(user_collection, status_collection):
    '''
    Saves user database into a file
    '''
    filename = input('Enter filename for users file: ')
    main.save_users(user_collection, filename)


def add_status(user_collection, status_collection):
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection, user_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status(user_collection, status_collection):
    '''
    Updates information for an existing status
    '''
    status_id = input('Status ID: ')
    user_id = input('New User ID: ')
    status_text = input('New Status text: ')
    if not main.update_status(status_id,  user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status(user_collection, status_collection):
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result is None:
        print("ERROR: Status does not exist")
    else:
        print(f"result")


def delete_status(user_collection, status_collection):
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def save_status(user_collection, status_collection):
    '''
    Saves status database into a file
    '''
    filename = input('Enter filename for status file: ')
    main.save_status_updates(filename, status_collection)


def quit_program(user_collection, status_collection):
    '''
    Quits program
    '''
    sys.exit()

def search_status_by_user(user_collection, status_collection):
    '''
    searches all statuses of a user
    '''
    user_id = input('Enter status ID to get statuses: ')
    result = main.search_status(user_id, status_collection)
    if result is None:
        print("ERROR: Statuses do not exist")
    else:
        print(f"result")

'''
This code will run a menu that the user will use to select operations to perform
on the database
'''
if __name__ == '__main__':
    with logger.catch():
        user_collection = main.init_user_collection()
        status_collection = main.init_status_collection()
        menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': add_user,
            'D': update_user,
            'E': search_user,
            'F': delete_user,
            'G': save_users,
            'H': add_status,
            'I': update_status,
            'J': search_status,
            'K': delete_status,
            'L': save_status,
            'Q': quit_program,
            'Z': search_status_by_user,
        }
        while True:
            user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Add user
                                D: Update user
                                E: Search user
                                F: Delete user
                                G: Save user database to file
                                H: Add status
                                I: Update status
                                J: Search status
                                K: Delete status
                                L: Save status database to file
                                Q: Quit
                                L: Search statuses by user

                                Please enter your choice: """)
            if user_selection.upper() in menu_options:
                menu_options[user_selection.upper()](user_collection, status_collection)
            else:
                print("Invalid option")
