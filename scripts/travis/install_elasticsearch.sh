#!/bin/bash

curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.0-amd64.deb
dpkg -i --force-confnew elasticsearch-7.15.0-amd64.deb

chown -R elasticsearch:elasticsearch /etc/default/elasticsearch

service elasticsearch restart
