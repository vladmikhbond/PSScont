 
# Базовий образ з Python 3.12 + dev tools
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
# FROM python:3.12-slim


# Встановлюємо Node.js (наприклад, версії 18)
RUN apt-get update && apt-get install -y curl \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Перевіримо версії
RUN python --version && node --version && npm --version

# Копіюємо requirements.txt у контейнер (опціонально — VS Code і сам це зробить)
COPY requirements.txt /tmp/requirements.txt
COPY run.py /run.py
COPY app /app

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r /tmp/requirements.txt
                                 
# Відкриваємо порт
EXPOSE 7000


# Робоча директорія в контейнері
# WORKDIR /

CMD ["python", "run.py"]