#!/usr/bin/env bash
set -euo pipefail

FOLDER=test_quirtylog

echo "##########################################"
echo "### Execute test for quirtylog package ###"
echo "##########################################"

coverage run -a suite.py --test $FOLDER
coverage report -m

echo ""
echo ""
echo "Done!"
