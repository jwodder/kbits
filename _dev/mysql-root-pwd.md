To specify the MySQL root password programmatically when installing, run:

    debconf-set-selections <<<'mysql-server-5.5 mysql-server/root_password password PASSWORD'
    debconf-set-selections <<<'mysql-server-5.5 mysql-server/root_password_again password PASSWORD'

before running `apt-get install mysql-server`.  (Adjust version number in
command as necessary.)  Note that there *must* be exactly one space between the
"password" keyword and the actual password.
