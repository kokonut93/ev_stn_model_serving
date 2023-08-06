# After cloning git repo, run this file by build_image.sh

FROM public.ecr.aws/lambda/python:3.8-arm64

COPY . /model

WORKDIR /model

RUN pip3 install -r requirements.txt

CMD ["inference.handler"]