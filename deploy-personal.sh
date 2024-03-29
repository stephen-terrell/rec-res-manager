#!/usr/bin/bash

mkdir ./build/deploy

pip install -r ./requirements.txt --target ./build/deploy

cp -r ./src/ ./build/deploy
cp -r ./configuration/ ./build/deploy
cp ./user-config.json ./build/deploy

cd build/deploy

timestamp=$(date +%s)

zip -r ./$timestamp.zip *

cd ../..

aws s3 cp ./build/deploy/$timestamp.zip s3://rec-res-user-config-personal-379689532145/personal/$timestamp.zip

aws cloudformation create-stack --stack-name rec-res-service-stack-personal --template-body file://configuration/cloudformation/service-stack.yaml --parameters ParameterKey=buildArtifactBucketName,ParameterValue=rec-res-user-config-personal-379689532145 ParameterKey=buildArtifactObjectKey,ParameterValue=personal/$timestamp.zip ParameterKey=domainName,ParameterValue=api.personal.camp.stephenterrell.io ParameterKey=hostedZoneId,ParameterValue=Z07013631K40E93YQXYF5 ParameterKey=env,ParameterValue=personal --capabilities CAPABILITY_NAMED_IAM

rm -rf ./build/deploy

echo "build timestamp:"
echo $timestamp
