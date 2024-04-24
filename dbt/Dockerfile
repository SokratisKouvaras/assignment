FROM ghcr.io/dbt-labs/dbt-postgres:1.7.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
WORKDIR /usr/src/app/assignment
CMD [ "build", "--profiles-dir", "profiles", "--fail-fast", "--full-refresh" ]