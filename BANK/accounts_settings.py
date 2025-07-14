from datetime import datetime, timedelta
from validator import Validator
from database import DataBase
from bank_ops import BankingOperations
from otp import OTP
import logging
db = DataBase()
validator = Validator()
bankOps = BankingOperations()
otp = OTP()

logger = logging.getLogger('accounts_settings')


class Account_settings:
    
    def format_amount(self, amount):
            if len(amount)>3:
                if len(amount) == 6:
                    return f'{amount[0]},{amount[1:len(amount)-3]},{amount[-3:]}'
                else:
                    return f'{amount[:len(amount)-3]},{amount[-3:]}'
            else:
                return amount
                
    def set_trans_limit(self, account_number):
        while True:
            flag = input('\nWanted to set transaction limit?(yes/no): ')
            if flag in ['yes', 'no']:
                break
            else:
                print('\nEnter the valid response, yes or no')
        if flag == 'yes':
            amount = validator.transcation_limit()
            data = db.get_file_data(account_number, 'credentials.json')
            data['Transaction_limit'] = amount
            db.update_file_data(account_number, 'credentials.json', data)
            amount = self.format_amount(amount)
            print(f'\nTransaction limit ₹{amount}/- has been set on your Savings Account.')
    
    def passbook_prompt(self):
        print('''
            1. Last 30 Days
            2. Last 60 Days
            3. Last 90 Days
            4. Last year
            5. From Date
        ''')

        while True:
            opt = input('\nChoose the options Last 30 Days(1)/Last 60 Days(2)/Last 90 Days(3)/Last Year(4)/From Date(5): ')
            if opt in ['1', '2', '3', '4', '5']:
                break
            else:
                print('\nPlease enter the valid repsonse...')
        return opt

    def passbook_download(self, account_number):
        opt = self.passbook_prompt()
        if opt == '1':
            value = datetime.now()- timedelta(days=30)
            d_path = bankOps.save_file(account_number, trans=0, t_date=value, days = 30)
            print(f'\nAccount Statment for the last 30 days has been downloaded on the {d_path}')
        elif opt == '2':
            value = datetime.now()- timedelta(days=60)
            d_path = bankOps.save_file(account_number, trans=0, t_date=value, days = 60)
            print(f'\nAccount Statment for the last 60 days has been downloaded on the {d_path}')
        elif opt == '3':
            value = datetime.now()- timedelta(days=90)
            d_path = bankOps.save_file(account_number, trans=0, t_date=value, days = 90)
            print(f'\nAccount Statment for the last 90 days has been downloaded on the {d_path}')
        elif opt == '4':
            value = datetime.now()- timedelta(days=365)
            d_path = bankOps.save_file(account_number, trans=0, t_date=value, days = 365)
            print(f'\nAccount Statment for the last 365 days has been downloaded on the {d_path}')
        elif opt == '5':
            value = validator.dob_val(from_date=True, account_number=account_number)
            d_path = bankOps.save_file(account_number, trans=0, t_date=value)
            print(f'\nAccount Statment form the date {datetime.strftime(value,"%Y-%m-%d") } to {datetime.now().strftime("%Y-%m-%d")} has been downloaded on the {d_path}')


    def add_nomiee(self, account_number, update = False):
        u_data = db.get_file_data(account_number, 'account_details.json')
        print('\nPlease enter the following data.')
        salutation = validator.salutation_val()
        first_name = validator.name_val('first')
        middle_name = validator.name_val('middle')
        last_name = validator.name_val('last')

        while True:
            relationship = input('\nPlease add relationship(Son/Spouse/Mother/Father): ')
            if relationship.lower() in ['son', 'spouse', 'father', 'mother']:
                break
            else:
                print('\nPlease enter valid realtionship.')
        name = f'{salutation}{first_name.capitalize()} {middle_name.capitalize()} {last_name.capitalize()}'
        u_data['nominee'] = dict(name = name, relationship =relationship)
        db.update_file_data(account_number,'account_details.json', u_data )
        if update:
            print(f'\n{name} has been updated as your nominee.')
        else:
            print(f'\n{name} has been added as your nominee.')

    def edit_profile(self, account_number):
        profile_change = []
        u_data = db.get_file_data(account_number, 'account_details.json')
        name = f'{u_data["salutaition"]}{u_data["first_name"]} {u_data["middle_name"]} {u_data["last_name"]}'
        print(f'\nFull Name: {name}')
        while True:
            u_ipt = input('\nWanted to change/edit full name?(yes/no): ')
            if u_ipt in ['yes', 'no']:
                break
            else:
                print('\nPlease enter the valid response, yes or no')
        if u_ipt == 'yes':
            u_data['salutaition'] = validator.salutation_val()
            u_data['first_name'] = validator.name_val('first')
            u_data['middle_name'] = validator.name_val('middle')
            u_data['last_name'] = validator.name_val('last')
            profile_change.append(True)
        
        print(f'\nDate of Birth: {u_data["dob"]}')
        while True:
            u_ipt = input('\nWanted to change/edit Date of birth?(yes/no): ')
            if u_ipt in ['yes', 'no']:
                break
            else:
                print('\nPlease enter the valid response, yes or no')
        if u_ipt == 'yes':
            u_data['dob'] = validator.dob_val()
            profile_change.append(True)
        print(f'\nAddress: {u_data["address"]}')
        while True:
            u_ipt = input('\nWanted to change/edit Address?(yes/no): ')
            if u_ipt in ['yes', 'no']:
                break
            else:
                print('\nPlease enter the valid response, yes or no')
        if u_ipt == 'yes':
            u_data['address'] = validator.address_val()
            u_data['pincode'] = validator.pincode_val()
            profile_change.append(True)

        if profile_change:
            print(f"\nTo update/change your profile data in database, you have to authenticate yourself, A OTP wil be sent on your registered email ID '{u_data['email_id']}'")
            msg = otp.email_auth_ops(u_data['email_id'], user_verify=True )
            if 'Pass' in msg:
                db.update_file_data(account_number, 'account_details.json', u_data)
            else:
                print('\nOTP authentication failed, not able to save the details.')
                logger.warning("Email OTP authetication failed, for changeing user details.")

    
        






