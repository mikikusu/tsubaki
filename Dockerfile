FROM python:3.7-slim
RUN pip install flask

COPY hello.py /hello.py
EXPOSE 5000
CMD python /hello.py