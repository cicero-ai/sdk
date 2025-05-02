<?php

use Aquila\SDK\Sophia\{Sophia, Router};

require_once('./vendor/autoload.php');


$nlu = new Sophia();
$router = new Router();

$router->add('verbs/action/travel/depart', "\\vacation");
$nlu->route($router, "I want to take off to Thailand and have some fun");
echo "Done\n";

function vacation(int $verb_position, int $phrase_num, array $phrase, array $output) { 
    foreach ($phrase['nouns'] as $noun) {
        $token = $output['mwe'][$noun['head']];
            echo "Looks like we're vacationing in " . $token['word'] . "\n";
    }
}


