import test from './furcifer.mjs';
import languagePluginLoader from './pyodide/pyodide.mjs';

languagePluginLoader().then(module => {
  self.loaded = test(module);
})