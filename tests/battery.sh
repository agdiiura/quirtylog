#!/usr/bin/env bash
set -euo pipefail

FOLDER=test_quirtylog

echo "##########################################"
echo "### Execute test for quirtylog package ###"
echo "##########################################"

coverage run suite.py --test $FOLDER
coverage report -m

echo ""
echo ""
echo "Done!"
