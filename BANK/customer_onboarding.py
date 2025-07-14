from validator import Validator
import time
import random
import string
from email.mime.text import MIMEText
import smtplib
import shutil
import logging
from encryption import Crypto_encryption

validator = Validator()
encrypt = Crypto_encryption()
logger = logging.getLogger('customer_onboarding')

class Customer_onboarding:
    def form(self):
        user_data = {}
        salutation = validator.salutation_val()
        user_data['salutaition'] = salutation
        first_name = validator.name_val('first')
        user_data['first_name'] = first_name
        middle_name = validator.name_val('middle')
        user_data['middle_name'] = middle_name
        last_name = validator.name_val('last')
        user_data['last_name'] = last_name
        dob = validator.dob_val()
        user_data['dob'] = dob
        address = validator.address_val()
        user_data['address'] = address
        pincode = validator.pincode_val()
        user_data['pincode'] = pincode
        mobile_num = validator.mobile_val()
        user_data['mobile_num'] = encrypt.encrypt_value(mobile_num)
        email_id = validator.email_val()
        user_data['email_id'] = encrypt.encrypt_value(email_id)
        logger.info(f'Collected user data: {user_data}')
        return user_data
    

    def update_contact_detials(self, data):
        t_size = shutil.get_terminal_size()
        t_width = t_size.columns
        text = '\033[1;31m Warning!!! \033[0m'
        padding = (t_width-len(text))//2 +5
        time.sleep(1)
        print()
        print('\033[1;31m*\033[0m'*padding+text+'\033[1;31m*\033[0m'*padding)
        print(f'''
Hello {data['first_name'].capitalize()},
    To validate your contact details, you are going to receive a OTP on your registered mobile number \033[1;32m+91-{encrypt.decrypt_value(data['mobile_num'])}\033[0m
    and Email Id \033[1;32m{encrypt.decrypt_value(data['email_id'])}\033[0m. You are going to get \033[1;31m3\033[0m chance to validate your credentials. If you are failed to provide
    correct OTP then your account will be deleted.

    Regards,
    Customer Onboarding Support, 
    Bank Of Python
            ''')
        print('\033[1;31m*\033[0m'*(t_width-1))
        time.sleep(1)
        print('\nWanted to change Eamil Id/Mobile Number? or Proceed for Authentication?')
        while True:
            choice = input('\nChange contact details(1)/Proceed for Authentication(2): ')
            if choice in ['1', '2']:
                break
            else:
                print('\nPlease enter the valid response(1 or 2)')

        if choice == '1':
            return self.change_contact_details(data)
        else:
            return data
        
    def change_contact_details(self, data):
        print('\nUpdating your contact details')
        time.sleep(1)
        print(f'\nCurrent Email ID: {encrypt.decrypt_value(data["email_id"])}')
        print(f'\nCurrent Mobile Number: {encrypt.decrypt_value(data["mobile_num"])}')

        new_mobile = validator.mobile_val()
        new_email = validator.email_val()

        data['mobile_num'] = encrypt.encrypt_value(new_mobile)
        data['email_id'] = encrypt.encrypt_value(new_email)
        return data

    def generate_account_number(self):
        acc_num = random.randint(11111111111, 99999999999)
        return str(acc_num)
    
    def generate_pwd(self):
        # Password must be contains 12 characters
        # Password should contains
        # at least one small letter
        # at least one capital letter
        # at least one digit
        # at least one special characters from !@#$%^&*
        pwd = []
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special_chars = '!@#$%^&*'
        chars = uppercase + lowercase + digits + special_chars
        pwd = [random.choice(chars) for i  in range(12)]
        return ''.join(pwd)
    
    def send_onboarding_success_email(self, account_number, pwd, data):
        sender_email = "bankofpython4598@gmail.com"
        app_password = "fktm kvbe zclq wkxc"
        subject = 'Welcome to Bank Of Python-Your Account Has Been Successfully Crated.'
        body = f'''
        Dear {data['first_name'].capitalize()},
            We are pleaseto inform you that your account has been partially created with Bank Of Python.

            Account Details:
                - Account Number : {encrypt.decrypt_value(account_number)}
                - Temporary Password: {encrypt.decrypt_value(pwd)}
            
            Please try to Sign In using above credentials, to enjoy the our banking services.

            If you have any questions and need assitance feel free to contact our customer
            support team.

            Thank for choosing Bank Of Python.

        Best regards,
        Customer Onboarding Team
        Bank Of Python
        '''
        msg = MIMEText(body)
        msg['Form'] = sender_email
        msg['To'] = encrypt.decrypt_value(data['email_id'])
        msg['Subject'] = subject

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, encrypt.decrypt_value(data['email_id']), msg.as_string())
            logger.info('Onboarding success email has ben sent successfully.')
        except Exception as e :
            print(f'Error: {str(e)}')
            logger.error(f'Failed to send onboarding email. Error{str(e)}')
        finally:
            server.quit()
