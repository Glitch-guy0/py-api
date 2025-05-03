#!/usr/bin/bash

BuildDir="builds/services/user_service"

if [ -d "$BuildDir" ]; then
    rm -rf $BuildDir
fi

mkdir -p $BuildDir

cp production/services/user_service/dockerfile $BuildDir/
cp production/services/user_service/docker-compose.yml $BuildDir/
cp production/services/user_service/start_service.py $BuildDir/

cp -r src/services/user_service $BuildDir/
cp -r src/services/shared_lib $BuildDir/
cp ./requirements.txt $BuildDir/
