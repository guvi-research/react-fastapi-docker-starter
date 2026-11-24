# Quick project setup

Copy-ready Docker template for a React frontend, FastAPI API, MongoDB, Redis, and an RQ worker. Development, staging, and production share one Compose file and differ only in their override files. You need Docker Compose v2 and Make. Node and Python stay inside the images.

## Start

```bash
make dev
```

Open http://localhost:5173. The page loads `/api/health` and can enqueue a sample job. The API is also published at http://localhost:8000/api/health. MongoDB is on port 27017 and Redis is on port 6379, with no passwords.

Stop it with `make down`.

## Commands

`ENV` defaults to `development`. Pass `ENV=staging` or `ENV=production` to target another environment. `make dev`, `make staging`, and `make prod` set that for you and start the stack.

| Command | What it does |
| --- | --- |
| `make dev` | Development: Vite and Uvicorn reload, database ports published |
| `make staging` | Staging images behind nginx on port 8080 |
| `make prod` | Production images behind nginx on port 80 |
| `make up` | Build and start the selected environment |
| `make down` | Stop the selected environment |
| `make build` | Build images |
| `make restart` | Restart containers. Use this after worker code changes in development |
| `make ps` | Container status |
| `make logs` | Follow every service |
| `make logs-api` | Follow the API |
| `make logs-worker` | Follow the worker |
| `make logs-frontend` | Follow the frontend |
| `make shell-api` | Shell in the API container |
| `make shell-worker` | Shell in the worker container |
| `make shell-frontend` | Shell in the frontend container |
| `make config` | Print the merged Compose file |
| `make clean` | Stop containers and delete that environment's volumes |

`make up ENV=staging` is the same as `make staging`. Any other `ENV` value fails before Docker runs.

## What changes per environment

| | Development | Staging | Production |
| --- | --- | --- | --- |
| Frontend | Vite on port 5173, source mounted | Built files served by nginx, internal only | Same as staging |
| API | Uvicorn `--reload` on port 8000 | One process, internal only | `WEB_CONCURRENCY` workers (default 4) |
| Worker | One process, source mounted | One process | Two replicas |
| Data stores | No auth, ports published | Username and password, internal only | Same, plus Redis AOF |
| Public entry | Frontend and API ports | nginx on port 8080 | nginx on port 80 |
| Restart | No | `unless-stopped` | `always`, plus memory limits and log rotation |

Redis database 0 is the RQ queue. Database 1 is the cache. Each environment has its own Compose project name, so the volumes do not overlap:

- development: `quicksetup-dev`
- staging: `quicksetup-staging`
- production: `quicksetup-prod`

Staging: http://localhost:8080  
Production: http://localhost (port 80)

nginx sends `/api/` to the API and `/` to the frontend. The browser keeps calling `/api` in every environment.

## Use this for a new project

1. Copy this directory.
2. Change `COMPOSE_PROJECT_NAME` in [env/development.env](env/development.env), [env/staging.env](env/staging.env), and [env/production.env](env/production.env). Image names are derived from it.
3. Replace every `change-me` password in the staging and production env files, and set `CORS_ORIGINS` to the real public origin.
4. MongoDB stores the root password only when its volume is created. After a password change, run `make clean ENV=staging` or `make clean ENV=production` before starting again.
5. For production TLS, put `fullchain.pem` and `privkey.pem` in `nginx/certs`, uncomment the 443 server in [nginx/production.conf](nginx/production.conf), and publish `443:443` on the proxy service.

The env files in this repo are templates. Do not put real production secrets in them.

## Where to add code

- API routes: [backend/app/routes](backend/app/routes)
- Settings: [backend/app/config.py](backend/app/config.py) reads environment variables
- Worker tasks: [backend/app/tasks.py](backend/app/tasks.py). The worker command is `rq worker --url $REDIS_URL default`. In development the API reloads on save; restart the worker with `make restart` after task changes.
- React UI: [frontend/src](frontend/src)

Add a Python package to [backend/requirements.txt](backend/requirements.txt), then run `make build`. Add an npm package by rebuilding the frontend image the same way. The development frontend keeps `node_modules` in a Docker volume, so a new dependency also needs `make build` (and `make clean` if that volume is stale).
