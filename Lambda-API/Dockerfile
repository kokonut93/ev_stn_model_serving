# After cloning git repo, run this file by build_image.sh

FROM public.ecr.aws/lambda/python:3.9

COPY model.pt /model/
COPY requirements.txt /model/
COPY utils.py /model/
COPY inference.py /model/

WORKDIR /model

RUN pip3 install -r requirements.txt

CMD ["inference.handler"]