#!/bin/zsh
BUILD_PATH="/Users/marc/repos/m2ag-thing/m2ag-things/build"
gsutil cp -r "$BUILD_PATH/$1.json" gs://m2ag-things-dev
gsutil -m setmeta -h "Content-Type:application/json" \
  -h "Cache-Control:public, max-age=30" \
  -h "Content-Disposition" gs://m2ag-things-dev/$1.json
