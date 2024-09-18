#!/usr/bin/env bash

FOLDER=test_quirtylog

echo "##########################################"
echo "### Execute test for quirtylog package ###"
echo "##########################################"

coverage run suite.py --test $FOLDER
coverage report -m

echo "Done!"
