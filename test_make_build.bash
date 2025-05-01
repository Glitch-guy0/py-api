#!/usr/bin/bash

BuildDir="builds/services/auth_service"

if [ -d "$BuildDir" ]; then
    rm -rf $BuildDir
fi

mkdir -p $BuildDir
cp production/services/auth_service/dockerfile $BuildDir/
cp production/services/auth_service/docker-compose.yml $BuildDir/
cp production/services/auth_service/start_service.py $BuildDir/

cp requirements.txt $BuildDir/
cp -r src/services/auth_service $BuildDir/
cp -r src/services/shared_lib $BuildDir/
