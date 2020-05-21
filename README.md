<p align="center">
  <img height='300px' src='./logo.png'>
</p>

Furcifer is a microframework that enables the creation of serverless web apps using Python

## How it works
The configuration of the project is stored in `furcifer.config.json`. This file defines which modules need to be compiled. Furcifer then store all the modules in the Emscripten File System and declares them as python modules for the Pyodide library.