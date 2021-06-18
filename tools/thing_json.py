#!/usr/bin/env python3
import sys
import json

thing_path = '/Users/marc/repos/m2ag-thing/m2ag-things/things'
build_path = '/Users/marc/repos/m2ag-thing/m2ag-things/build'
source_json = f'{thing_path}/thingslist.json'

if len(sys.argv) < 2:
    print('no args')
    sys.exit(2)

config = {'thing': {}, 'helper': ''}
target = sys.argv[1]

try:
    with open(f'{thing_path}/{target}/{target}.json', 'r') as file:
        config['thing'] = file.read().replace('\n', "")
        config['thing'] = json.loads(config['thing'])
except FileNotFoundError:
    print("no thing found")
    sys.exit(2)

try:
    with open(f'{thing_path}/{target}/{target}.py', 'r') as file:
        config['helper'] = file.read()
except FileNotFoundError:
    pass

try:
    with open(f'{build_path}/{target}.json', 'w') as file:
        file.write(json.dumps(config))
        file.close()
except FileExistsError:
    pass

