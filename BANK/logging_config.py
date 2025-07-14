import logging
import os

def setup_logging():
    current_folder_path = os.getcwd()
    main_folder_path = os.path.dirname(current_folder_path)
    logs_path = os.path.join(main_folder_path, 'LOGS')
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    
    formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
    module_names = [
        'customer_onboarding',
        'validator',
        'otp',
        'database',
        'signin',
        'block',
        'bank_ops',
        'accounts_settings',
        'encryption'
    ]

    for name in module_names:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        log_file_path = os.path.join(logs_path, f'{name}.log')
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)


    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.INFO)
    main_log_file_path = os.path.join(logs_path, 'main.log')
    main_file_handler = logging.FileHandler(main_log_file_path)
    main_file_handler.setFormatter(formatter)
    main_file_handler.setLevel(logging.INFO)
    main_logger.addHandler(main_file_handler)



    

