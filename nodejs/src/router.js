

export class Router {
  constructor() {
    this.routes = new Map();
  }

  /**
   * Add a new route
   * @param {string} categoryPath - The category path
   * @param {Function} callback - The callback function
   */
  add(categoryPath, callback) {
    if (!this.routes.has(categoryPath)) {
      this.routes.set(categoryPath, []);
    }
    this.routes.get(categoryPath).push(callback);
  }

  /**
   * Clear all routes
   */
  purge() {
    this.routes.clear();
  }

  /**
   * Handle a verb
   * @param {Object} token - The token data
   * @param {number} position - The token position
   * @param {number} phraseNum - The phrase number
   * @param {Object} phrase - The phrase data
   * @param {Object} output - The full output
   */
  async handleVerb(token, position, phraseNum, phrase, output) {
    for (const chkPath of token.categories) {
      const callables = this._checkCategory(chkPath);
      if (!callables) continue;

      for (const func of callables) {
        await func(position, phraseNum, phrase, output);
      }
    }
  }

  /**
   * Check category path
   * @param {string} chkPath - The category path to check
   * @returns {Array<Function>|null} Matching callbacks or null
   */
  _checkCategory(chkPath) {
    const callables = [];

    for (const [catPath, funcs] of this.routes) {
      if (chkPath.startsWith(catPath)) {
        callables.push(...funcs);
      }
    }

    return callables.length > 0 ? callables : null;
  }
}



