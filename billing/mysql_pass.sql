use mysql;
UPDATE user SET password=PASSWORD('password') WHERE user='root';
flush privileges;

