
import json
import random
from typing import Any, Dict, List
import requests
from requests import Request, Response

class RpcClient:
    """RPC Client for making JSON-RPC 2.0 requests."""

    def send(self, url: str, method: str, params: List[Any] = None) -> Any:
        """
        Send an RPC call to the specified URL.

        Args:
            url (str): The RPC server URL.
            method (str): The RPC method to call.
            params (List[Any], optional): Parameters for the RPC method. Defaults to None.

        Returns:
            Any: The result from the RPC server.

        Raises:
            Exception: If the response is invalid or contains an error.
        """
        if params is None:
            params = []

        # Prepare JSON-RPC request
        json_req = {
            "jsonrpc": "2.0",
            "id": random.randint(10000, 99999),
            "method": method,
            "params": params
        }

        # Send HTTP request
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(json_req))
        except requests.RequestException as e:
            raise Exception(f"Failed to send request to RPC server: {str(e)}")

        # Handle response
        if response.status_code != 200:
            raise Exception(
                f"Did not receive valid response from RPC server, got status {response.status_code} with body: {response.text}"
            )

        try:
            vars = response.json()
        except ValueError:
            raise Exception(f"Did not receive valid JSON object from RPC server, instead received: {response.text}")

        if "error" in vars and vars["error"] is not None:
            if isinstance(vars["error"], dict) and "code" in vars["error"] and "message" in vars["error"]:
                error_msg = f"Code ({vars['error']['code']}) {vars['error']['message']}"
            else:
                error_msg = f"Unexpected error format: {vars['error']}"
            raise Exception(f"Received error from RPC server: {error_msg}")

        if "result" not in vars:
            raise Exception(f"Response missing 'result' field: {vars}")

        return vars["result"]


