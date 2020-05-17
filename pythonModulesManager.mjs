import { languagePluginLoader } from './pyodide/pyodide.mjs';

class PythonModulesManager {
  baseURL = '';

  addModule(moduleName, files) {
    return new Promise((resolve, reject) => {
      const pyodideLoaded = languagePluginLoader();
      pyodideLoaded.then(() => {
        window.pyodide.loadedPackages[moduleName] = "default channel";
        const addFiles = files.map(file => this.addFile(moduleName, file));
        Promise.all(addFiles).then(() => resolve());
      });
      pyodideLoaded.catch(err => reject(err));
    })
  }

  addFile(moduleName, fileName) {
    return new Promise((resolve, reject) => {
      const request = fetch(`${this.baseURL}/${fileName}`);
      request.then(response => {
        if (response.status === 200) {
          const responseText = response.text();
          responseText.then(code => {
            let path = ('/lib/python3.7/site-packages/' + moduleName + '/' + fileName).split('/');
            let lookup = '';
    
            for (let i in path) {
              if (!path[i]) {
                continue;
              }
    
              lookup += (lookup ? '/' : '') + path[i];
    
              if (parseInt(i) === path.length - 1) {
                window.pyodide._module.FS.writeFile(lookup, code);
                console.debug(`fetched ${lookup}`);
              } else {
                try {
                  window.pyodide._module.FS.lookupPath(lookup);
                } catch {
                  window.pyodide._module.FS.mkdir(lookup);
                  console.debug(`created ${lookup}`);
                }
              }
            }
            resolve();
          });
          responseText.catch(err => reject(err));
        } else {
          reject();
        }
      });
      request.catch(err => reject(err));
    })
  }
}

export const moduleManager = new PythonModulesManager();