<?php

function pairIsInOrder($pair): bool
{
    // Inner function can be inconclusive -- we denote this with null
    $aux = function ($pair) use (&$aux): ?bool {
        $left = $pair[0];
        $right = $pair[1];

        if (is_int($left) && is_int($right)) {
            if ($left < $right) {
                return true;
            } elseif ($left > $right) {
                return false;
            } elseif ($left === $right) {
                return null;
            }
        } elseif (is_array($left) && is_array($right)) {
            foreach ($left as $key => $lv) {
                if (!isset($right[$key])) {
                    // Ran out of keys on the right
                    return false;
                }

                $rv = $right[$key];

                $result = $aux([$lv, $rv]);

                if (is_bool($result)) {
                    return $result;
                }
            }

            // Both ran out at the same time -- inconclusive
            if (count($left) === count($right)) {
                return null;
            }

            // Ran out of elements on the left
            return true;
        } elseif (is_int($left)) {
            $left = [$left];
            return $aux([$left, $right]);
        } elseif (is_int($right)) {
            $right = [$right];
            return $aux([$left, $right]);
        }
    };

    return $aux($pair);
}

$lines = file('input', FILE_IGNORE_NEW_LINES);

$left = [];
$right = [];

foreach ($lines as $key => $line) {
    if ($key % 3 === 0) {
        $left[] = json_decode($line);
    } elseif ($key % 3 === 1) {
        $right[] = json_decode($line);
    }
}

// Zip left and right together
$pairs = array_map(null, $left, $right);

$pairsInOrder = [];

foreach ($pairs as $key => $pair) {
    if (pairIsInOrder($pair)) {
        // Expects starting index to be 1
        $pairsInOrder[] = $key + 1;
    }
}

echo 'Part 1. Sum of pair indices in order: ' . array_sum($pairsInOrder) . PHP_EOL;
