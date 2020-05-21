import json
import os
import sys

def print_err(err):
  print(f'Error: {err}')

def print_help():
  print('\npython furcifer.py <folder_path>')


def compile_wasm(base_path):
  config_file = open(f'{base_path}/furcifer.config.json')

  config_json = json.load(config_file)

  base_command = f'emcc furcifer.cpp -o {base_path}/furcifer.mjs --pre-js pre-code.js --post-js post-code.js -s NO_EXIT_RUNTIME=0 -s MODULARIZE=1'

  def get_path(package_name):
    return f'{base_path}/{package_name}@lib/python3.7/site-packages/{package_name}'

  if 'modules' in config_json:
    modules = config_json['modules']
    base_command += ' --preload-file'
    for module in modules:
      base_command += ' ' + get_path(module)

  os.system(base_command)

if len(sys.argv) != 2:
  print_err("Invalid number of arguments")
  print_help()
else:
  compile_wasm(sys.argv[1])
