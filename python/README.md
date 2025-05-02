
Below is a rewritten version of the provided PHP README for the Cicero SDK, tailored for the Python implementation of the cicero-sdk. The content is adapted to reflect Python conventions, package installation via pip, and the previously ported classes (RpcClient, Sophia, Router). The structure and examples are updated to match the Python SDK’s functionality, incorporating the improved description for mapping verb categories as requested. The README is designed to be placed in cicero-sdk-repo/python/README.md.
# Cicero SDK (Python)

A user-friendly SDK for interacting with Cicero project products, such as the Sophia NLU Engine, available at https://cicero.sh/. This SDK simplifies integration with the localhost RPC server and provides tools to parse and process user input effectively.

## Installation

Install the SDK via pip:


    `pip install cicero-sdk`


## Basic Usage

The following example demonstrates how to use the Sophia class to tokenize, interpret, and query data from the Cicero RPC server.

~~~python
from cicero_sdk import Sophia

# Initialize Sophia
nlu = Sophia()

# Tokenize
output = nlu.tokenize("Some example text to parse through the tokenizer.")
for token in output["tokens"]:
    print(f"{token['word']}, id: {token['index']}, pos: {token['pos']}")

# Interpret
res = nlu.interpret("This function parses user input into phrases with the verb and noun clauses fully broken down and easily usable.")
for phrase in res["phrases"]:
    print(phrase)

# Get words
res = nlu.get_word("lawn")
print(res)

# Get token
res = nlu.get_token(58221)
print(res)

# Get category
cat = nlu.get_category("verbs/action/travel/depart")
print(cat)
~~~

## Map Verb Categories to Functions

You can map parent categories to functions that automatically execute whenever a word within that category or its subcategories is detected. This enables you to seamlessly trigger functions based on matched meanings, simplifying the process by focusing on categories rather than individual words.

~~~python

from cicero_sdk import Sophia, Router

# Initialize Sophia and Router
nlu = Sophia()
router = Router()

# Define a callback function for vacation-related verbs
def vacation(verb_position: int, phrase_num: int, phrase: dict, output: dict) -> None:
    for noun in phrase["nouns"]:
        token = output["mwe"][noun["head"]]
        print(f"Looks like we're vacationing in {token['word']}")

# Route verb category to the vacation function
router.add("verbs/action/travel/depart", vacation)

# Trigger the function
nlu.route(router, "I want to take off to Thailand and have some fun")
~~~

## Contact

For questions, feedback, or inquiries, please visit: https://cicero.sh/.


