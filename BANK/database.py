import os
import json
from datetime import datetime
from encryption import Crypto_encryption


encrypt = Crypto_encryption()

class DataBase:
    def create_database_folder(self, account_number=None, partial=None):
        if account_number:
            folder_path = os.getcwd()
            new_folder_path = os.path.join(os.path.dirname(folder_path), 'DataBase', account_number)
            os.makedirs(new_folder_path, exist_ok=True)
            return new_folder_path
        elif partial:
            folder_path = os.getcwd()
            new_folder_path = os.path.join(os.path.dirname(folder_path), 'DataBase', 'Partial')
            os.makedirs(new_folder_path, exist_ok=True)
            return new_folder_path

    def get_database_path(self, account_number=None, partial = None):
        if account_number:
            folder_path = os.getcwd()
            main_folder_name = os.path.dirname(folder_path)
            return os.path.join(main_folder_name, 'DataBase', account_number)
        elif partial:
            folder_path = os.getcwd()
            main_folder_name = os.path.dirname(folder_path)
            return os.path.join(main_folder_name, 'DataBase', partial)
    
    def is_file_exist(self,file_name, account_number=None,partial=None ):
        if account_number:
            path = self.get_database_path(account_number)
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                return True
            else:
                return False
        elif partial:
            path = self.get_database_path(partial)
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                return True
            else:
                return False

    
    def dump_data_into_partial_data_file(self, data):
        if not self.is_file_exist(partial="Partial", file_name='partial_data.json' ):
            database_path = self.create_database_folder(partial='Partial')
            file_path = os.path.join(database_path, 'partial_data.json')
            with open(file_path, 'w') as json_file:
                user_data = {1: data}
                json.dump(user_data, json_file, indent=4)
        else:
            database_path = self.get_database_path(partial='Partial')
            file_path = os.path.join(database_path, 'partial_data.json')
            with open(file_path, 'r') as json_file:
                user_data = json.load(json_file)
            
            l_data = len(user_data) + 1
            user_data.update({l_data:data})
            with open(file_path, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)


    def dump_data_into_accounts_file(self, account_number, user_data):
        if not self.is_file_exist(account_number, 'account_details.json'):
            database_path = self.create_database_folder(encrypt.decrypt_value(account_number))
            file_path = os.path.join(database_path, 'account_details.json')
            with open(file_path, 'w') as json_file:
                user_data = {f'{account_number}': user_data}
                json.dump(user_data, json_file, indent=4)


    def dump_data_into_credentials_file(self, account_number, pwd):
        if not self.is_file_exist(account_number, 'credentials.json'):
            database_path = self.create_database_folder(encrypt.decrypt_value(account_number))
            file_path = os.path.join(database_path, 'credentials.json')
            with open(file_path, 'w') as json_file:
                user_data = {f'{account_number}': {'pwd': pwd, 'count': 0}}
                json.dump(user_data, json_file, indent=4)

    def get_file_data(self, account_number, file):
        database_path = self.get_database_path(encrypt.decrypt_value(account_number))
        if os.path.isdir(database_path):
            file_path = os.path.join(database_path, file)
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data[account_number]
        else:
            return f'Fail-No Directory for account number {account_number}.'
        
    def update_file_data(self, account_number, file, data):
        database_path = self.get_database_path(encrypt.decrypt_value(account_number))
        file_path = os.path.join(database_path, file)
        with open(file_path, 'r') as file:
                c_data = json.load(file)
        if isinstance(c_data[account_number], list):
            c_data[account_number].append(data)
        else:
            c_data[account_number] = data
        with open(file_path, 'w') as json_file:
                json.dump(c_data, json_file, indent=4 )

    def dump_data_into_transactions_file(self, account_number):
        if not self.is_file_exist(account_number, 'transactions.json'):
            database_path = self.create_database_folder(encrypt.decrypt_value(account_number))
            file_path = os.path.join(database_path, 'transactions.json')
            timestatmp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            trans_data = {
                    account_number : [{timestatmp: dict(balance = encrypt.encrypt_value(str(0)), deposite = encrypt.encrypt_value(str(0)), withdraw = encrypt.encrypt_value(str(0)))}]
                }
            with open(file_path, 'w') as json_file:
                json.dump(trans_data, json_file, indent=4)





