#!/bin/zsh
typeset -a ACTIVE
ACTIVE=("alert" "bme280" "bme680" "bmp280" "ccs811" "htu21d" "lis3dh" "pigpio"
        "pmsa003i" "raspi" "veml7700")
for ((i = 1; i <= $#ACTIVE; i++)) do
   ./thing_json.py $ACTIVE[i]
   ./copy_set_gcs.sh $ACTIVE[i]
done;
gsutil cp -r "/Users/marc/repos/m2ag-thing/m2ag-things/things/thingslist.json" gs://m2ag-things-dev
gsutil -m setmeta -h "Content-Type:application/json" \
  -h "Cache-Control:public, max-age=30" \
  -h "Content-Disposition" gs://m2ag-things-dev/thingslist.json
