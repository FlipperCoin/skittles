param($tag)
if (!$tag)
{
    Write-Output "enter a tag"
    exit
}

Set-Variable WORKDIR ../../
Set-Location $WORKDIR

# build
docker build src/traffic-generator/ --tag=flippercoin/traffic-generator:$tag
docker save -o compiled/traffic-generator-image.docker flippercoin/traffic-generator:$tag