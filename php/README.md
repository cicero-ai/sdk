
# Cicero SDK

An easy to utilize SDK for all products produced via the Cicero project at https://cicero.sh/, such as the Sophia NLU Engine.  This 
SDK allows for easily integration and communication with the localhost RPC server, along with tools to parse and handle user input appropriately.

## Installation

Install via Composer with:

> `composer require aquila/cicero-sdk`


## Basic Usage

~~~php

use Aquila\SDK\Sophia\Sophia;

// Start Sophia
$nlu = new Sophia();

// Tokenize
$output = $nlu->tokenize("Some example text to parse through the tokenizer.");
foreach ($output['tokens'] as $token) {
    echo $token['word'] . ', id: ' . $token['index'] . ', pos: ' . $token['pos'] . "\n";
}

// Interpret
$res = $nlu->interpret("This function parses user input into phrases with the verb and noun clauses fully broken down and easily usable.");
foreach ($res['phrases'] as $phrase) {
    print_r($phrase);
}

// Get words
$res = $nlu->getWord('lawn');
print_r($res);

// Get token
$res = $nlu->getToken(58221);
print_r($res);

// Get category
$cat = $nlu->getCategory('verbs/action/travel/depart');
print_r($cat);
~~~


## Map Verb Categories to Functions

You can map parent categories to functions that automatically execute whenever a word within that category or its subcategories is detected. This enables you to seamlessly trigger functions based on matched meanings, simplifying the process by focusing on categories rather than individual words.

~~~php

use Aquila\SDK\Sophia\{Sophia, Router};

$nlu = new Sophia();
$router = new Router();

// Route verb category to the vacation() function
$router->add('verbs/action/travel/depart', "\\vacation");

// Trigger that function
$nlu->route($router, "I want to take off to Thailand and have some fun");

function vacation(int $verb_position, int $phrase_num, array $phrase, array $output) { 
    foreach ($phrase['nouns'] as $noun) {
        $token = $output['mwe'][$noun['head']];
            echo "Looks like we're vacationing in " . $token['word'] . "\n";
    }
}
~~~


## Contact

For all questions, feedback and inquiries please visit: [https://cicero.sh/](https://cicero.sh/).


