#!/usr/bin/env bash
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

servicedir=$(ls -d build/AWS-Architecture-Service*)
if [ -d "$servicedir/Arch_Developer- Tools" ]; then
  mv "$servicedir/Arch_Developer- Tools" "$servicedir/Arch_Developer-Tools"
fi

for dir in build/AWS-Architecture-Resource*/*; do
  componentname=$(basename $dir | sed 's/^Res_//' | tr 'A-Z_' 'a-z-')
  lightfiles=$dir/Res_48_Light/*.svg
  python files_to_svg.py $componentname target/aws-$componentname-resource-light.svg $lightfiles
  darkfiles=$dir/Res_48_Dark/*.svg
  python files_to_svg.py $componentname-dark target/aws-$componentname-resource-dark.svg $darkfiles
done

for dir in build/AWS-Architecture-Service*/*; do
  componentname=$(basename $dir | sed 's/^Arch_//' | tr 'A-Z_' 'a-z-')
  files=$dir/*48/*.svg
  python files_to_svg.py $componentname target/aws-$componentname-service.svg $files
done

