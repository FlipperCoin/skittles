param($tag)
if (!$tag)
{
    Write-Output "enter a tag"
    exit
}

# Set-Variable WORKDIR ../../
# Set-Location $WORKDIR

# build
docker build src/records-loadbalancer/ --tag=flippercoin/records-loadbalancer:$tag
docker save -o compiled/records-loadbalancer-image.docker flippercoin/records-loadbalancer:$tag

#deploy
scp compiled/records-loadbalancer-image.docker itai@10.0.0.12:~
ssh itai@10.0.0.12 'sudo docker load -i ~/records-loadbalancer-image.docker'
kubectl set image deployment/records-loadbalancer records-loadbalancer=flippercoin/records-loadbalancer:$tag