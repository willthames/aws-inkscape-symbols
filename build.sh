#!/bin/bash
PATH=$PATH:/sbin
set -e

if [ $# -ne 1 ]; then
  echo "Usage: $0 AWS-icon-zip-file"
  exit 1
fi

zipfile=$1

rm -rf target build
mkdir target build

tempdir=`mktemp -d`

bsdtar=`which bsdtar`
if [ -f "$bsdtar" ]; then
  bsdtar -xf $zipfile -s'|[^/]*/||' --include='*.svg' --exclude="._*" -C $tempdir
  rsync -av $tempdir/ build --exclude GRAYSCALE/* --exclude __MACOSX
else
  unzip -q $zipfile "*.svg" -d $tempdir
  rsync -av $tempdir/PNG*/ build --exclude GRAYSCALE/* --exclude __MACOSX
fi

rm -rf $tempdir

for dir in build/*; do
  python dir_to_svg.py "$dir" target
done
