param($tag)
if (!$tag)
{
    Write-Output "enter a tag"
    exit
}


docker build . --tag=flippercoin/webapi:$tag
docker push flippercoin/webapi:$tag
kubectl set image deployment/hello-py webapi=flippercoin/webapi:$tag