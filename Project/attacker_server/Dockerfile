FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY attacker.py .
EXPOSE 9090
CMD ["python", "attacker.py"]