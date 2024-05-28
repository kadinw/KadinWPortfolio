import unittest
import main
import peewee as pw
from users import Users
from users import UserCollection
from user_status import UserStatusCollection
from socialnetwork_model import Users, Status, create_tables, close_database
from unittest.mock import patch
from unittest.mock import mock_open

'''
Test file. Each function within tests the corresponding function in main.py
'''
class Test_main(unittest.TestCase):

    def setUp(self):
        self.db = pw.SqliteDatabase(':memory:')
        self.db.connect()
        create_tables()
        self.userColl1 = UserCollection()
        self.user1 = Users('121', 'firstlast@email.com', 'first', 'last')
        self.userStat = UserStatusCollection()
        self.user_collection = main.init_user_collection()
        self.status_collection = main.init_status_collection()

    def tearDown(self):
        close_database()



    def test_add_user(self):
        self.assertEqual(self.user1.user_id, '121')
        self.assertEqual(self.user1.user_email, 'firstlast@email.com')
        self.assertEqual(self.user1.user_name, 'first')
        self.assertEqual(self.user1.user_last_name, 'last')
        self.userColl1.add_user('121', 'firstlast@email.com', 'first', 'last')
        self.assertEqual(self.userColl1.search_user(121).user_id, self.user1.user_id)
        self.assertEqual(self.userColl1.search_user(121).user_email, self.user1.user_email)
        self.assertEqual(self.userColl1.search_user(121).user_name, self.user1.user_name)
        self.assertEqual(self.userColl1.search_user(121).user_last_name, self.user1.user_last_name)
        
    def test_modify_user(self):
        self.userColl1.add_user('121', 'firstlast@email.com', 'first', 'last')
        self.userColl1.modify_user('121', 'jeffglass@email.com', 'Jeff', 'Glass') 
        self.assertEqual(self.userColl1.search_user('121').user_id, '121')
        self.assertEqual(self.userColl1.search_user('121').user_email, 'jeffglass@email.com')
        self.assertEqual(self.userColl1.search_user('121').user_name, 'Jeff')
        self.assertEqual(self.userColl1.search_user('121').user_last_name, 'Glass')

    def test_delete_user(self):
        self.userColl1.add_user('121', 'firstlast@email.com', 'first', 'last')
        self.assertEqual(self.userColl1.search_user('121').user_id, '121')
        self.userColl1.delete_user('121')
        self.assertEqual(self.userColl1.search_user('121').user_id, None)


    def test_search_user(self):
        self.userColl1.add_user('121', 'firstlast@email.com', 'first', 'last')
        self.assertEqual(self.userColl1.search_user('121').user_id, '121')
        self.assertEqual(self.userColl1.search_user('121').user_email, 'firstlast@email.com')
        self.assertEqual(self.userColl1.search_user('121').user_name, 'first')
        self.assertEqual(self.userColl1.search_user('121').user_last_name, 'last')

    def test_add_status(self):
        self.userColl1.add_user('122', 'jeffglass@email.com', 'Jeff', 'Glass')
        self.userStat.add_status('1', '122', 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_text, 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_id, '1')
        self.assertEqual(self.userStat.search_status('1').user_id, '122')

    def test_modify_status(self):
        self.userColl1.add_user('122', 'jeffglass@email.com', 'Jeff', 'Glass')
        self.userStat.add_status('1', '122', 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_text, 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_id, '1')
        self.assertEqual(self.userStat.search_status('1').user_id, '122')
        self.userStat.modify_status('1', '122', 'Modified')
        self.assertEqual(self.userStat.search_status('1').status_text, 'Modified')
        self.assertEqual(self.userStat.search_status('1').status_id, '1')
        self.assertEqual(self.userStat.search_status('1').user_id, '122')

    def test_delete_status(self):
        self.userColl1.add_user('122', 'jeffglass@email.com', 'Jeff', 'Glass')
        self.userStat.add_status('1', '122', 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_text, 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_id, '1')
        self.assertEqual(self.userStat.search_status('1').user_id, '122')
        self.userStat.delete_status('1')
        self.assertEqual(self.userStat.search_status('1').status_text, None)
        self.assertEqual(self.userStat.search_status('1').status_id, None)
        self.assertEqual(self.userStat.search_status('1').user_id, None)


    def test_search_status(self):
        self.userColl1.add_user('122', 'jeffglass@email.com', 'Jeff', 'Glass')
        self.userStat.add_status('1', '122', 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_text, 'Hello World')
        self.assertEqual(self.userStat.search_status('1').status_id, '1')
        self.assertEqual(self.userStat.search_status('1').user_id, '122')

    @patch('builtins.open', mock_open(read_data="124,test@email.com,Test,User"))
    def test_load_users(self):
        result = main.load_users('accounts.csv', self.user_collection)
        self.assertTrue(result)

    @patch('builtins.open', mock_open(read_data="124,test@email.com,Test,User"))
    def test_save_users(self):
        self.user_collection.add_user(5, 'test@email.com', 'First', 'Last')
        result = main.save_users('accounts.csv', self.user_collection)
        self.assertTrue(result)

    @patch('builtins.open', mock_open(read_data="1001,s12,Testing status"))
    def test_load_status_updates(self):
        result = main.load_status_updates('status_updates.csv', self.status_collection)
        self.assertTrue(result)

    @patch('builtins.open', mock_open(read_data="1001,s12,Testing status"))
    def test_save_status_updates(self):
        result = main.save_status_updates('status_updates.csv', self.status_collection)
        self.assertTrue(result)

    def test_main_add_users(self):
        result = main.add_user(3, 'test@email.com', 'First', 'Last', self.user_collection)
        self.assertTrue(result)

    def test_main_update_user(self):
        main.add_user('3', 'test@email.com', 'First', 'Last', self.user_collection)
        result = main.update_user('3', 'newTest@email.com', 'John', 'Doe', self.user_collection)
        self.assertTrue(result)

    def test_main_delete_user(self):
        main.add_user('3', 'test@email.com', 'First', 'Last', self.user_collection)
        result = main.delete_user('3', self.user_collection)
        self.assertTrue(result)

    def test_main_search_user(self):
        main.add_user('3', 'test@email.com', 'First', 'Last', self.user_collection)
        result = main.search_user('3', self.user_collection)
        self.assertTrue(result)

    def test_main_add_status(self):
        result = main.add_status('3', '1', 'Test status', self.status_collection, self.user_collection)
        self.assertTrue(result)

    def test_main_update_status(self):
        main.add_status('3', '1', 'Test status', self.status_collection, self.user_collection)
        result = main.update_status('1', '3', 'Modified status', self.status_collection)
        self.assertTrue(result)

    def test_main_delete_status(self):
        main.add_status('3', '1', 'Test status', self.status_collection, self.user_collection)
        result = main.delete_status('1', self.status_collection)
        self.assertTrue(result)

    def test_main_search_status(self):
        main.add_status('3', '1', 'Test status', self.status_collection, self.user_collection)
        result = main.search_status('1', self.status_collection)
        self.assertTrue(result)







if __name__ == '__main__':
    unittest.main()

