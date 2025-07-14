import time

from database import DataBase
from validator import Validator
from block import Block
from encryption import Crypto_encryption
import logging
import getpass
db = DataBase()

validator = Validator()
block = Block()
encrypt = Crypto_encryption()

logger = logging.getLogger('signin')

class SignIN:
    def sign_in(self):
        count = 0
        while count <2:
            account_number = input('\nPlease enter your account number: ')
            data = db.get_file_data(encrypt.encrypt_value(account_number), 'credentials.json') 
            if 'Fail' in data:
                if count == 2:
                    print('\nInvalid Account number.')
                    logger.warning(f'Invalid account number entered: {account_number}')
                    return f'Fail- Sign In, Invalid Account Number. Account Number: {account_number}'
                print('\nInvalid Account number.')
                count +=1
            else:
                if not block.is_user_blocked(account_number):
                    if data['count'] % 25 == 0:
                        print('\nTo continue change your password.')
                        data = self.change_pwd(data)
                        db.update_file_data(encrypt.encrypt_value(account_number)   , 'credentials.json', data)
                        if data.get('blocked'):
                            logger.warning(f'This Account {account_number} has been blocked due to old password is not matched.')
                            return f"Fail- Sign In, Your account is blocked, Please try after {data['blocked']}. Account Number: {account_number}"
                        else:
                            print('\nTo continue Please sign in again.')
                            return self.sign_in()
                    else:
                        data = self.log_in(data)
                        db.update_file_data(encrypt.encrypt_value(account_number), 'credentials.json', data)
                        if data.get('blocked'):
                            logger.warning(f'This account {account_number} has been blocked. Due to repated wrong password.')
                            return f"Fail- Sign In, Your account is blocked, Please try after {data['blocked']}. Account Number: {account_number}"
                        else:
                            return f'Pass - Sign In, {account_number}'
                else:
                    data['count'] += 1
                    db.update_file_data(account_number, 'credentials.json', data)
                    print(f'\nYour account is blocked, Please try after {data["blocked"]}.')
                    logger.warning(f'\nThis account {account_number} is blocked, Please try after {data["blocked"]}.')
                    return f"Fail- Sign In, Your account is blocked, Please try after {data['blocked']}. Account Number: {account_number}"
                    

    def log_in(self, data):
        count = 0
        while count <3:
            pwd = getpass.getpass('\nPlease enter your password: ')
            if pwd == encrypt.decrypt_value(data['pwd']):
                data['count']+=1
                break
            else:
                if count == 0:
                    print('\nPlease enter the correct password...')
                    data['count']+=1
                elif count ==1:
                    print('\nThis is your last chance, Your account will be blocked for next 8 hours.')
                    data['count']+=1
                else:
                    block_time = block.block_user(8)
                    data['blocked'] = block_time
        return data

    def change_pwd(self, data):
        count = 0
        while count <3:
            old_pwd = getpass.getpass('\nPlease enter your old password: ')
            if old_pwd == encrypt.decrypt_value(data['pwd']):
                while True:
                    new_pwd = validator.password_val()
                    if new_pwd == old_pwd:
                        print('\nPlease Enter the new password, Old password is not acceptable.')
                    else:
                        re_new_pwd = getpass.getpass('\nConfirm your new password: ')
                        if re_new_pwd == new_pwd:
                            data['pwd'] = encrypt.encrypt_value(new_pwd)
                            data['count'] = 1
                            break
                        else:
                            print('\nPasswords are not matching, Please enter again...')
                return data
            else:
                if count == 0:
                    print('\nPlease enter the correct password.')
                elif count == 1:
                    print('\nThis is your last chance. Your account will be blocked for next 8 hours.')
                else:
                    block_time = block.block_user(8)
                    data['blocked'] = block_time
                    data['count'] += 1
                    return data
                count +=1
                        


