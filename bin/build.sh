#!/bin/bash

set -e # exit on first error

TARGET=$1

BIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT=`cd "$BIN/.."; pwd`


if [[ $TARGET = "osx" ]]; then

	pyinstaller --onedir --windowed --noconfirm main.spec
	codesign -s "Developer ID Application: Patrick Stinson (8KJB799CU7)" dist/PKTrader.app
	open ./dist

elif [[ $TARGET == "clean" ]]; then

	echo "CLEAN"
	rm -rf ./build ./dist

fi
