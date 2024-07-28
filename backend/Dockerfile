FROM python:3.11-slim as build
LABEL authors="d.vernadskii@gmail.com"
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

RUN apt-get update && mkdir /app

WORKDIR /app

COPY . ./

RUN pip install poetry==1.8.3
RUN poetry install

# Add entrypoint
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

EXPOSE 8000
# Run app
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["run"]