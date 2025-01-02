#!/usr/bin/bash
export IS_LOCAL=True
docker run -d -p 4444:4444 --name selenium-hub selenium/hub:3.141.59                                                         
docker run -d --link selenium-hub:hub selenium/node-chrome:3.141.59
docker run -d --link selenium-hub:hub selenium/node-firefox:3.141.59