#!/bin/bash

set -e # exit on first error

TARGET=$1


if [[ $TARGET = "osx" ]]; then

	# pyinstaller --onedir --windowed --noconfirm main.spec
	rm -rf ./build ./dist
	pyinstaller --onedir --windowed --noconfirm PKTrader.spec
	codesign --deep -s "Developer ID Application: Patrick Stinson (8KJB799CU7)" dist/PKTrader.app
	open ./dist

elif [[ $TARGET == "clean" ]]; then

	echo "CLEAN"
	rm -rf ./build ./dist

fi
