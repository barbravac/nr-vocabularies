#!/bin/bash

cd $(dirname $0)

source .venv/bin/activate

(
  cd nr-vocabularies
  pip install -e '.[tests,elasticsearch7,postgresql]'
  pip uninstall elasticsearch --force
  pip install "elasticsearch<7.14.0"
)
