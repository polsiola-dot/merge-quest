#!/bin/bash
# Regenerates ../scene.rml from the drawing (gen_svg.py) and the motion (build.py).
# Needs: python3 with fonttools + brotli (pip install fonttools brotli) and the Rive CLI.
set -e
cd "$(dirname "$0")"
python3 gen_svg.py
# convert outside the project, so the ids don't depend on the scene already there
tmp=$(mktemp -d)
cp cast.svg "$tmp/" && rive svg "$tmp/cast.svg" --out="$tmp/cast.rml" --artboard=HomeCast --force --quiet
cp "$tmp/cast.rml" cast.rml && rm -rf "$tmp"
python3 build.py
rm -f cast.svg cast.rml   # intermediates: the project reads every .rml in its folder
rive .. --verify
