<?php
declare(strict_types=1);

namespace Aquila\SDK\Sophia;

/**
 * Sophia Router
 */
class Router
{

    // Properties
    private array $routes = [];

    /**
     * Add new route
     */
    public function add(string $category_path, callable $callback):void
    {
        $this->routes[$category_path][] = $callback;
    }

    /**
     * Purge
     */
    public function purge():void
    {
        $this->routes = [];
    }

    /**
     * Handle verb
     */
    public function handleVerb(array $token, int $position, int $phrase_num, array $phrase, array $output):void
    {

        // Go through categories
        foreach ($token['categories'] as $chk_path) {
            if (!$callables = $this->checkCategory($chk_path)) {
                continue;
            }

            // Call
            foreach ($callables as $func) {
                call_user_func($func, ...[$position, $phrase_num, $phrase, $output]);
            }
        }

    }

    /**
     * Check category path
     */
    private function checkCategory(string $chk_path):?array
    {
        $callables = [];

        foreach ($this->routes as $cat_path => $func) {
            if (!str_starts_with($chk_path, $cat_path)) { continue; }
            array_push($callables, ...$func);
        }

        if (count($callables) == 0) { return null; }
        return $callables;
    }

}


