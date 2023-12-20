#!/usr/bin/env bash

FOLDER=test_quirtylog
COMMAND="python suite.py --test"

echo ">>>>>>>>>>>>"
echo ">>> quirtylog"
echo ">>>>>>>>>>>>"

$COMMAND $FOLDER/test_base.py
$COMMAND $FOLDER/test_singleton.py
$COMMAND $FOLDER/test_sqlite_logger.py
$COMMAND $FOLDER/test_tqdm_logger.py

echo "Done!"
