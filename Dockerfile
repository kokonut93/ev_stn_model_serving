FROM bitnami/pytorch:2.0.1
LABEL maintainer "seokyang <snuoon@naver.com>"

COPY ./ /infer
WORKDIR /infer

RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["inference.py"]
