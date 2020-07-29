Creating an Atlassian-compatible PostgreSQL user and database:

- From the command line:

        sudo -u postgres createuser -SdrPE <username>  # then enter password for new user
        sudo -u postgres createdb --owner <username> -E utf8 -l C -T template0 <database>

- In SQL:

        CREATE USER <username> WITH NOSUPERUSER CREATEDB CREATEROLE ENCRYPTED PASSWORD '<password>';
        CREATE DATABASE <database> WITH OWNER <username> ENCODING 'utf8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;

- In Ansible:

        - postgresql_user:
            name: <username>
            password: <password>
            encrypted: true
            state: present
            role_attr_flags: NOSUPERUSER,CREATEDB,CREATEROLE,LOGIN
          become_user: postgres

        - postgresql_db:
            name: <database>
            owner: <username>
            encoding: UNICODE
            lc_collate: C
            lc_ctype: C
            template: template0
            state: present
          become_user: postgres
