In order to simply import the entirety of one or more Apache access files into
Logstash without continuing to monitor them:

- Get a Logstash Forwarder installation
- Create a Logstash Forwarder config file of the form:

        {
          "network": { /* whatever's needed for the Logstash server */ },
          "files": [
              {
                  "paths": [ /* list of paths to access files */ ],
                  "fields": { "type": "apache" /*, whatever else */ }
              }
          ]
        }

- Touch any access files more than 24 hours old.
- Run:

        logstash-forwarder -from-beginning=true -config /path/to/config-file

    Apparently, newer versions of `logstash-forwarder` have the behavior of
    `-from-beginning=true` by default and no longer recognize this option.  I
    wonder if I'll ever get to encounter such a version....

- Once the program stops sending data, `^C`.
