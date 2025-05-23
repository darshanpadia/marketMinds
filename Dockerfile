FROM python:3.11
RUN mkdir /app
WORKDIR /app

ENV PYTHONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements_py311.txt /app/
RUN pip install -r requirements_py311.txt
COPY . /app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]