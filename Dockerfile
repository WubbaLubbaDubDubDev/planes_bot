FROM python:3.11.11-alpine3.21

WORKDIR app/

COPY . .

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

CMD ["python3", "main.py", "-d"]
