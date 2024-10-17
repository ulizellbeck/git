FROM mongo:latest

RUN apt-get update && apt-get install -y wget

WORKDIR /app

COPY import_data.sh .

RUN chmod +x import_data.sh

CMD ["./import_data.sh"]
