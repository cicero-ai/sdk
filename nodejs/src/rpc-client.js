import fetch from 'node-fetch';

export class RpcClient {
  /**
   * Send an RPC call
   * @param {string} url - The RPC server URL
   * @param {string} method - The RPC method to call
   * @param {Array} params - Parameters for the RPC method
   * @param {Object} [options] - Additional fetch options (e.g., auth)
   * @returns {Promise<any>} The result from the RPC server
   */
  async send(url, method, params = [], options = {}) {
    // Prepare JSON-RPC request
    const jsonReq = {
      jsonrpc: '2.0',
      id: Math.floor(Math.random() * 90000) + 10000,
      method,
      params,
    };

    // Prepare headers
    const headers = {
      'Content-Type': 'application/json',
    };

    // Add Basic Auth if auth option is provided
    if (options.auth) {
      const { username, password } = options.auth;
      const authString = Buffer.from(`${username}:${password}`).toString('base64');
      headers['Authorization'] = `Basic ${authString}`;
      console.log(`Generated Authorization header: Basic ${authString}`); // Debug
    }

    try {
      // Send HTTP request
      console.log(`Sending request to ${url} with headers:`, headers); // Debug
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(jsonReq),
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(
          `Did not receive valid response from RPC server, got status ${response.status} with body: ${body}`
        );
      }

      const data = await response.json();
      console.log('Response:', data); // Debug

      if (data.error) {
        if (typeof data.error === 'object' && data.error.code && data.error.message) {
          throw new Error(`Received error from RPC server: Code (${data.error.code}) ${data.error.message}`);
        }
        throw new Error(`Received unexpected error from RPC server: ${JSON.stringify(data.error)}`);
      }

      if (!('result' in data)) {
        throw new Error(`Response missing 'result' field: ${JSON.stringify(data)}`);
      }

      return data.result;
    } catch (error) {
      console.error('Full error:', error); // Debug
      throw new Error(`Failed to send request to RPC server: ${error.message}`);
    }
  }
}


