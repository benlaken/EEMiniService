#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        exec python python_app/main.py
        ;;
    test)
        echo "Running Tests"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        exec py.test -v
        ;;
    production)
        echo "Running Production Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        #exec gunicorn -w 2 main:app
        exec gunicorn -c gunicorn.py main:app
        ;;
    *)
        exec "$@"
esac
