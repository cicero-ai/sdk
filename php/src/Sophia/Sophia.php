<?php
declare(strict_types=1);

namespace Aquila\SDK\Sophia;

use Aquila\SDK\RpcClient;
use Aquila\SDK\Sophia\Router;

/**
 * Sophia
 */
class Sophia
{

    public function __construct(
        private string $host = '127.0.0.1',
        private int $port = 7513,
        private string $username = 'sophia',
        private string $password = 'sophia'
    ) { 

    }

    /**
     * Tokenize
     */
    public function tokenize(string $input):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'tokenize', [$input]);
        return $res;
    }

    /**
     * Interpret
     */
    public function interpret(string $input):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'interpret', [$input]);
        return $res;
    }

    /**
     * Run selector
     */
    public function runSelector(string $selector_alias, string $user_input):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'run-selector', [$selector_alias, $user_input]);
        return $res;
    }

    /**
     * Get token
     */
    public function getToken(int $index):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'get-token', [(string) $index]);
        return $res;
    }

    /**
     * get word
     */
    public function getWord(string $word):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'get-word', [$word]);
        return $res;
    }

    /**
     * get category
     *
     * @param string $category_path the Full category path (eg. verbs/move/persue)
     */
    public function getCategory(string $category_path):array
    {

        // SEnd RPC
        $rpc = new RpcClient();
        $res = $rpc->send($this->getUrl(), 'get-category', [$category_path]);
        return $res;
    }

    /**
     * Get URL
     */
    private function getUrl():string {
        return 'http://' . $this->username . ':' . $this->password . '@' . $this->host . ':' . $this->port . '/';
    }

    /**
     * Handle user input via router
     */
    public function route(Router $router, string $input):void
    {

        // Interpret
        $res = $this->interpret($input);

        // Iterate through phrases
        $phrase_num=0;
        foreach ($res['phrases'] as $phrase) {

            // Check verbs
            foreach ($phrase['verbs'] as $verb) {
                $token = $res['mwe'][$verb['head']];
                $router->handleVerb($token, $verb['head'], $phrase_num, $phrase, $res);

                // Siblings
                foreach ($verb['siblings'] as $sibling) {
                    $token = $res['mwe'][$sibling['position']];
                    $router->handleVerb($token, $sibling['position'], $phrase_num, $phrase, $res);
                }

            // Modifiers
                foreach ($verb['modifiers'] as $modifier) {
                    $token = $res['mwe'][$modifier['position']];
                    $router->handleVerb($token, $modifier['position'], $phrase_num, $phrase, $res);
                }

            }

            $phrase_num++;
        }

    }

}

