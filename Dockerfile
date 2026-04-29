# Указываем базовый образ
FROM python:3.13.5

# Устанавливаем curl для проверки здоровья контейнера
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем poetry (без создания виртуального окружения)
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта (без создания виртуального окружения)
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Создаем директорию для медиафайлов и статики
RUN mkdir -p /app/media /app/static

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
