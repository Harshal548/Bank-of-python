from datetime import datetime
import os
import logging
from colorama import Fore, Style
from database import DataBase
from validator import Validator
from encryption import Crypto_encryption
from block import Block
from otp import OTP
import re
db = DataBase()
validator = Validator()
otp_val = OTP()
block = Block()
encrypt = Crypto_encryption()
logger = logging.getLogger('bank_ops')

class BankingOperations:

    def format_amount(self, amount):
            amount = str(amount)
            if len(amount)>3:
                if len(amount) == 6:
                    return f'{amount[0]},{amount[1:len(amount)-3]},{amount[-3:]}'
                else:
                    return f'{amount[:len(amount)-3]},{amount[-3:]}'
            else:
                return amount
            
    def get_balance(self, account_number):
        data = db.get_file_data(account_number, 'transactions.json')
        for k,v in data[-1].items():
            prev_val = encrypt.decrypt_value(v['balance'])
        return int(prev_val)
    
    def deposite(self, account_number):
        amount = int(validator.amount_val())
        data = db.get_file_data(account_number, 'transactions.json')
        for k,v in data[-1].items():
            prev_bal = int(encrypt.decrypt_value(v['balance']))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {timestamp: dict(balance = encrypt.encrypt_value(str(prev_bal + amount)), deposite = encrypt.encrypt_value(str(amount)), withdraw = encrypt.encrypt_value(str(0)))}
        db.update_file_data(account_number, 'transactions.json', new_entry)
        print(f'\n₹{self.format_amount(amount)}/- has been deposited successfully on your account. Your total balance is ₹{self.format_amount(prev_bal + amount)}/-.')

    def withdraw(self, account_number):
        bal = self.get_balance(account_number)
        amount = int(validator.amount_val(withdraw=True, bal=bal))
        data = db.get_file_data(account_number, 'transactions.json')
        for k,v in data[-1].items():
            prev_bal = int(encrypt.decrypt_value(v['balance']))
        cred_data = db.get_file_data(account_number, 'credentials.json')
        if cred_data.get('Transaction_limit') and int(cred_data['Transaction_limit']) > amount:
            c_data = db.get_file_data(account_number, 'account_details.json')
            msg = otp_val.email_auth_ops(encrypt.decrypt_value(c_data['email_id']), user_verify= True)
            if 'Pass' in msg:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_entry = {timestamp: dict(balance = encrypt.encrypt_value(str(prev_bal - amount)), deposite = encrypt.encrypt_value(str(0)), withdraw = encrypt.encrypt_value(str(amount)))}
                db.update_file_data(account_number, 'transactions.json', new_entry)
                print(f'\n₹{self.format_amount(amount)}/- has been withdraw successfully from your account. Your total balance is ₹{self.format_amount(prev_bal - amount)}/-')
            else:
                cred_data = db.get_file_data(account_number, 'credentials.json')
                timestamp = block.block_user(2)
                cred_data['blocked'] = timestamp
                db.update_file_data(account_number, 'credentials.json', cred_data)
                logger.warning(f'Account {account_number} has been blocked due to incorrect otp, while money withdraw.')
                print(f'\nYour account has been blocked. Try after {cred_data["blocked"]}')
        else:
            if cred_data.get('Transaction_limit') and int(cred_data['Transaction_limit']) < amount:
                print('\nYour withdraw amount is exceeding the transaction limit.')
            else:
                c_data = db.get_file_data(account_number, 'account_details.json')
                msg = otp_val.email_auth_ops(encrypt.decrypt_value(c_data['email_id']), user_verify= True)
                if 'Pass' in msg:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_entry = {timestamp: dict(balance = encrypt.encrypt_value(str(prev_bal - amount)), deposite = encrypt.encrypt_value(str(0)), withdraw = encrypt.encrypt_value(str(amount)))}
                    db.update_file_data(account_number, 'transactions.json', new_entry)
                    print(f'\n₹{self.format_amount(amount)}/- has been withdraw successfully from your account. Your total balance is ₹{self.format_amount(prev_bal - amount)}/-')
                else:
                    cred_data = db.get_file_data(account_number, 'credentials.json')
                    timestamp = block.block_user(2)
                    cred_data['blocked'] = timestamp
                    logger.warning(f'Account {account_number} has been blocked due to incorrect otp, while money withdraw.')
                    print(f'\nYour account has been blocked. Try after {cred_data["blocked"]}')

    def get_terminal_width(self):
        width, _  = os.get_terminal_size()
        return width
    
    def get_empty_space(self, width, char_length):
        return width - char_length

    def account_statement(self, account_number, trans = -5, t_date = None):
        t_data = db.get_file_data(account_number, 'transactions.json')
        statment_date = datetime.now().strftime('%Y%m%d')
        for k, v in t_data[-1].items():
            total_bal = v['balance']
        
        dis_account_number = f'Account Number: {encrypt.decrypt_value(account_number)}'
        dis_statment_date = f'Statement Date: {statment_date}'
        dis_account_type = f'Account Type: Savings'
        dis_total_bal = f'Total Balance: {encrypt.decrypt_value(total_bal)}'

        t_width = self.get_terminal_width()
        empty_space_01 = self.get_empty_space(t_width, (len(dis_account_number) + len(dis_account_type)))
        empty_space_02 = self.get_empty_space(t_width, (len(dis_statment_date) + len(dis_total_bal)))

        line = []
        line.append(' '*t_width)
        line.append('*'*t_width)
        line.append(f'{{Bank Of Python:^{t_width}}}')
        #line.append(f'{'Bank Of Python':^{t_width}}')
        line.append('*'*t_width)
        line.append(f'{dis_account_number}{" "*empty_space_01}{dis_account_type}')
        line.append(f'{dis_statment_date}{" "*empty_space_02}{dis_total_bal}')
        line.append('*'*t_width)
        line.append(f'{{Transaction Details:^{t_width}}}')
        #line.append(f'{'Transaction Details':^{t_width}}')
        line.append('*'*t_width)
        line.append(f"{'':<28}{'Date':<28}{'Time':<28}{Fore.GREEN}{'Credit'}{Style.RESET_ALL}/{Fore.RED}{'Debit':<28}{Style.RESET_ALL}{'Balance':<28}")
        line.append('*'*t_width)
        for t in t_data[trans:]:
            for timestamp, transaction in t.items():
                date, time_ = timestamp.split(' ')
                if t_date and datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') >= t_date:
                    if encrypt.decrypt_value(transaction['deposite']) != '0':
                        line.append(f"{'':<26}{date:<28}{time_:<33}{Fore.GREEN}{encrypt.decrypt_value(transaction['deposite']):<33}{Style.RESET_ALL}{encrypt.decrypt_value(transaction['balance'])}")
                    elif encrypt.decrypt_value(transaction['withdraw'])!= '0':
                        line.append(f"{'':<26}{date:<28}{time_:<33}{Fore.RED}{encrypt.decrypt_value(transaction['withdraw']):<33}{Style.RESET_ALL}{encrypt.decrypt_value(transaction['balance'])}")
                else:
                    if not t_date:
                        if encrypt.decrypt_value(transaction['deposite']) != '0':
                            line.append(f"{'':<26}{date:<28}{time_:<33}{Fore.GREEN}{encrypt.decrypt_value(transaction['deposite']):<33}{Style.RESET_ALL}{encrypt.decrypt_value(transaction['balance'])}")
                        elif encrypt.decrypt_value(transaction['withdraw'])!= '0':
                            line.append(f"{'':<26}{date:<28}{time_:<33}{Fore.RED}{encrypt.decrypt_value(transaction['withdraw']):<33}{Style.RESET_ALL}{encrypt.decrypt_value(transaction['balance'])}")

        line.append('*'*t_width)
        line.append(' '*t_width)    
        return '\n'.join(line)

    def get_download_path(self, account_number):
        account_number = encrypt.decrypt_value(account_number)
        main_folder_path = os.path.dirname(os.getcwd())
        download_path = os.path.join(main_folder_path, 'Database', account_number, 'Downloads')
        os.makedirs(download_path, exist_ok=True)
        return download_path
    
    def save_file(self, account_number, trans, t_date, days=''):
        statement = self.account_statement(account_number, trans, t_date)
        download_path = self.get_download_path(account_number)
        ansi_esacpt_pattern = re.compile(r'\x1b\[[0-9;]*m')
        file_path = os.path.join(download_path, f'{encrypt.decrypt_value(account_number)}_{days}.txt')
        with open(file_path, 'w') as file:
            file.write(ansi_esacpt_pattern.sub('',statement))
        return download_path
    
    def user_profile(self, account_number):
        t_data = db.get_file_data(account_number, 'transactions.json')
        u_data = db.get_file_data(account_number, 'account_details.json')
        statment_date = datetime.now().strftime('%Y%m%d')
        for k, v in t_data[-1].items():
            total_bal = v['balance']
        
        dis_account_number = f'Account Number: {encrypt.decrypt_value(account_number)}'
        dis_statment_date = f'Statement Date: {statment_date}'
        dis_account_type = f'Account Type: Savings'
        dis_total_bal = f'Total Balance: {encrypt.decrypt_value(total_bal)}'
        dis_full_name = f'Full Name: {u_data["salutaition"]} {u_data["first_name"].capitalize()} {u_data["middle_name"].capitalize()} {u_data["last_name"].capitalize()}'
        dis_mobile_number = f'Mobile Number: +91-{encrypt.decrypt_value(u_data["mobile_num"])}'
        dis_email = f'Email ID: {encrypt.decrypt_value(u_data["email_id"])}'
        dis_pincode = f'Pincode: {u_data["pincode"]}'
        dis_address = f'Address: {u_data["address"]}'
        dis_dob = f'Date Of Birth: {u_data["dob"]}'

        t_width = self.get_terminal_width()
        empty_space_01 = self.get_empty_space(t_width, (len(dis_account_number) + len(dis_account_type)))
        empty_space_02 = self.get_empty_space(t_width, (len(dis_statment_date) + len(dis_total_bal)))
        empty_space_03 = self.get_empty_space(t_width, (len(dis_full_name) + len(dis_dob)))
        empty_space_04 = self.get_empty_space(t_width, (len(dis_email) + len(dis_pincode)))
        empty_space_05 = self.get_empty_space(t_width, (len(dis_mobile_number) + len(dis_address)))

        line = []
        line.append(' '*t_width)
        line.append('*'*t_width)
        line.append(f'{"Bank Of Python":^{t_width}}')
        line.append('*'*t_width)
        line.append(f'{dis_account_number}{" "*empty_space_01}{dis_account_type}')
        line.append(f'{dis_statment_date}{" "*empty_space_02}{dis_total_bal}')
        line.append('*'*t_width)
        line.append(f'{"User Profile":^{t_width}}')
        line.append('*'*t_width)
        line.append(f'{dis_full_name}{" "*empty_space_03}{dis_dob}')
        line.append(f'{dis_email}{" "*empty_space_04}{dis_pincode}')
        line.append(f'{dis_mobile_number}{" "*empty_space_05}{dis_address}')
        line.append('*'*t_width)
        line.append(' '*t_width)
        if u_data.get('nominee'):
            dis_nominee = f'Nominee: {u_data["nominee"]["name"]}'
            dis_rel = f'Relationship: {u_data["nominee"]["relationship"]}'
            empty_space_06 = self.get_empty_space(t_width, (len(dis_nominee) + len(dis_rel)))
            line.append('*'*t_width)
            line.append(f'{"Nominee Details":^{t_width}}')
            line.append('*'*t_width)
            line.append(f"{dis_nominee}{' '*empty_space_06}{dis_rel}")
            line.append('*'*t_width)
            line.append(' '*t_width)
        return '\n'.join(line)
        



        


    




            










