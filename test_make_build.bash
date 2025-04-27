#!/usr/bin/bash

BuildDir="build"

if [ $1 ]; then
    BuildDir=$1
fi

if [ -d "$BuildDir" ]; then
    rm -rf $BuildDir
fi

mkdir $BuildDir
cp production/auth_service/dockerfile $BuildDir/
cp production/auth_service/docker-compose.yml $BuildDir/
cp production/auth_service/start_service.py $BuildDir/

cp requirements.txt $BuildDir/
cp -r src/auth_service $BuildDir/
cp -r src/shared_lib $BuildDir/
