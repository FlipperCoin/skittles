param($tag)
if (!$tag)
{
    Write-Output "enter a tag"
    exit
}

# webapi app build
docker build . --tag=flippercoin/webapi:$tag

#deploy
docker save -o ../../compiled/webapi-image.docker flippercoin/webapi:$tag
scp ../../compiled/webapi-image.docker itai@10.0.0.12:~
ssh itai@10.0.0.12 'sudo docker load -i ~/webapi-image.docker'
kubectl set image ../../deployment/webapi webapi=flippercoin/webapi:$tag