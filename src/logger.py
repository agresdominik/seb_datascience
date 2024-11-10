import logging
import os
import shutil


def rotate_log_file(log_file_path, backup_log_file_path, log_folder_path) -> None:
    if os.path.exists(log_folder_path):
        if os.path.exists(backup_log_file_path):
            with open(backup_log_file_path, 'w'):
                pass
        else:
            print("app_old.log does not exist. Creating now...")
            with open(backup_log_file_path, 'w'):
                pass
        
        if os.path.exists(log_file_path):
            shutil.copy(log_file_path, backup_log_file_path)

        with open(log_file_path, 'w'):
            pass
    else:
        print("Error in accessing log folder, no logs will be saved.")


root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
log_folder_path = os.path.join(root_folder, 'log')
log_file_path = os.path.join(root_folder, 'log', 'app.log')
old_log_file_path = os.path.join(root_folder, 'log', 'app_old.log')

rotate_log_file(log_file_path, old_log_file_path, log_folder_path)

logger = logging.getLogger('datasience')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file_path)

console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
