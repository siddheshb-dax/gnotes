#!/bin/bash

uv run celery -A config worker --loglevel=info
