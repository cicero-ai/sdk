
# Cicero SDK (Node.js)

A user-friendly SDK for interacting with Cicero project products, such as the Sophia NLU Engine, available at https://cicero.sh/. This SDK simplifies integration with the localhost RPC server and provides tools to parse and process user input effectively.


## Installation

Install the SDK via npm:

    `npm install cicero-sdk`


## Basic Usage

The following example demonstrates how to use the Sophia class to tokenize, interpret, and query data from the Cicero RPC server. Note that all methods are asynchronous and return Promises.

~~~javascript

import { Sophia } from 'cicero-sdk';

async function main() {
  // Initialize Sophia
  const nlu = new Sophia();

  // Tokenize
  const output = await nlu.tokenize('Some example text to parse through the tokenizer.');
  for (const token of output.tokens) {
    console.log(`${token.word}, id: ${token.index}, pos: ${token.pos}`);
  }

  // Interpret
  const res = await nlu.interpret(
    'This function parses user input into phrases with the verb and noun clauses fully broken down and easily usable.'
  );
  for (const phrase of res.phrases) {
    console.log(phrase);
  }

  // Get words
  const wordRes = await nlu.getWord('lawn');
  console.log(wordRes);

  // Get token
  const tokenRes = await nlu.getToken(58221);
  console.log(tokenRes);

  // Get category
  const cat = await nlu.getCategory('verbs/action/travel/depart');
  console.log(cat);
}

main().catch(console.error);
~~~

## Map Verb Categories to Functions

You can map parent categories to functions that automatically execute whenever a word within that category or its subcategories is detected. This enables you to seamlessly trigger functions based on matched meanings, simplifying the process by focusing on categories rather than individual words.


~~~javascript

import { Sophia, Router } from 'cicero-sdk';

async function main() {
  // Initialize Sophia and Router
  const nlu = new Sophia();
  const router = new Router();

  // Define a callback function for vacation-related verbs
  async function vacation(verbPosition, phraseNum, phrase, output) {
    for (const noun of phrase.nouns) {
      const token = output.mwe[noun.head];
      console.log(`Looks like we're vacationing in ${token.word}`);
    }
  }

  // Route verb category to the vacation function
  router.add('verbs/action/travel/depart', vacation);

  // Trigger the function
  await nlu.route(router, 'I want to take off to Thailand and have some fun');
}

main().catch(console.error);
~~~

## Contact

For questions, feedback, or inquiries, please visit: https://cicero.sh/.


