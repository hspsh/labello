export APP_SECRET_KEY=$(openssl rand -hex 16)

env | grep APP_ > .env
