Installing MySQL on RHEL:

    sudo yum install http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
    sudo yum install mysql-community-server
    sudo systemctl enable mysqld
    sudo systemctl start mysqld
    mysql_secure_installation
