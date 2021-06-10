#!/bin/bash

git init .
git remote add origin https://github.com/asger-weirsoee/rest-vaccine-tilmelder
git remote update
git fetch
git checkout -b master
git pull origin master
