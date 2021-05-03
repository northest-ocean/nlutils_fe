PROJECT=timemagic
IMAGE=nlutils-fe
TAG=latest
if [ -n "$2" ] ; then
    TAG=$2
fi
IMAGE_URL=${PROJECT}/${IMAGE}:${TAG}
npm run build
sudo docker build -t ${PROJECT}/${IMAGE}:${TAG} .
sudo docker push ${PROJECT}/${IMAGE}:${TAG}