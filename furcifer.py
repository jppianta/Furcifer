import json
import os
import sys
import pkg_resources
import importlib

loaded_packages = { "jedi", "parso", "pyodide.py", "sitecustomize.py", "six.py" }

def get_module_location(package):
  module_name = list(pkg_resources.get_distribution(package)._get_metadata('top_level.txt'))[0]

  module = importlib.import_module(module_name)

  path = module.__file__

  splitted_path = os.path.split(path)

  if (splitted_path[1] == '__init__.py'):
    splitted_path = os.path.split(splitted_path[0])

  return splitted_path[1]

def print_err(err):
  print(f'Error: {err}')

def print_help():
  print('\npython furcifer.py <folder_path>')

def load_dependencies(base_path):
  global base_command
  pipfile = open(f'{base_path}/Pipfile.lock')

  pipfile_json = json.load(pipfile)

  def get_dependency_path(package_name):
    return f'{base_path}/.venv/Lib/site-packages/{package_name}@lib/python3.7/site-packages/{package_name}'

  if 'default' in pipfile_json:
    dependencies = pipfile_json['default']
    for dependency in dependencies:
      module_name = get_module_location(dependency)
      if module_name not in loaded_packages:
        base_command += ' --preload-file ' + get_dependency_path(module_name)
        loaded_packages.add(module_name)

def load_modules(base_path):
  global base_command
  config_file = open(f'{base_path}/furcifer.config.json')

  config_json = json.load(config_file)


  def get_path(package_name):
    return f'{base_path}/{package_name}@lib/python3.7/site-packages/{package_name}'

  if 'modules' in config_json:
    modules = config_json['modules']
    for module in modules:
      base_command += ' --preload-file ' + get_path(module)

def compile_wasm(base_path):
  load_dependencies(base_path)
  load_modules(base_path)

  os.system(base_command)

if len(sys.argv) != 2:
  print_err("Invalid number of arguments")
  print_help()
else:
  base_command = f'emcc furcifer.cpp -o {sys.argv[1]}/furcifer.mjs --pre-js pre-code.js --post-js post-code.js -s NO_EXIT_RUNTIME=0 -s MODULARIZE=1'
  compile_wasm(sys.argv[1])