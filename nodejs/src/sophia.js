import { RpcClient } from './rpc-client.js';
import { Router } from './router.js';

export class Sophia {
  /**
   * @param {string} host - The RPC server host
   * @param {number} port - The RPC server port
   * @param {string} username - The RPC server username
   * @param {string} password - The RPC server password
   */
  constructor(host = '127.0.0.1', port = 7513, username = 'sophia', password = 'sophia') {
    this.host = host;
    this.port = port;
    this.username = username;
    this.password = password;
  }

  /**
   * Tokenize the input string
   * @param {string} input - The input string
   * @returns {Promise<Array>} The tokenized result
   */
  async tokenize(input) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'tokenize', [input], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Interpret the input string
   * @param {string} input - The input string
   * @returns {Promise<Object>} The interpreted result
   */
  async interpret(input) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'interpret', [input], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Run a selector
   * @param {string} selectorAlias - The selector alias
   * @param {string} userInput - The user input
   * @returns {Promise<Array>} The result
   */
  async runSelector(selectorAlias, userInput) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'run-selector', [selectorAlias, userInput], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Get a token by index
   * @param {number} index - The token index
   * @returns {Promise<Array>} The token data
   */
  async getToken(index) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'get-token', [String(index)], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Get data for a word
   * @param {string} word - The word
   * @returns {Promise<Array>} The word data
   */
  async getWord(word) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'get-word', [word], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Get data for a category
   * @param {string} categoryPath - The full category path (e.g., verbs/move/pursue)
   * @returns {Promise<Array>} The category data
   */
  async getCategory(categoryPath) {
    const rpc = new RpcClient();
    return await rpc.send(this._getUrl(), 'get-category', [categoryPath], {
      auth: { username: this.username, password: this.password },
    });
  }

  /**
   * Handle user input via router
   * @param {Router} router - The router instance
   * @param {string} input - The input string
   */
  async route(router, input) {
    const res = await this.interpret(input);
    let phraseNum = 0;

    for (const phrase of res.phrases) {
      for (const verb of phrase.verbs) {
        const token = res.mwe[verb.head];
        await router.handleVerb(token, verb.head, phraseNum, phrase, res);

        for (const sibling of verb.siblings) {
          const siblingToken = res.mwe[sibling.position];
          await router.handleVerb(siblingToken, sibling.position, phraseNum, phrase, res);
        }

        for (const modifier of verb.modifiers) {
          const modifierToken = res.mwe[modifier.position];
          await router.handleVerb(modifierToken, modifier.position, phraseNum, phrase, res);
        }
      }
      phraseNum++;
    }
  }

  /**
   * Construct the RPC server URL (without credentials)
   * @returns {string} The formatted URL
   */
  _getUrl() {
    return `http://${this.host}:${this.port}/`;
  }
}
