# Bulletin_Board API -

Доска объявлений - backend-приложение для размещения объявлений
с возможностью оставлять отзывы, авторизацией через JWT и разграничением ролей (пользователь/администратор).

## Технологии

- **Python 3.13**
- **Django 5.2** + **Django REST Framework 3.17**
- **PostgreSQL 16** - основная база данных
- **Redis 7** - кэширование
- **JWT** - аутентификация (djangorestframework-simplejwt)
- **Docker** + **Docker Compose** - контейнеризация
- **pytest** - тестирование (покрытие 89%)
- **Swagger/OpenAPI** - документация API

## Функциональность

### Пользователи

- Регистрация и аутентификация (JWT)
- Роли: **пользователь** и **администратор**
- Восстановление пароля через email
- Профиль пользователя (имя, фамилия, телефон, город, аватар, e-mail)

### Объявления

- **CRUD** операции с объявлениями
- Пагинация (4 объявления на страницу)
- Поиск по заголовку, описанию
- Фильтрация по категории и цене
- Сортировка по цене и дате
- Загрузка изображений

### Отзывы

- Оставление отзывов под объявлениями
- Рейтинг (1-5 звезд)
- Фильтрация отзывов по объявлению

### Права доступа

| Действие               | Аноним | Пользователь | Админ |
|------------------------|--------|--------------|-------|
| Просмотр объявлений    | ✅      | ✅            | ✅     |
| Создание объявления    | ❌      | ✅            | ✅     |
| Редактирование своего  | ❌      | ✅            | ✅     |
| Редактирование чужого  | ❌      | ❌            | ✅     |
| Создание отзыва        | ❌      | ✅            | ✅     |
| Удаление своего отзыва | ❌      | ✅            | ✅     |
| Удаление чужого отзыва | ❌      | ❌            | ✅     |

#### Интеграции:

- CORS: Для обеспечения возможности взаимодействия фронтенда с API.
- Автодокументация API: Генерация документации (например, с использованием Swagger/OpenAPI).

#### Подключены сторонние пакеты:

- Django REST Framework — для реализации API
- django-filter — для расширенной фильтрации данных настроена обработка
  медиафайлов для загрузки изображений и аватаров

#### Тестирование: coverage

Проект использует **pytest** для тестирования.
Покрытие тестами составляет более 89%. Тестирование всех CRUD операций, прав доступа, фильтрации, пагинации.

### Установка и Запуск:

Данный проект использует Poetry для управления зависимостями.

- Клонируйте репозиторий: git clone https://github.com/PavelOleynikov/Bulletin_Board cd Bulletin_Board
- Создайте и активируйте виртуальное окружение: python -m venv venv source venv/bin/activate - для Linux/macOS;
  venv\Scripts\activate - для Windows
- Установите зависимости с помощью Poetry:
  poetry install
- Настройте переменные окружения. Рекомендуется использовать файл .env и установить переменную DJANGO_SETTINGS_MODULE в
  соответствии с вашим файловым путем.
- Примените миграции базы данных: poetry run python manage.py migrate
- Запустите сервер разработки
  Django: poetry run python manage.py runserver
- Убедитесь, что Redis запущен
- Для запуска всех тестов: poetry run pytest

  Перед запуском скопируйте `.env.example` в `.env` и укажите свои значения

### Запуск проекта с использованием Docker Compose

Файл docker-compose.yaml определяет конфигурацию для запуска всех необходимых сервисов вашего проекта: веб-приложения
Django, базы данных PostgreSQL, Redis.

Предварительные требования:

- Docker установлен и работает.
- Docker Compose установлен (обычно входит в состав Docker Desktop).
- Файл .env с необходимыми переменными окружения (например, DB_NAME, DB_USER, DB_PASSWORD).

Процесс запуска

- сборка и запуск всех сервисов -
  перейдите в корневую директорию вашего проекта (где находится файл docker-compose.yaml и Dockerfile).

- Затем выполните следующую команду:
  docker compose up -d --build или docker compose -f docker-compose.yaml up

* API будет доступно по адресу: http://localhost:8000/
* Для авторизации используйте полученный при регистрации email и пароль
* Для доступа к админке используйте адрес: http://localhost:8000/admin/

Проверка сервисов

- docker compose ps — все контейнеры должны быть в статусе Up
- docker compose logs -f web — логи Django

