# After cloning git repo, run this file by build_image.sh

FROM public.ecr.aws/lambda/python:3.9

COPY ./* ${LAMBDA_TASK_ROOT}/

WORKDIR /${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/lambda-entrypoint.sh"]

CMD ["inference.handler"]