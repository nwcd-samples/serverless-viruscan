FROM public.ecr.aws/lambda/python:3.9

RUN echo ${LAMBDA_TASK_ROOT}

COPY app.py requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt

#install clamav
RUN yum install -y wget

RUN yum install -y clamav

RUN freshclam



#copy virus file
# COPY ./eicar.com ${LAMBDA_TASK_ROOT}/

# RUN clamscan -V
# RUN clamdscan  ${LAMBDA_TASK_ROOT}/eicar.com

CMD [ "app.handler" ]