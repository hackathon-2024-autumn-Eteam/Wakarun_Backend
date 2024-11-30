FROM nginx:1.27.2-alpine
RUN apk add --update vim bash
COPY ./infra/prod/web/nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY ./static /static
