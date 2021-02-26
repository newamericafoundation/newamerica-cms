#!/bin/bash

curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.deb
dpkg -i --force-confnew elasticsearch-5.6.16.deb

# Enable script scoring
cat << EOF >> /etc/elasticsearch/elasticsearch.yml
script.inline: on
script.search: on
EOF

service elasticsearch restart
