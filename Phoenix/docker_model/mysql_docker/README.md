```bash
sudo docker run -it --name=mysql-server -v /var/mysql:/data/mysql -v /var/exchange:/data/exchange -e MYSQL_ROOT_PASSWORD=pw -p 3301:3301 -d mysql:5.7 /bin/bash
```

设定时区

```bash
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

```bash
sudo docker run -it --name=mysql_server_1 --user 999:999 -v /etc/localtime:/etc/localtime -v /data/mysql/conf.d:/etc/mysql/conf.d -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=6414939  -p 3306:3306 -d mysql:8.0.32 /bin/bash
```


mysql14great

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newPassword';

```bash
docker run -it --name http_server -v /etc/localtime:/etc/localtime -v /data/apache_conf:/etc/apache2 -v /data/django:/var/www/html -p 80:80 -d httpd:2.4.57 /bin/bash
```

```bash
```

python3.7 only support Django3.2.18
python3.8 support Django3.2.18 and Django4.0.1

```bash
sudo docker run -it --name=http_server_1 -v /etc/localtime:/etc/localtime:ro -v /data/apache_conf:/etc/apache2 -v /data/website:/var/www/website -p 80:80 -d http_server_image:v1.0 /bin/bash
```
