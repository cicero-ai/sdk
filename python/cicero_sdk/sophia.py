
from typing import Any, Dict, List
from .rpc_client import RpcClient
from .router import Router  # Placeholder; replace with actual Router import when available

class Sophia:
    """Sophia class for interacting with Cicero RPC server."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 7513,
        username: str = "sophia",
        password: str = "sophia",
    ):
        """
        Initialize Sophia client.

        Args:
            host (str): The RPC server host. Defaults to "127.0.0.1".
            port (int): The RPC server port. Defaults to 7513.
            username (str): The RPC server username. Defaults to "sophia".
            password (str): The RPC server password. Defaults to "sophia".
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def tokenize(self, input: str) -> List[Any]:
        """
        Tokenize the input string.

        Args:
            input (str): The input string to tokenize.

        Returns:
            List[Any]: The tokenized result from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "tokenize", [input])

    def interpret(self, input: str) -> Dict[str, Any]:
        """
        Interpret the input string.

        Args:
            input (str): The input string to interpret.

        Returns:
            Dict[str, Any]: The interpreted result from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "interpret", [input])

    def run_selector(self, selector_alias: str, user_input: str) -> List[Any]:
        """
        Run a selector with the given alias and user input.

        Args:
            selector_alias (str): The alias of the selector.
            user_input (str): The user input to process.

        Returns:
            List[Any]: The result from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "run-selector", [selector_alias, user_input])

    def get_token(self, index: int) -> List[Any]:
        """
        Get a token by index.

        Args:
            index (int): The index of the token.

        Returns:
            List[Any]: The token data from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "get-token", [str(index)])

    def get_word(self, word: str) -> List[Any]:
        """
        Get data for a specific word.

        Args:
            word (str): The word to query.

        Returns:
            List[Any]: The word data from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "get-word", [word])

    def get_category(self, category_path: str) -> List[Any]:
        """
        Get data for a category by its full path.

        Args:
            category_path (str): The full category path (e.g., verbs/move/pursue).

        Returns:
            List[Any]: The category data from the RPC server.
        """
        rpc = RpcClient()
        return rpc.send(self._get_url(), "get-category", [category_path])

    def route(self, router: Router, input: str) -> None:
        """
        Handle user input via the router.

        Args:
            router (Router): The router instance to handle verbs and modifiers.
            input (str): The input string to process.
        """
        # Interpret the input
        res = self.interpret(input)

        # Iterate through phrases
        phrase_num = 0
        for phrase in res["phrases"]:
            # Check verbs
            for verb in phrase["verbs"]:
                token = res["mwe"][verb["head"]]
                router.handle_verb(token, verb["head"], phrase_num, phrase, res)

                # Siblings
                for sibling in verb["siblings"]:
                    token = res["mwe"][sibling["position"]]
                    router.handle_verb(token, sibling["position"], phrase_num, phrase, res)

                # Modifiers
                for modifier in verb["modifiers"]:
                    token = res["mwe"][modifier["position"]]
                    router.handle_verb(token, modifier["position"], phrase_num, phrase, res)

            phrase_num += 1

    def _get_url(self) -> str:
        """
        Construct the RPC server URL with authentication.

        Returns:
            str: The formatted URL (e.g., http://username:password@host:port/).
        """
        return f"http://{self.username}:{self.password}@{self.host}:{self.port}/"



