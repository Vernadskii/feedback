FROM python:3.11 as build
LABEL authors="d.vernadskii@gmail.com"
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Install system dependencies for psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create the application directory
RUN mkdir /app
WORKDIR /app

COPY . ./

RUN pip install poetry==1.8.3
RUN poetry install

RUN chmod -R a+rx /app

# Add entrypoint
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

EXPOSE 8000
# Run app
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["run"]