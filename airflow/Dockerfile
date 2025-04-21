FROM apache/airflow:2.7.1

WORKDIR /opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["airflow"]
CMD ["scheduler"]
