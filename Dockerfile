FROM python:3.8-alpine
RUN apk add --no-cache mariadb-dev build-base pkgconf
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
ENV MYSQL_USER root
ENV MYSQL_PASSWORD secret
ENV MYSQL_DB student
ENV MYSQL_HOST 34.125.223.69

ENV MYSQLCLIENT_CFLAGS "-I/usr/include/mariadb"
ENV MYSQLCLIENT_LDFLAGS "-L/usr/lib/"
ENTRYPOINT [ "python" ]
CMD ["app.py" ]
