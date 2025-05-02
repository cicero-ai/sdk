<?php
declare(strict_types=1);

namespace Aquila\SDK;

use Nyholm\Psr7\Request;

/**
 * RPC Client
 */
class RpcClient
{

    /**
     * Send RPC call
     */
    public function send(string $url, string $method, array $params = []):mixed
    {

        // Set request
        $json_req = json_encode([ 
            "jsonrpc" => "2.0",
            'id' => rand(10000, 99999),
            'method' => $method, 
            'params' => $params
        ]);
        $request = new Request('POST', $url, ['Content-type: application/json'], $json_req);

        // Send http request
        $http = new \GuzzleHttp\Client();
        $res = $http->sendRequest($request);
        if ($res->getStatusCode() != 200) {
            throw new \Exception("Did not receive valid response from RPC server, got status " . $res->getStatusCode() . " with body: " . $res->getBody()->getContents());
        } elseif (!$vars = json_decode($res->getBody()->getContents(), true)) {
            throw new \Exception("Did not receive valid JSON object from RPC server, instead received: " . $res->getBody());
        } elseif (isset($vars['error'])) {
            $error_msg = "Code (" . $vars['error']['code'] . ") " . $vars['error']['message'];
            throw new \Exception("Received error from Monero RPC server: $error_msg");
        }

        // Return
        return $vars['result'];
    }

}


