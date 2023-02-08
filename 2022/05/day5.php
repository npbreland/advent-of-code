<?php

$lines = file("input", FILE_IGNORE_NEW_LINES);

// Determine where the instructions begin
for ($i = 0; $i < count($lines); $i++) {
    if (substr($lines[$i], 0, 4) === "move") {
        $first_ln_instructions = $i;
        break;
    }
}

$instructions = array_slice($lines, $first_ln_instructions);

/* Above this line is the pictorial representation of the stack. Below we build
 * the stack's data structure */
$stacks = [];

// Go backwards because we want lowest to be first in stacks
for ($i = $first_ln_instructions; $i >= 0; $i--) {
    preg_match_all("/[A-Z]/", $lines[$i], $matches, PREG_OFFSET_CAPTURE);

    if (count($matches[0]) === 0) {
        continue;
    }

    $matches = $matches[0];

    foreach ($matches as $match) {
        // Stack for each crate is identified by its offset in each line
        $stacks[$match[1]][] = $match[0];
    }
}

ksort($stacks); // Sort by offset keys
$stacks = array_values($stacks); // No need for offset numbers anymore

// Make instructions machine-readable
$instructions = array_map(function ($ln) {
    preg_match_all("/[0-9]+/", $ln, $matches);

    $num_to_move = $matches[0][0];
    // Subtract by one since $stacks is zero-indexed
    $source = $matches[0][1] - 1;
    $dest = $matches[0][2] - 1;
    return [
        'num' => $num_to_move,
        'source' => $source,
        'dest' => $dest
    ];
}, $instructions);

function cm9000Move($stacks, $instructions)
{
    foreach ($instructions as $ln) {
        for ($i = 0; $i < $ln['num']; $i++) {
            array_push($stacks[$ln['dest']], array_pop($stacks[$ln['source']]));
        }
    }
    return $stacks;
}

function cm9001Move($stacks, $instructions)
{
    foreach ($instructions as $ln) {
        $crates = array_splice($stacks[$ln['source']], -$ln['num']);
        $stacks[$ln['dest']] = array_merge($stacks[$ln['dest']], $crates);
    }

    return $stacks;
}

function topOfStacks($acc, $stack)
{
    return $acc . array_slice($stack, -1)[0];
}

$top9000 = array_reduce(cm9000Move($stacks, $instructions), 'topOfStacks');
$top9001 = array_reduce(cm9001Move($stacks, $instructions), 'topOfStacks');

echo "Part 1. CrateMover 9000, Top of stacks: " . $top9000 . PHP_EOL;
echo "Part 2. CrateMover 9001, Top of stacks: " . $top9001 . PHP_EOL;
