# 

import re
from datetime import datetime
from database import DataBase

db = DataBase()


def is_leap_year(year):
        if (year%4 == 0 and year % 100 !=0) or year % 400 ==0 :
            return True
        else:
            return False
            
def get_days(y, m):
    years = {'l_year': {2:29, (4,6,9,11): 30, (1,3,5,7,8,10,12):31}, 'year': {2:28, (4,6,9,11): 30, (1,3,5,7,8,10,12):31}}
    if is_leap_year(int(y)):
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

def within_age_limit(y):
    current_year = datetime.now().year
    diff = current_year -int(y)
    if diff == 0 or diff >65 or diff <18:
        return False
    else:
        return True

def dob_val(from_date = False, account_number = None):
    while True:
        if from_date:
            msg = '\nEnter the date(yyyy-mm-dd): '
        else:
            msg = '\nEnter your Date of Birth(yyyy-mm-dd): '
        dob = input(msg)
        pattern = r'^(19[0-9][0-9]|20[0-9][0-9])-(0[1-9]|1[0-2])-(0[1-9]|(1|2)[0-9]|3[0-1])'
        if re.search(pattern, dob):
            y, m, d = dob.split('-')
            days = get_days(y, m)
            if from_date and int(d) <= days:
                account_od = db.get_file_data(account_number, 'transactions.json')
                val_date = datetime.strptime(dob, '%Y-%m-%d')
                if val_date > datetime.now():
                    print('\nDate should be from the past not form the future.')
                else:
                    for i in account_od[0]:
                        if val_date < datetime.strptime(i, '%Y-%m-%d %H:%M:%S'):
                            print(f'\nTransaction data is only avaialable from {i.split(' ')[0]} onwards.')
                        else:
                            return val_date
            else:
                if from_date:
                    print('\nEnter date is invalid')
                
            if not from_date and int(d) <= days:
                if within_age_limit(y):
                    break
                else:
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


# print(dob_val())
print('after dob validation')
value = dob_val(from_date=True, account_number="76156132256")
print(value)
print(type(value))