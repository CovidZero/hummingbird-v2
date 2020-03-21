#!/bin/bash

cd /app/src

gunicorn main:app --bind 0.0.0.0:5000 -w 4 --reload --access-logfile -