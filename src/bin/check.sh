#!/usr/bin/env sh

set -o errexit
set -o nounset

pyclean () {
  find . | grep -E '(__pycache__|\.py[cod]$)' | xargs rm -rf
}

run_check () {
  echo flake8...
  flake8 .

  echo xenon...
  xenon --max-absolute A --max-modules A --max-average A src -i 'test*'
}

pyclean

trap pyclean EXIT INT TERM

run_check
