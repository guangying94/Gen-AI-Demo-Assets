FROM python:3.12-slim

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install only the necessary dependencies for SQL Server connectivity
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Download the package to configure the Microsoft repo
RUN curl -sSL -O https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb

RUN apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
#RUN source ~/.bashrc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3","main.py"]