#!/usr/bin/env sh

set -o errexit
set -o nounset

pyclean () {
  find . | grep -E '(__pycache__|\.py[cod]$)' | xargs rm -rf
}

run_check () {
  echo security...
  pip-audit --desc on --ignore-vuln PYSEC-2023-194

  echo bandit...
  bandit -ii -ll -r /app
}

pyclean

trap pyclean EXIT INT TERM

run_check
