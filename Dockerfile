 # Базовий образ з Python 3.12
FROM python:3.12-slim

# Встановлюємо Node.js (наприклад, версії 18)
RUN apt-get update && apt-get install -y curl \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Встановити .NET SDK
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    apt-transport-https \
 && wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
 && dpkg -i packages-microsoft-prod.deb \
 && apt-get update \
 && apt-get install -y --no-install-recommends dotnet-sdk-8.0 \
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

CMD ["python", "run.py"]