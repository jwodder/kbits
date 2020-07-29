- By default, `mysqld` only listens on localhost; to change this, set
  `bind-address` in `/etc/mysql/my.cnf` to `0.0.0.0`.

- When setting up an Apache HTTPS proxy for an Atlassian application that
  forces all HTTP connections to be HTTPS, the URL rewrite rules must be placed
  in `sites-enabled/000-default.conf`, not `apache2.conf`.

- In order to set up an application link between two Atlassian applications
  where at least one of them uses HTTPS, the SSL certificate for each
  HTTPS-enabled application must be added to the other application's JRE's
  keystore by running:

        keytool -import -alias <server_name> \
            -keystore <JAVA_HOME>/lib/security/cacerts \
            -file /path/to/cert.crt

    (The password for the keystore is "`changeit`".)  For JIRA and Confluence,
    the Java home directory is `<INSTALLATION DIR>/jre`; other Atlassian
    applications use the system JRE (for OpenJDK, the Java home is
    `/usr/lib/jvm/java-7-openjdk-amd64/jre`).

    After adding the certificate, you will need to restart the application.

- As of version 1.8.4, if an Ansible role's `defaults/main.yml` contains a
  variable that makes use of a password lookup, Ansible will look for & create
  the specified file in the role's `files` directory or, if that does not
  exist, its `tasks` directory.  Moreover, if two separate roles default the
  same variable to the same password lookup, they will use two separate files
  and passwords.

- If a reverse proxy in front of Crowd connects to Crowd via a public IP
  address, then the remote addresses of the applications in Crowd will only
  need to be set to the proxy's IP address.  If the reverse proxy connects to
  Crowd at localhost, however, then the applications' remote addresses must be
  their actual public IP addresses instead.
