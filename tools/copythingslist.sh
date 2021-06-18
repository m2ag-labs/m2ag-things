#!/bin/zsh
gsutil cp -r "/Users/marc/repos/m2ag-thing/m2ag-things/things/thingslist.json" gs://m2ag-things-dev
gsutil -m setmeta -h "Content-Type:application/json" \
  -h "Cache-Control:public, max-age=30" \
  -h "Content-Disposition" gs://m2ag-things-dev/thingslist.json
