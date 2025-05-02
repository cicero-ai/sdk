

from typing import Any, Callable, Dict, List, Optional

class Router:
    """Sophia Router for handling verb categories and callbacks."""

    def __init__(self):
        """Initialize the router with an empty routes dictionary."""
        self.routes: Dict[str, List[Callable]] = {}

    def add(self, category_path: str, callback: Callable) -> None:
        """
        Add a new route for a category path with a callback function.

        Args:
            category_path (str): The category path (e.g., verbs/move/pursue).
            callback (Callable): The callback function to handle the route.
        """
        if category_path not in self.routes:
            self.routes[category_path] = []
        self.routes[category_path].append(callback)

    def purge(self) -> None:
        """Clear all routes."""
        self.routes = {}

    def handle_verb(
        self,
        token: Dict[str, Any],
        position: int,
        phrase_num: int,
        phrase: Dict[str, Any],
        output: Dict[str, Any]
    ) -> None:
        """
        Handle a verb by invoking callbacks for matching category paths.

        Args:
            token (Dict[str, Any]): The token data containing categories.
            position (int): The position of the token.
            phrase_num (int): The phrase number.
            phrase (Dict[str, Any]): The phrase data.
            output (Dict[str, Any]): The full output from the RPC server.
        """
        # Go through categories
        for chk_path in token["categories"]:
            callables = self._check_category(chk_path)
            if not callables:
                continue

            # Call each callback
            for func in callables:
                func(position, phrase_num, phrase, output)

    def _check_category(self, chk_path: str) -> Optional[List[Callable]]:
        """
        Check if a category path matches any registered routes.

        Args:
            chk_path (str): The category path to check.

        Returns:
            Optional[List[Callable]]: List of matching callbacks, or None if no matches.
        """
        callables = []

        for cat_path, funcs in self.routes.items():
            if chk_path.startswith(cat_path):
                callables.extend(funcs)

        return callables if callables else None