#### API Эндпоинты

###### Аутентификация

POST /users/register/ Регистрация  
POST /users/login/ Вход (JWT)  
POST /users/token/refresh/ Обновление токена  
POST /users/reset_password/ Сброс пароля  
POST /users/reset_password_confirm/ Подтверждение сброса  
GET /users/me/ Текущий пользователь  
GET /users/ Список пользователей

###### Объявления

GET /ads/ads/ Список объявлений (пагинация 4)  
GET /ads/ads/{id}/ Детали объявления  
POST /ads/ads/ Создать объявление  
PUT/PATCH /ads/ads/{id}/ Обновить объявление  
DELETE /ads/ads/{id}/ Удалить объявление  
GET /ads/categories/ Список категорий

###### Отзывы

GET /feedback/reviews/ Список отзывов  
POST /feedback/reviews/ Создать отзыв  
DELETE /feedback/reviews/{id}/ Удалить отзыв

#### Команды

- Остановка и удаление контейнеров: docker compose down
- Перезапуск: docker compose restart
- Миграции: docker compose exec web python manage.py migrate
- Суперпользователь: docker compose exec web python manage.py createsuperuser

#### Проверка установки

* docker --version
* docker compose version

### CI/CD Pipeline (GitHub Actions)

```markdown

Файл `.github/workflows/ci.yml`:

| Job | Описание |
|-----|----------|
| **lint** | Проверка кода flake8 |
| **test** | Запуск тестов Django |
| **build** | Сборка и публикация Docker образа |
| **deploy** | Деплой на сервер через SSH |

### Secrets GitHub

- `SECRET_KEY` — ключ Django
- `DOCKER_HUB_USERNAME` — логин Docker Hub
- `DOCKER_HUB_ACCESS_TOKEN` — токен Docker Hub
- `SSH_KEY` — приватный ключ
- `SSH_USER` — пользователь сервера
- `SERVER_IP` — IP сервера

### Процесс деплоя

1. Push → запуск workflow
2. Линтинг → тесты → сборка образа → публикация в Docker Hub → деплой на сервер

### Мониторинг деплоя

# На сервере

cd ~/Bulletin_Board
docker compose ps
docker compose logs -f web

* API будет доступно по адресу: http://111.88.146.99:8000/
* Для авторизации используйте полученный при регистрации email и пароль
* Для доступа к админке используйте адрес: http://111.88.146.99:8000/admin/
* API документация: http://111.88.146.99:8000/swagger/
```

### Структура проекта

**Bulletin_Board**

├── .github/  
│ ├── workflows/ # Документация CI/CD
│ ├── ci.yml
├── config/ # Настройки проекта  
│ ├── settings.py  
│ └── urls.py  
├── users/ # Приложение пользователей  
│ ├── models.py # Кастомная модель User  
│ ├── views.py # Регистрация, аутентификация  
│ ├── permissions.py  
│ ├── serializers.py  
│ ├── urls.py  
│ └── management/commands/csu.py  
├── ads/ # Приложение объявлений  
│ ├── models.py # Category, Ad  
│ ├── views.py # CRUD, поиск  
│ ├── permissions.py # IsAuthorOrAdmin  
│ ├── pagination.py  
│ ├── serializers.py  
│ ├── tests  
│ ├── urls.py  
│ └── validators.py  
├── feedback/ # Приложение отзывов  
│ ├── models.py # Review  
│ ├── views.py  
│ ├── serializers.py  
│ ├── urls.py  
│ └── permissions.py # IsAdminOrAuthor
├── static/
├── htmlcov/
├── templates/  
│ └── index.html # Фронтенд интерфейс   
├── .env.example  
├── .flake8  
├── .gitinore  
├── .dockerignore  
├── pytest.ini  
├── Dockerfile  
├── docker-compose.yaml  
├── manage.py  
├── poetry.lock  
├── pyproject.toml  
├── conftest.py  
├── pytest.ini    
└── README.md

### Доступный функционал:

* Регистрация и вход
* Просмотр объявлений (сетка карточек)
* Создание объявлений с изображениями
* Редактирование/удаление своих объявлений
* Просмотр деталей объявления
* Оставление отзывов (только для авторизованных)
* Удаление своих отзывов
* Поиск по заголовку и описанию
* Пагинация (4 объявления на страницу)

👤 Автор
Pavel Oleynikov
