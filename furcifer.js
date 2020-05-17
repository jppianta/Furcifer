import { moduleManager } from './pythonModulesManager.mjs';

class Furcifer {
  constructor() {
    this.pythonModulesManager = moduleManager;
  }
}

const furcifer = new Furcifer();

if (typeof self !== 'undefined') {
  window.furcifer = furcifer;
}