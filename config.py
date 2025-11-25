# Конфигурация путей

PATHS = {
    'data_input': 'data/input/',
    'data_output': 'data/output/',  # Убедитесь, что этот путь существует
    'reports_documents': 'reports/documents/',
    'reports_visualizations': 'reports/visualizations/',
    'models': 'models/'
}



# Конфигурация базы данных PostgreSQL
DB_CONFIG = {
    'url': 'postgresql://user:password@localhost:5432/your_database',
    'host': 'localhost',
    'port': 5432,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Конфигурация API
API_CONFIG = {
    'base_url': 'https://jsonplaceholder.typicode.com',  # Публичный тестовый API
    'endpoints': {
        'data': '/users',  # Для получения данных о пользователях
        'posts': '/posts',  # Для получения постов
        'comments': '/comments'
    },
    'headers': {
        'Content-Type': 'application/json'  # Для этого API токен не требуется
    },
    'params': {
        'limit': 10,  # Ограничение количества записей
        'offset': 0
    }
}


# Настройки логирования
LOGGING = {
    'level': 'INFO',
    'format': '{time} | {level} | {message}',
    'sink': 'app.log',
    'rotation': '500 KB'
}

# Настройки email уведомлений
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'port': 587,
    'username': 'your_email@example.com',
    'password': 'your_email_password',
    'sender': 'your_email@example.com',
    'recipients': [
        'recipient1@example.com',
        'recipient2@example.com'
    ]
}

# Общие настройки приложения
APP_SETTINGS = {
    'debug_mode': True,
    'max_workers': 4,
    'report_frequency': 'daily'
}
