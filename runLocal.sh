#!/bin/bash
# Stop, remove, build and start container.
docker container stop simplelist
docker container rm simplelist
docker image rm simplelist
# THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker build . -t simplelist
docker run -d -p 5000:5000 --name simplelist simplelist