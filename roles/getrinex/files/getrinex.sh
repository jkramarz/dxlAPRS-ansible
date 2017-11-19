#!/bin/bash
set -e

WORK_DIR=`mktemp -d`
function cleanup {
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT
cd $WORK_DIR

year=`date +'%Y'`

FILE=`curl -s ftp://cddis.gsfc.nasa.gov/gps/data/daily/$year/brdc/ | awk '/brdc.*n/ {print $9}' | tail -n 1`
wget ftp://cddis.gsfc.nasa.gov/gps/data/daily/$year/brdc/$FILE -O rinex.Z

gzip -d rinex.Z
cp rinex /var/run/rinex
