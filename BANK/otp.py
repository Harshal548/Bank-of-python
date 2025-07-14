import string
import random
import requests
import time
from email.mime.text import MIMEText
import smtplib
import logging

logger = logging.getLogger('otp')

class OTP:
    def warning_msg(self, data):
        print(f'''
Hello {data['first_name'].capitalize()},
    Make sure that your mobile/network device near to you, you are about to receive a OTP.
        ''')

    def mobile_otp_genrator(self):
        otp = []
        digits = string.digits
        for _ in range(6):
            otp.append(random.choice(digits))
        return ''.join(otp)

    def send_otp_mobile(self, mobile_number):
        BASE = "https://2factor.in/API/V1"
        API  = "415bbd8f-2b06-11f0-8b17-0200cd936042"
        otp = self.mobile_otp_genrator()
        url = f"{BASE}/{API}/SMS/+91{mobile_number}/{otp}/OTP1"
        r = requests.get(url, timeout=10)
        print(otp)
        return otp

    def mobile_auth_ops(self, mobile_number):
        max_tries = 2
        count = 0
        while count <=max_tries:
            otp = self.send_otp_mobile(mobile_number)
            print(f'\nOTP has been sent to the +91-{mobile_number}')
            u_otp = input('\nPlease enter your OTP: ')
            if u_otp.strip() == otp:
                print('\nYour Mobile number has been authenticated successfully...')
                msg = 'Pass - Mobile Authentication'
                break
            else:
                if count == 0 :
                    time.sleep(1)
                    print('\nYou have entered wrong OTP...!!!')
                    count += 1
                elif count == 1:
                    time.sleep(1)
                    print('\nPlease try again...\n\nThis is your last chance, Other wise your account will be partially deleted.')
                    count += 1
                else:
                    msg = 'Fail - Mobile Authentication.'
                    logger.warning(f'This account has been blocked due to failed OTP attempts for mobile validation. {mobile_number}')
                    print('\nYour account has been partially deleted.')
                    count +=1
        return msg
    
    def email_otp_genrator(self):
        otp = []
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special_chars = string.punctuation
        for _ in range(6):
            letter = uppercase + lowercase + digits + special_chars
            otp.append(random.choice(letter))
        return ''.join(otp)


    def send_otp_email(self, receiver_email, user_verify):
        # how to configure your mail for email service
        # 1. Go to the account settings and enable two step authentication
        # 2. Go to the App Passwords and generate password
        sender_email = "bankofpython512@gmail.com"
        app_password = "paxy gtkp ushl ijfm"
        if user_verify:
            otp = self.mobile_otp_genrator()
            subject = 'Bank Of Python-User Authentication'
            body = f'Your OTP for User Authentication is: {otp}'
        else:
            otp = self.email_otp_genrator()
            subject = 'Bank Of Python-Email Verification'
            body = f'Your OTP for Email Verification is: {otp}'
        msg = MIMEText(body)
        msg['Form'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e :
            print(f'Error: {str(e)}')
        finally:
            server.quit()
        return otp


    def email_auth_ops(self, email, flag=None, user_verify = False):
        max_tries = 2
        count = 0
        while count <=max_tries:
            otp = self.send_otp_email(email, user_verify)
            print(f'\nOTP has been sent to the {email}')
            u_otp = input('\nPlease enter your OTP: ')
            if u_otp.strip() == otp:
                print('\nYour Email Id has been authenticated successfully...')
                msg = 'Pass - Email Authentication'
                break
            else:
                if count == 0 :
                    time.sleep(1)
                    print('\nYou have entered wrong OTP...!!!')
                    count += 1
                elif count == 1:
                    time.sleep(1)
                    if flag and 'Fail' in flag:
                        print('\nPlease try again...\n\nThis is your last chance, Other wise your account will be deleted.')
                        count += 1
                    elif user_verify:
                        print('\nPlease try again...\n\nThis is your last chance, Other wise your account will be blocked for two hours.')
                        count += 1
                    else:
                        print('\nPlease try again...\n\nThis is your last chance, Other wise your account will be partially deleted.')
                        count += 1
                else:
                    msg = 'Fail - Email Authentication.'
                    if flag and 'Fail' in flag:
                        print('\nYour account has been deleted.')
                        logger.warning(f'This users data has been deleted. Since it failed to authenticates is mobile number and email id{email}. ')
                        count +=1
                    else:
                        if user_verify:
                            logger.warning(f'This account has been blocked due to failed in user authentication, {email}')
                            print('\nYour account has been blocked.')
                        else:
                            print('\nYour account has been Partially deleted.')
                            logger.warning(f'This account has been partially deleted due to failed in email authentication, {email}')
                        count +=1
        return msg