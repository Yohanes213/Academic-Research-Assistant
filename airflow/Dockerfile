FROM apache/airflow:2.7.1

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Use ENTRYPOINT instead of multiple CMDs
ENTRYPOINT ["airflow"]
CMD ["scheduler"]

# CMD ["airflow", "db", "init"]

# CMD ["airflow", "webserver", "--port", "8080"]

# CMD ["airflow", "scheduler"]