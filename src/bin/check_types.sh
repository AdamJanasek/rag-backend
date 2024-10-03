#!/usr/bin/env sh

set -o errexit
set -o nounset

pyclean () {
  find . | grep -E '(__pycache__|\.py[cod]$)' | xargs rm -rf
}

run_check () {
  echo mypy...
  mypy ./ --install-types --non-interactive --explicit-package-bases --config-file setup.cfg
}

pyclean

trap pyclean EXIT INT TERM

run_check
