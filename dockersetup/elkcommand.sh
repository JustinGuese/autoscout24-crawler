#!/bin/bash

docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
  -v $PWD/elk/data:/usr/share/elasticsearch/data \
  -e "discovery.type=single-node" \
  elasticsearch:7.9.2
