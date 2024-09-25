#!/usr/bin/env zsh

#
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
#
source /home/AsgerJon/.zshrc
,mamba

mamba activate ezside_env

# shellcheck disable=SC2155
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
python -m unittest discover -s tests



