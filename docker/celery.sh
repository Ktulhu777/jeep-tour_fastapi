#!/bin/bash

cd src

if [[ "${1}" == "celery" ]]; then
  celery --app=worker.worker.celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=worker.worker.celery flower
  fi
    