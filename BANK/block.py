from datetime import datetime, timedelta
from database import DataBase
from encryption import Crypto_encryption

encrypt = Crypto_encryption()
db = DataBase()


class Block:
    def block_user(self, duration):
        total_time = datetime.now() + timedelta(hours = duration)
        return total_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def is_user_blocked(self, account_number):
        u_data = db.get_file_data(encrypt.encrypt_value(account_number), 'credentials.json')
        block = False
        if u_data.get('blocked') and datetime.strptime(u_data['blocked'], '%Y-%m-%d %H:%M:%S') > datetime.now():
            block = True
        else:
            u_data['blocked'] = None
            db.update_file_data(encrypt.encrypt_value(account_number), 'credentials.json', u_data)
        return block