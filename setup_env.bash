#!/usr/bin/env bash
# install depends. quickly skip if not needed
# see Makefile

# python. esp heudiconv which is outdated in debain12 (0.13 v 1.0)
test -d .venv || python3 -m venv .venv
. .venv/bin/activate
[ -z "$(find .venv -iname '*heudiconv*'|sed 1q)" ] &&
   pip install -r requirements.txt

command -v dicom-rewrite-pname || pip install -e .

command -v bids-validator ||
   npm install bids-validator -g

