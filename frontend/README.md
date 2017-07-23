# Remote Car Control FrontEnd
## Introduction 

A "LAMP" stack is a group of open source software that is typically installed together to enable a server to host dynamic websites and web apps. This term is actually an acronym which represents the Linux operating system, with the Apache web server. The site data is stored in a MySQL database, and dynamic content is processed by PHP.

## Install Apache

> sudo apt-get update
> sudo apt-get install apache2

Verify it works: http://localhost

## Install MySQL

> sudo apt-get install mysql-server php5-mysql
> sudo mysql_install_db
> sudo mysql_secure_installation

> Username: root
> Password: 1!root

## Install PHP

> sudo apt-get install php5 libapache2-mod-php5 php5-mcrypt
> sudo vim /etc/apache2/mods-enabled/dir.conf 

Move the PHP index file: index.php to the first position after the DirectoryIndex, like this:

> <IfModule mod_dir.c>
>    DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
> </IfModule>

Restart apache:

> sudo service apache2 restart

For testing PHP, you have to create : vim /var/www/html/info.php and put the following text:

> <?php
> phpinfo();
> ?>

Now, you can visit : http://localhost//info.php
All .php files are located at /var/www/htm

## Install phpMyAdmin

> sudo apt-get install phpmyadmin apache2-utils

> Click on : http://localhost/phpmyadmin

> User: rcc
> Password: 1!root

Bibliography: 
* https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-14-04
* https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-ubuntu-12-04
