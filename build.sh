#!/bin/bash

docker build -t pyxapp .
docker run -it --rm -v $PWD/:/app -w /app/src -p 8000:8000 pyxapp pyxel package . launcher.py
mv ./src/src.pyxapp ./out/copilot-shooter.pyxapp
# docker run -it --rm -v $PWD/:/app -p 8000:8000 pyxapp pyxel app2html app.pyxapp
