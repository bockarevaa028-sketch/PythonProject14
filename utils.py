# utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from loguru import logger

def send_notification(subject, message, recipient, files=None):
    try:
        # Настройки SMTP (замените на ваши данные)
        SMTP_CONFIG = {
            'server': 'smtp.your-provider.com',
            'port': 587,
            'sender': 'your-email@domain.com',
            'password': 'your-app-password'  # Используйте пароль приложения
        }

        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = SMTP_CONFIG['sender']
        msg['To'] = recipient
        msg['Subject'] = subject

        # Добавление текста сообщения
        msg.attach(MIMEText(message, 'plain'))

        # Добавление вложений, если они есть
        if files:
            for file_path in files:
                if os.path.exists(file_path):
                    part = MIMEBase('application', "octet-stream")
                    with open(file_path, "rb") as attachment:
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f"attachment; filename= {os.path.basename(file_path)}"
                    )
                    msg.attach(part)
                else:
                    logger.warning(f"Файл не найден: {file_path}")

        # Отправка письма
        with smtplib.SMTP(
            SMTP_CONFIG['server'],
            SMTP_CONFIG['port']
        ) as server:
            server.starttls()
            server.login(
                SMTP_CONFIG['sender'],
                SMTP_CONFIG['password']
            )
            server.sendmail(
                SMTP_CONFIG['sender'],
                recipient,
                msg.as_string()
            )

        logger.info("Уведомление отправлено успешно")
        return True

    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {str(e)}")
        return False


def create_backup(source_dir, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logger.info(f"Создана директория для бэкапа: {backup_dir}")

        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            backup_file = os.path.join(backup_dir, filename)

            if os.path.isfile(source_file):
                os.replace(source_file, backup_file)
                logger.info(f"Создана резервная копия: {filename}")

        return True

    except Exception as e:
        logger.error(f"Ошибка при создании резервной копии: {str(e)}")
        return False


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"Функция {func.__name__} выполнена за {execution_time:.2f} секунд"
        )
        return result
    return wrapper


def check_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Создана директория: {directory}")
        else:
            logger.info(f"Директория существует: {directory}")
    return True
