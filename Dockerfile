FROM python:3.13

# Установка рабочей директории
WORKDIR /1122

# Установка необходимых системных зависимостей
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Установка pip и Poetry, а также зависимостей проекта
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Установка Pillow и gunicorn
RUN pip install Pillow gunicorn

# Копирование остального кода приложения
COPY . .

# Создание пользователя для запуска приложения
RUN adduser --disabled-password --gecos "" myuser

# Установка прав доступа к директории приложения
RUN chown -R myuser:myuser /1122

# Переключение на нового пользователя
USER myuser

# Открытие порта
EXPOSE 8000

# Команда для запуска приложения с использованием gunicorn
CMD ["gunicorn", "1122.wsgi:application", "--bind", "0.0.0.0:8000"]