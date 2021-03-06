#!/bin/bash

pushd "$(dirname $0)"
./run_backup_job.sh
docker run \
  --rm \
  -v fi:/var/www/finem_imperii/prod \
  -v fi_logs:/var/logs -d jardiacaj/finem_imperii \
  -e DJANGO_SETTINGS_MODULE=prod.settings \
  bin/bash \
  "./manage.py pass_turn $1"
popd
