#!/usr/bin/env bash

coverage run suite.py --test test_quirtylog/
coverage report -m
coverage html
