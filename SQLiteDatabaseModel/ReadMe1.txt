This repo contains the Python files: main.py, test_main.py, menu.py, socialnetwork_model.py, 
user_status.py, and users.py. 

Aside from this, the accounts.csv and status_updates.csv hold a list of users and statuses 
that can be loaded into the a database via the load_status_updates, and load_users
 functions within menu.py.

TO RUN THIS PROGRAM: Run the menu.py script, and follow the prompts in terminal.
This will create a database called 'socialnetwork.db' that all scipts in this repo will interact with.

A debugging_notes.md file is also available, where manuy of my previous tests in development are tracked.

Script Notes:

menu.py- the interface of this program that should be run.

main.py- the script that will be used to access the users.py and user_status.py classes
and interact with the database through them.

users.py- the script that runs all functions of a user and their database interactions

user_status.py- the script that runs all functions of a user_status and their database interactions

socialnetwork_model.py- the script that establishes the database 'socialnetwork.db'

test_main.py- a script containing functions used to test basic functions within main.py


PURPOSE OF THIS PROGRAM:
These sripts will be run through menu.py and will add users and statuses to a database called
'socialnetwork.db'. It is made with the intention to showcase basic skills in sqlite through Python,
and to create a database of users and their statuses, where statuses must have an attached user,
and be entirely dependent on them to persist. The database is purposefully created with a functional
approach in mind. The database is created after running this program, so feel free to 
delete socialnetwork.db between runs to test separate data entries. 