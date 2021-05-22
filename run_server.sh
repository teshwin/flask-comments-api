#!/bin/bash

export FLASK_APP=main.py
# export FLASK_ENV=development
export FLASK_ENV=production
python venv/bin/flask run