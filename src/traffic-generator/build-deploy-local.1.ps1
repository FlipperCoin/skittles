param($tag)
if (!$tag)
{
    Write-Output "enter a tag"
    exit
}

# Set-Variable WORKDIR ../../
# Set-Location $WORKDIR

# build
docker build src/traffic-generator/ --tag=flippercoin/traffic-generator:$tag
docker save -o compiled/traffic-generator-image.docker flippercoin/traffic-generator:$tag

#deploy
scp compiled/traffic-generator-image.docker itai@10.0.0.12:~
ssh itai@10.0.0.12 'sudo docker load -i ~/traffic-generator-image.docker'
kubectl set image deployment/traffic-generator traffic-generator=flippercoin/traffic-generator:$tag