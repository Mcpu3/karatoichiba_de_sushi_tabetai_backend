#!/bin/bash

echo run main.py
python main.py > main.log &

echo run server.py
python server.py