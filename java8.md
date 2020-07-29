---
title: Installing Java 8 in Ubuntu Trusty
tags:
    - Java
    - Ubuntu
---

Oracle Java 1.8 can be installed on Ubuntu Trusty as follows:

    sudo apt-add-repository -y ppa:webupd8team/java
    sudo apt-get update
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
    sudo apt-get install -y oracle-java8-installer

cf. <http://www.webupd8.org/2012/09/install-oracle-java-8-in-ubuntu-via-ppa.html>
