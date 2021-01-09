#!/bin/bash
# Stop, remove, container and image.
docker container stop simplelist
docker container rm simplelist
docker image rm simplelist