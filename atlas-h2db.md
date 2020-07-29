---
title: Connecting to an Atlassian app's embedded database
tags:
    - Atlassian
    - H2 database
---

To connect to an H2 ("embedded") database used by an Atlassian application,
[download the H2 JAR](http://www.h2database.com/html/download.html) and run:

    java -cp /path/to/h2.jar org.h2.tools.Shell -url jdbc:h2:$APP_HOME_DIR/database/h2db -user sa -password ''

(Note that the "`.h2.db`" suffix is omitted from the database name.)  You can
then test that you're actually in the database by running "`SHOW TABLES;`".
