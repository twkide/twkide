# twkide

An amazing online IDE inspired by Tung Wei Kuo

https://sites.google.com/site/tungweikuo/

# Development

## twk\_bakend

This is the django project containing most core-logics.

Please run
```bash
export ROCKET_CHAT_PRIVATE_URL=http://localhost:3000
export ROCKET_CHAT_PUBLIC_URL=http://localhost:3000
export ROCKET_CHAT_ADMIN_ACCOUNT=aaav
export ROCKET_CHAT_ADMIN_PASSWORD=123
export TWK_URL=http://localhost:8000
export JUDGE0_API_PRIVATE_URL=http://localhost:3001
export JUDGE0_API_PUBLIC_URL=http://localhost:3001
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

to launch a clean twk\_bakend server.

To add a super user admin account, please run
```bash
python3 manage.py createsuperuser
```

After the superuser is created, student accounts can be created by going to
`localhost:8000/admin/` (suppose you are running the server on port 8000).

## Automatic account generation

To generate 3 account named "stxxxxx": ("xxxxx" means 5 random digits)

```bash
python gen_fixtures.py st 3
./manage.py loaddata output.json
./manage.py shell < set_password.py
```

# Deployment

## Set up rocket chat
1. Follow the official tutorial (maybe https://rocket.chat/docs/installation/docker-containers/ if you want to use docker)
2. Goto: settings -> accounts -> Iframe. Set `Iframe URL` to `http://localhost:8000/login/`, and set `API URL` to `http://localhost:8000/isLogined/` (looks like trailing `/` is important because of CORS protection and 302 temporary moved redirection)
3. Add an user with admin permission, username = `admin`, password = `supersecret`. This user is used to automatically create new accounts for TWK IDE users.

## Set up judge0
1. Follow https://github.com/judge0/api#quick-production-setup

If failed, please try to change db image to `postgres:9.6.5`

Also please change port binding from `3000:3000` to `3001:3000`. (To avoid port number clashing with rocket chat)

# Instructions for Docker setup

Please ensure that your 3000, 3001, and 8000 port are free.

First, change working directory to docker, then

```bash
docker-compose build
docker-compose up
```

To view student account names/passwords and twk ide logs:
```bash
docker logs docker_twk-ide_1
```

To clean up state directories (if permission denied, you may need sudo):
```bash
./cleanup.sh
```

