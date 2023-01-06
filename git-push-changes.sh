#!/bin/zsh

sudo rm -rf dist
sudo rm -rf build
sudo rm -rf FairRedis.egg-info

git add .
git commit -m "Version 1+"
git push origin master