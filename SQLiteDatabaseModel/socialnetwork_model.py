from playhouse.dataset import DataSet

#links to the database file
db = DataSet('sqlite:///socialnetwork.db')
database = db

'''
create user table and establishes columns
'''
users_table = db['Users']
users_table.insert(user_id=None, user_email=None, user_name=None, user_last_name=None)
users_table.delete(user_id=None, user_email=None, user_name=None, user_last_name=None)

'''
creates a status table  and establishes columns
'''
status_table = db['Status']
status_table.insert(status_id=None, user_id=None, status_text=None)
status_table.delete(status_id=None, user_id=None, status_text=None)
