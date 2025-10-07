import os
import sys
import subprocess
import logging
import time
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='devops.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def check_python_version():
    logging.info("Checking Python version...")
    if sys.version_info < (3, 6):
        logging.error("Python 3.6 or higher is required.")
        sys.exit("Python 3.6 or higher is required.")
    logging.info(f"Python version is {sys.version}")

def list_files(directory):
    logging.info(f"Listing files in directory: {directory}")
    try:
        files = os.listdir(directory)
        for f in files:
            print(f)
        logging.info(f"Found {len(files)} files.")
    except Exception as e:
        logging.error(f"Error listing files: {e}")

def run_shell_command(command):
    logging.info(f"Running shell command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        print(output)
        logging.info(f"Command output: {output}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.stderr.decode()}")

def monitor_file_changes(directory, interval=5):
    logging.info(f"Monitoring file changes in {directory} every {interval} seconds.")
    previous_files = set(os.listdir(directory))
    try:
        while True:
            time.sleep(interval)
            current_files = set(os.listdir(directory))
            added = current_files - previous_files
            removed = previous_files - current_files
            if added:
                logging.info(f"Added files: {added}")
                print(f"Added files: {added}")
            if removed:
                logging.info(f"Removed files: {removed}")
                print(f"Removed files: {removed}")
            previous_files = current_files
    except KeyboardInterrupt:
        logging.info("Stopped monitoring.")

def backup_files(source_dir, backup_dir):
    logging.info(f"Backing up files from {source_dir} to {backup_dir}")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    for filename in os.listdir(source_dir):
        src = os.path.join(source_dir, filename)
        dst = os.path.join(backup_dir, filename)
        if os.path.isfile(src):
            try:
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    fdst.write(fsrc.read())
                logging.info(f"Backed up {filename}")
            except Exception as e:
                logging.error(f"Failed to backup {filename}: {e}")

def main():
    check_python_version()
    print("DevOps Utility Script")
    print("1. List files in directory")
    print("2. Run shell command")
    print("3. Monitor file changes")
    print("4. Backup files")
    choice = input("Enter your choice (1-4): ")
    if choice == '1':
        directory = input("Enter directory path: ")
        list_files(directory)
    elif choice == '2':
        command = input("Enter shell command: ")
        run_shell_command(command)
    elif choice == '3':
        directory = input("Enter directory to monitor: ")
        interval = int(input("Enter interval in seconds: "))
        monitor_file_changes(directory, interval)
    elif choice == '4':
        source_dir = input("Enter source directory: ")
        backup_dir = input("Enter backup directory: ")
        backup_files(source_dir, backup_dir)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()