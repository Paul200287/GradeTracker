# Guide

## Backend

First, you need to initialize the docker containers

```bash
docker compose up --build
```

Then change to the *backend/* directory and install the required packages and activate the virtual environment (commands for Windows)

```bash
uv sync
```
```bash
.\.venv\Scripts\activate
```

Change to the *backend/app* directory and initialize the database with the following command

```bash
python .\initial_data.py
```

Start the API with the following command
```bash
fastapi dev
```


## Frontend

Change to the *frontend/* directory.

If not already installed, install the *pnpm* package manager with the following command
```bash
npm install -g pnpm
```

Now start the frontend with the following command
```bash
pnpm dev
```

The frontend will be reachable at the following address
```
http://localhost:5432/
```

## Tools

You can access the database via the tool adminer at the following address
```
http://localhost:8080/
```

The FastAPI Swagger UI will be reachable at the following address
```
http://127.0.0.1:8000/docs
```

## Default login data

### Web App

E-mail: admin@admin.com
Password: Kennwort1

### Adminer

System: Postgres
Server: db
Username: postgres
Password: Kennwort1
Database: app-grade-tracker

### FastAPI

E-mail: admin@admin.com
Password: Kennwort1