#!/bin/bash
apt-get update && apt-get install -y cmake
pip install --upgrade pip
pip install -r backend/requirements.txt
