#!/bin/bash

curl -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.4.6/elasticsearch-2.4.6.deb
dpkg -i --force-confnew elasticsearch-2.4.6.deb

# Enable script scoring
cat << EOF >> /etc/elasticsearch/elasticsearch.yml
script.inline: on
script.search: on
EOF

service elasticsearch restart
