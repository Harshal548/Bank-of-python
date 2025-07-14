import re
import logging
from datetime import datetime
from database import DataBase
import getpass

db = DataBase()
logger = logging.getLogger('validator')
class Validator:
    def salutation_val(self):
        while True:
            sal = input('\nChoose Salutation (Mr./Ms./Mrs.): ')
            pattern = r'^M(r|rs|s)\.'
            if re.search(pattern, sal):
                break
            else:
                ('\nEnter valid Salutation with proper format as given, Mr./Ms./Mrs/ ')
        return sal
    
    def name_val(self, sequence):
        while True:
            name = input(f'\nEnter your {sequence} name: ')
            pattern = r'^[A-Z][A-Z]+'
            if re.search(pattern, name):
                break
            else:
                print('\nEntr valid name in capital letters. e.g. RAM')
        return name

    def is_leap_year(self, year):
        if (year%4 == 0 and year % 100 !=0) or year % 400 ==0 :
            return True
        else:
            return False
            
    def get_days(self, y, m):
        years = {'l_year': {2:29, (4,6,9,11): 30, (1,3,5,7,8,10,12):31}, 'year': {2:28, (4,6,9,11): 30, (1,3,5,7,8,10,12):31}}
        if self.is_leap_year(int(y)):
            if int(m) == 2:
                days = years['l_year'][2]
            else:
                for i in years['l_year']:
                    if isinstance(i, tuple) and int(m) in i:
                        days = years['l_year'][i]
        else:
            if int(m) == 2:
                days = years['year'][2]
            else:
                for i in years['year']:
                    if isinstance(i, tuple) and int(m) in i:
                        days = years['year'][i]
        return days

    def within_age_limit(self, y):
        current_year = datetime.now().year
        diff = current_year -int(y)
        if diff == 0 or diff >65 or diff <18:
            return False
        else:
            return True

    def dob_val(self, from_date = False, account_number = None):
        while True:
            if from_date:
                msg = '\nEnter the date(yyyy-mm-dd): '
            else:
                msg = '\nEnter your Date of Birth(yyyy-mm-dd): '
            dob = input(msg)
            pattern = r'^(19[0-9][0-9]|20[0-9][0-9])-(0[1-9]|1[0-2])-(0[1-9]|(1|2)[0-9]|3[0-1])'
            if re.search(pattern, dob):
                y, m, d = dob.split('-')
                days = self.get_days(y, m)
                if from_date and int(d) <= days:
                    account_od = db.get_file_data(account_number, 'transactions.json')
                    val_date = datetime.strptime(dob, '%Y-%m-%d')
                    if val_date > datetime.now():
                        print('\nDate should be from the past not form the future.')
                    else:
                        for i in account_od[0]:
                            if val_date < datetime.strptime(i, '%Y-%m-%d %H:%M:%S'):
                                print(f"\nTransaction data is only avaialable from {i.split(' ')[0]} onwards.")
                            else:
                                return val_date
                else:
                    if from_date:
                        print('\nEnter date is invalid')
                    
                if not from_date and int(d) <= days:
                    if self.within_age_limit(y):
                        break
                    else:
                        logger.error(f'Users age is not in the range of 18-65. users dob is {dob}. Raising exception.')
                        raise Exception('\nYour age is not within the range of 18-65, so you are not eligible to open a bank account.')
                else:
                    if not from_date:
                        print('\nEnter date is invalid')
            else:
                if from_date:
                    e_msg = '\nEnter valid Date, Date must be in the format of yyyy-mm-dd'
                else:
                    e_msg = '\nEnter valid Date of Birth, DOB must be in the format of yyyy-mm-dd'
                print(e_msg)
        
        return dob
    
    def address_val(self):
        while True:
            address = input('\nEnter your address: ')
            pattern = r'^([0-9]|[A-Za-z,-])+[A-Z,a-z,. ]+'
            if re.search(pattern, address):
                break
            else:
                print('\nAddress must be contain, House/Flat No., Area/Street Name, Landmark etc.')
        return address
    
    def pincode_val(self):
        while True:
            pincode = input('\nPlease enter your area Pin Code: ')
            pattern = r'^(4[0-2]|4[4-9]|41\d|42\d|43[0-2]|43[4-9]|44|50\d|56\d|57\d|58\d)\d{3}$'
            if re.search(pattern, pincode):
                break
            else:
                logger.error(f'User is not belong to the listed states: {pincode}')
                raise Exception('\nRight now we only servces in Maharashtra, Karnataka and Telangana.')
        return pincode
    
    def mobile_val(self):
        while True:
            mobile_num = input('\nPlease enter your mobile number: ')
            pattern= r'^(9|8|7|6)\d{9}$'
            if re.search(pattern, mobile_num):
                break
            else:
                logger.info(f'User entered wrong mobile number. {mobile_num}')
                print('\nPlease enter the valid mobile number.')
        return mobile_num
    
    def email_val(self):
        while True:
            email_id = input('\nPlease enter your Gmail ID: ')
            pattern = r'^[a-z]+[\.]?[a-z0-9]*@gmail.com'
            if re.search(pattern, email_id):
                break
            else:
                url = 'https://support.google.com/mail/answer/9211434?hl=en'
                print(f'\nPlease enter the valid Gmail addres. We only accept the Gmail IDs. We follow the gmails username policy. \n{url}')
                logger.info(f'User entered wrong email id:{email_id}')
        return email_id
    

    def password_val(self):
        while True:
            pwd = getpass.getpass('\nPlease enter the new password: ')
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\D)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{12}$'
            if re.match(pattern, pwd):
                break
            else:
                print('''
                Password should of contained 12 characters and must contain atleast one:
                1. Capital Letter
                2. Small Letter
                3. Digit
                4. One Special Character from !@#$%^&*(no other special character allowed.)
                ''')
        return pwd
    
    def amount_val(self, withdraw = False, bal =0):
        while True:
            amount = input('\nPlease enter the amount: ')
            pattern = r'\d+'
            if re.fullmatch(pattern, amount):
                if amount == '0':
                    print('\nAmount must be greater than zero...')
                elif withdraw:
                    if int(amount) > bal:
                        print(f'Please enter the valid amount, your account balance is {bal}')
                    else:
                        break
                else:
                    break
            else:
                print('\nPlease enter the valid number, amount should be in digits...')                    
        return amount
    
    def transcation_limit(self):
        while True:
            amount = input('\nPlease Enter the amount: ')
            pattern = r'\d+'
            if re.fullmatch(pattern, amount):
                if amount == '0':
                    print('\nAmount must be greater than zero...')
                elif int(amount) > 1_00_000:
                    print('\nPlease enter the valid amount, maximum transaction limit is ₹1,00,000/- only.')
                else:
                    return amount
            else:
                print('Please enter the valid number, input should be in digits...')
            

    

    



