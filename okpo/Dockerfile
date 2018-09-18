FROM python:3.6
COPY app.py /etc
COPY requirements.txt /etc
WORKDIR /etc
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["app.py"]