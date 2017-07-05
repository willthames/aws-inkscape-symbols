#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "Usage: $0 AWS-icon-zip-file"
  exit 1
fi

zipfile=$1

rm -rf target build
mkdir target build

tempdir=`mktemp -d`
unzip -q $zipfile "*.svg" -d $tempdir
rsync -av $tempdir/AWS*/ build --exclude GRAYSCALE/* --exclude __MACOSX
rm -rf $tempdir

for dir in build/*; do
  python dir_to_svg.py "$dir" target
done
