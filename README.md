# Learning Log

Веб-приложение для ведения журнала обучения (Learning Log), разработанное на Django и стилизованное с помощью Bootstrap 4. Позволяет пользователям регистрироваться, создавать темы для изучения и добавлять записи к каждой теме с разделением прав доступа (каждый пользователь видит и редактирует только свои темы и записи).

---

## Стек технологий

- **Python 3.12 / 3.14**
- **Django**
- **django-bootstrap4** (стилизация интерфейса)
- **WhiteNoise** (раздача статических файлов)
- **Gunicorn** (WSGI-сервер)
- **Docker & Docker Compose** (контейнеризация и оркестрация)
- **SQLite** (хранилище данных в persistent docker volume)

---

## Структура проекта

```text
learning_log/
├── compose.yaml              # Конфигурация запуска Docker Compose
├── Dockerfile                # Сборка контейнера приложения
├── .dockerignore             # Исключения для контекста Docker
├── .gitignore                # Исключения для Git
├── .env.example              # Пример переменных окружения
├── requirements.txt          # Зависимости проекта
├── manage.py                 # Управляющий скрипт Django
├── learning_log/             # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── learning_logs/            # Основное приложение (темы и записи)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/learning_logs/
│       ├── base.html
│       ├── index.html
│       ├── topics.html
│       ├── topic.html
│       ├── new_topic.html
│       ├── new_entry.html
│       └── edit_entry.html
└── users/                    # Приложение аутентификации и регистрации
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py
    └── templates/registration/
        ├── login.html
        ├── register.html
        └── logged_out.html
```

---

## Переменные окружения (.env)

Для работы приложения на сервере или локально создайте файл `.env` в корне проекта (на основе `.env.example`):

```bash
cp .env.example .env
```

| Переменная | Описание | Пример значения |
|---|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ Django | `random-secret-key-string` |
| `DJANGO_DEBUG` | Режим отладки (`True` для разработки, `False` для продакшена) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Список разрешённых хостов через запятую | `192.168.1.11,localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Доверенные источники для защиты CSRF | `http://192.168.1.11:8000` |
| `DJANGO_USE_HTTPS` | Использование HTTPS для кук сессий и CSRF (`True`/`False`) | `False` |
| `SQLITE_PATH` | Путь к базе данных SQLite внутри контейнера | `/app/data/db.sqlite3` |
| `APP_BIND_IP` | IP-адрес для привязки портов | `0.0.0.0` |
| `APP_PORT` | Внешний порт приложения | `8000` |

---

## Развёртывание через Docker Compose

### 1. Клонирование и настройка
```bash
git clone <URL_РЕПОЗИТОРИЯ> learning_log
cd learning_log
cp .env.example .env
# Отредактируйте .env при необходимости (укажите APP_PORT, ALLOWED_HOSTS и т.д.)
```

### 2. Запуск приложения
```bash
docker compose up -d --build
```

При запуске автоматически:
- Собирается Docker-образ на базе Python 3.12-slim;
- Применяются все миграции базы данных (`python manage.py migrate --noinput`);
- Собирается статика WhiteNoise (`python manage.py collectstatic --noinput`);
- Запускается Gunicorn на указанном порту;
- База данных SQLite сохраняется в именованном томе `learning_log_data`.

### 3. Создание суперпользователя (администратора)
```bash
docker compose exec web python manage.py createsuperuser
```

### 4. Проверка работы
```bash
docker compose ps
docker compose logs --tail=100 web
```
Приложение доступно в браузере по адресу:
`http://<IP-АДРЕС-СЕРВЕРА>:<APP_PORT>/` (например, `http://localhost:8000/` или `http://192.168.1.11:8000/`).

---

## Локальный запуск без Docker (для разработки)

```bash
python3 -m venv ll_env
source ll_env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Запуск тестов:
```bash
python manage.py test
```
