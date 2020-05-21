import json
import os

config_file = open('furcifer.config.json')

config_json = json.load(config_file)

base_path = './example'

base_command = f'emcc furcifer.cpp -o {base_path}/furcifer.mjs --pre-js pre-code.js --post-js post-code.js -s NO_EXIT_RUNTIME=0 -s MODULARIZE=1'

def get_path(package_name):
  global base_path
  return f'{base_path}/{package_name}@lib/python3.7/site-packages/{package_name}'

if 'modules' in config_json:
  modules = config_json['modules']
  base_command += ' --preload-file'
  for module in modules:
    base_command += ' ' + get_path(module)

os.system(base_command)