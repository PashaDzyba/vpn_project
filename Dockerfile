# Використовуйте офіційний образ Python як базовий
FROM python:3.9

RUN pip install --upgrade pip


# Встановіть робочу директорію в контейнері
WORKDIR /usr/src/app/vpn_project



# Встановіть залежності проекту
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копіюйте ваш проект в контейнер
COPY . .

# Вказуйте порт, який буде відкритий у контейнері
EXPOSE 8000

# Команда для запуску вашого проекту
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]