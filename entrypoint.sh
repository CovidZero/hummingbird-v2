#!/bin/bash

cd /app/src

waitress-serve --port=5000 --expose-tracebacks main:app