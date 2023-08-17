# After cloning git repo, run this file by build_image.sh

FROM public.ecr.aws/lambda/python:3.9

WORKDIR /${LAMBDA_TASK_ROOT}

RUN yum update -y
RUN yum install git -y
RUN git clone https://github.com/hwangpeng-sam/model-serving.git .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/lambda-entrypoint.sh"]

CMD ["inference.handler"]