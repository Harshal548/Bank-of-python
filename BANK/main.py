import os
import time
import logging
from customer_onboarding import Customer_onboarding
from otp import OTP
from database import DataBase
from signin import SignIN
from bank_ops import BankingOperations
from accounts_settings import Account_settings
from logging_config import setup_logging
from encryption import Crypto_encryption

encrypt = Crypto_encryption()
onboarding = Customer_onboarding()
otp = OTP()
db = DataBase()
login = SignIN()
bankOps = BankingOperations()
services = Account_settings()
WIDTH = bankOps.get_terminal_width()
logger = logging.getLogger('main')
class Main:
    def start_msg(self):
        print('\nHello there!!!')
        time.sleep(1)
        print('\nGreetings of the day!!!')
        time.sleep(1)
        print('\nWelcome to Bank Of Python!!!')

    def sigin_signup(self):
        print('\nSign In/Sign Up')
        while True:
            choice = input('\nChoose the option SignIn(1)/SignUp(2): ')
            if choice in ['1', '2']:
                break
            else:
                print('\nPlease enter the valid response...')
        return choice
    
    def bank_ops_prompt(self, account_number):
        flag = True if bankOps.get_balance(account_number)>0 else False
        if flag:
            print(' '*WIDTH)
            print('*'*WIDTH)
            print('''
            1. Deposite
            2. Withdraw
            3. Account Statement
            4. Previous Menu
            ''')
            print('*'*WIDTH)
        else:
            print(' '*WIDTH)
            print('*'*WIDTH)
            print('''
            1. Deposite
            2. Account Statement
            3. Previous Menu
            ''')
            print('*'*WIDTH)

        while True:
            if flag:
                opt = input('\nChoose the option, Deposite(1)/Withdraw(2)/Account Statement(3)/Previous Menu(4): ')
                if opt in ['1', '2', '3', '4']:
                    break
                else:
                    print('\nPlease enter teh valid option...')
            else:
                opt = input('\nChoose the option, Deposite(1)/Account Statement(2)/Previous Menu(3): ')
                if opt in ['1', '2', '3']:
                    if opt == '2':
                        opt = '3'
                    elif opt == '3':
                        opt = '4'
                    break
                else:
                    print('\nPlease enter teh valid option...')
        return opt
        
    def setting_services(self):
        print(' '*WIDTH)
        print('*'*WIDTH)
        print('''
            1. Passbook Download
            2. Profile Settings
            3. Account Services
            4. Previous Menu
        ''')
        print('*'*WIDTH)
        while True:
            opt = input('\nChoose the options Passbook Download(1)/Profile Settings(2)/Account Services(3)/Previous Menu(4): ')
            if opt in ['1', '2', '3', '4', '5']:
                break
            else:
                print('\nPlease enter the valid repsonse...')
        return opt
    
    def profile_setting_prompt(self, account_number):
        u_data = db.get_file_data(account_number, 'account_details.json')
        if bankOps.get_balance(account_number) > 50_000 and u_data.get('nominee'):
            print(' '*WIDTH)
            print('*'*WIDTH)
            print('''
            1.View Profile
            2.Edit Profile
            3.Edit nominee
            4.Previous Menu
            ''')
            print('*'*WIDTH)
            while True:
                opt= input('\nChoose the option, View Profile(1)/Edit Profile(2)/Edit nominee(3)/Previous Menu(4): ')
                if opt in ['1', '2', '3', '4']:
                    break
                else:
                    print('\nPlease enter the valid response')
        elif bankOps.get_balance(account_number) > 50_000 and not u_data.get('nominee'):
            print(' '*WIDTH)
            print('*'*WIDTH)
            print('''
            1.View Profile
            2.Edit Profile
            3.Add nominee
            4.Previous Menu
            ''')
            print('*'*WIDTH)
            while True:
                opt= input('\nChoose the option, View Profile(1)/Edit Profile(2)/Add nominee(3)/Previous Menu(4): ')
                if opt in ['1', '2', '3', '4']:
                    break
                else:
                    print('\nPlease enter the valid response')
        else:
            print(' '*WIDTH)
            print('*'*WIDTH)
            print('''
            1.View Profile
            2.Edit Profile
            3.Previous Menu
            ''')
            print('*'*WIDTH)
            while True:
                opt= input('\nChoose the option, View Profile(1)/Edit Profile(2)/Previous Menu(3): ')
                if opt in ['1', '2', '3']:
                    if opt == '3':
                        opt = 4
                    break
                else:
                    print('\nPlease enter the valid response')
        return opt


    def prompt_01(self):
        print(' '*WIDTH)
        print('*'*WIDTH)
        print('''
         1.Banking Oprations
         2.Account Settings and Services
         3.Exit
        ''')
        print('*'*WIDTH)
        while True:
            opt= input('\nChoose the option, Banking Operations(1)/Account settings and services(2)/exit(3): ')
            if opt in ['1', '2', '3']:
                break
            else:
                print('\nPlease enter the valid response')
        return opt
    
    def exit_msg(self):
        print('\nThanks for banking with us..')
        time.sleep(1)
        print('\nPlease visit again...')
        return True
    
    def prompt_orch(self, account_number):
        val = self.prompt_01()
        if val == '1':
            while True:
                opt = self.bank_ops_prompt(account_number)
                if opt == '1':
                    bankOps.deposite(account_number)
                elif opt == '2':
                    bankOps.withdraw(account_number)
                elif opt == '3':
                    statement = bankOps.account_statement(account_number)
                    print(statement)
                elif opt == '4':
                    if self.prompt_orch(account_number): 
                        os._exit(0)
        elif val == '2':
            while True:
                opt = self.setting_services()
                if opt == '1':
                    services.passbook_download(account_number)
                elif opt == '2':
                    opt = self.profile_setting_prompt(account_number)
                    if opt == '1':
                        profile = bankOps.user_profile(account_number)
                        print(profile)
                    elif opt == '2':
                        services.edit_profile(account_number)
                    elif opt == '3':
                        data = db.get_file_data(account_number, 'account_details.json')
                        if data.get('nominee'):
                            services.add_nomiee(account_number, update=True)
                        else:
                            services.add_nomiee(account_number)
                    elif opt == '4':
                        if self.prompt_orch(account_number):
                            os._exit(0)
                elif opt == '3':
                    services.set_trans_limit(account_number)
                elif opt == '4':
                    if self.prompt_orch(account_number):
                        os._exit(0)
        elif val == '3':
            return self.exit_msg()
        
    def engine(self):
        self.start_msg()
        choice = self.sigin_signup()
        if choice == '1':
            data = login.sign_in()
            if 'Pass' in data:
                account_number = data.split(',')[-1].strip()
                logger.info(f'User signed in successfully, with account numer, {account_number}')
                self.prompt_orch(encrypt.encrypt_value(account_number))
                
            else:
                account_number = data.split(':')[-1].strip()
                msg = data.split('.')[0]+'.'
                logger.warning(f'Sign in failed for account number {account_number}, message = {msg}')
                self.exit_msg()
        elif choice =='2':
            print('\nTo continue Please enter the following details.')
            data = onboarding.form()
            data = onboarding.update_contact_detials(data)
            otp.warning_msg(data)
            m_msg = otp.mobile_auth_ops(encrypt.decrypt_value(data['mobile_num']))
            e_msg = otp.email_auth_ops(encrypt.decrypt_value(data['email_id']), m_msg)
            logger.info(f'Email OTP result: {e_msg}, Mobile OTP result: {m_msg}, for user {data}')
            if 'Pass' in m_msg and 'Pass' in e_msg:
                account_number = encrypt.encrypt_value(onboarding.generate_account_number())
                pwd = encrypt.encrypt_value(onboarding.generate_pwd())
                db.dump_data_into_accounts_file(account_number, data)
                db.dump_data_into_credentials_file(account_number, pwd)
                db.dump_data_into_transactions_file(account_number)
                onboarding.send_onboarding_success_email(account_number, pwd, data)
                print(f'\nYour Account details has been sent to your Email ID: {encrypt.decrypt_value(data["email_id"])}.')
            else:
                logger.warning(f'Either Email OTP of mobile OTP has failed for user {data}')
                if 'Pass' in m_msg:
                    db.dump_data_into_partial_data_file(data)
                elif 'Pass' in e_msg:
                    db.dump_data_into_partial_data_file(data)
                else:
                    pass

if __name__ == '__main__':
    setup_logging()
    bank = Main()
    bank.engine()