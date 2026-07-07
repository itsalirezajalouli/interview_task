#!/bin/bash

set -e

export PYTHONPATH="$(pwd)"

uv pip install -e .

green -vvv evaluation
