- By default, `mysqld` only listens on localhost; to change this, set
  `bind-address` in `/etc/mysql/my.cnf` to `0.0.0.0`.

- As of version 1.8.4, if an Ansible role's `defaults/main.yml` contains a
  variable that makes use of a password lookup, Ansible will look for & create
  the specified file in the role's `files` directory or, if that does not
  exist, its `tasks` directory.  Moreover, if two separate roles default the
  same variable to the same password lookup, they will use two separate files
  and passwords.
