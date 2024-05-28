2024-01-30 18:30:23.274 | ERROR    | __main__:<module>:182 - An error has been caught in function '<module>', process 'MainProcess' (92629), thread 'MainThread' (8119439360):
Traceback (most recent call last):

> File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/menu.py", line 184, in <module>
    status_collection = main.init_status_collection()
                        │    └ <function init_status_collection at 0x101359a80>
                        └ <module 'main' from '/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/main.py'>

  File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/main.py", line 31, in init_status_collection
    s_collection = user_status.UserStatusCollection()
                   │           └ <class 'user_status.UserStatusCollection'>
                   └ <module 'user_status' from '/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/user_status.py'>

  File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/user_status.py", line 15, in __init__
    db.create_tables([Status], safe = True)

NameError: name 'db' is not defined
2024-01-30 18:31:43.169 | ERROR    | __main__:<module>:182 - An error has been caught in function '<module>', process 'MainProcess' (92652), thread 'MainThread' (8119439360):
Traceback (most recent call last):

> File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/menu.py", line 220, in <module>
    menu_options[user_selection.upper()](user_collection, status_collection)
    │            │              │        │                └ <user_status.UserStatusCollection object at 0x105f3a610>
    │            │              │        └ <users.UserCollection object at 0x105f39bd0>
    │            │              └ <method 'upper' of 'str' objects>
    │            └ 'q'
    └ {'A': <function load_users at 0x1057eb600>, 'B': <function load_status_updates at 0x105f322a0>, 'C': <function add_user at 0x...

  File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/menu.py", line 177, in quit_program
    close_database()

NameError: name 'close_database' is not defined
2024-01-31 11:28:39.185 | ERROR    | __main__:<module>:182 - An error has been caught in function '<module>', process 'MainProcess' (94456), thread 'MainThread' (8119439360):
Traceback (most recent call last):

> File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/menu.py", line 220, in <module>
    menu_options[user_selection.upper()](user_collection, status_collection)
    │            │              │        │                └ <user_status.UserStatusCollection object at 0x10158a7d0>
    │            │              │        └ <users.UserCollection object at 0x10158a750>
    │            │              └ <method 'upper' of 'str' objects>
    │            └ 'e'
    └ {'A': <function load_users at 0x100e3b600>, 'B': <function load_status_updates at 0x1015822a0>, 'C': <function add_user at 0x...

  File "/Users/kadinwilkins/Documents/GitHub/assignment-08-kadinw/menu.py", line 88, in search_user
    print(f"ID: {result.user_id}")

AttributeError: 'dict' object has no attribute 'user_id'
