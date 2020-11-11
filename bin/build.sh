#!/bin/bash

set -e # exit on first error

TARGET=$1

BIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT=`cd "$BIN/.."; pwd`


if [[ $TARGET = "osx" ]]; then

	pyinstaller --onefile --windowed main.spec

elif [[ $TARGET == "clean" ]]; then

	rm -rf build dist

fi
