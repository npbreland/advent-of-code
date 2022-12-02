<?php

define("ROCK", [
    "their_shape" => "A",
    "my_shape" => "X", // Part 1
    "score" => 1
]);

define("PAPER", [
    "their_shape" => "B",
    "my_shape" => "Y", // Part 1
    "score" => 2
]);

define("SCISSORS", [
    "their_shape" => "C",
    "my_shape" => "Z", // Part 1
    "score" => 3
]);

define("LOSE", [
    "shape" => "X", // Part 2
    "score" => 0
]);

define("DRAW", [
    "shape" => "Y", // Part 2
    "score" => 3
]);

define("WIN", [
    "shape" => "Z", // Part 2
    "score" => 6
]);

function getMyRoundScorePart1($their_shape, $my_shape)
{
    switch ($my_shape) {
        case ROCK['my_shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return DRAW['score'] + ROCK['score'];
                case PAPER['their_shape']:
                    return LOSE['score'] + ROCK['score'];
                case SCISSORS['their_shape']:
                    return WIN['score'] + ROCK['score'];
            }
            // no break
        case PAPER['my_shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return WIN['score'] + PAPER['score'];
                case PAPER['their_shape']:
                    return DRAW['score'] + PAPER['score'];
                case SCISSORS['their_shape']:
                    return LOSE['score'] + PAPER['score'];
            }
            // no break
        case SCISSORS['my_shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return LOSE['score'] + SCISSORS['score'];
                case PAPER['their_shape']:
                    return WIN['score'] + SCISSORS['score'];
                case SCISSORS['their_shape']:
                    return DRAW['score'] + SCISSORS['score'];
            }
    }
}

function getMyRoundScorePart2($their_shape, $end_shape)
{
    switch ($end_shape) {
        case LOSE['shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return LOSE['score'] + SCISSORS['score'];
                case PAPER['their_shape']:
                    return LOSE['score'] + ROCK['score'];
                case SCISSORS['their_shape']:
                    return LOSE['score'] + PAPER['score'];
            }
            // no break
        case DRAW['shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return DRAW['score'] + ROCK['score'];
                case PAPER['their_shape']:
                    return DRAW['score'] + PAPER['score'];
                case SCISSORS['their_shape']:
                    return DRAW['score'] + SCISSORS['score'];
            }
            // no break
        case WIN['shape']:
            switch ($their_shape) {
                case ROCK['their_shape']:
                    return WIN['score'] + PAPER['score'];
                case PAPER['their_shape']:
                    return WIN['score'] + SCISSORS['score'];
                case SCISSORS['their_shape']:
                    return WIN['score'] + ROCK['score'];
            }
    }
}

$lines = file('input', FILE_IGNORE_NEW_LINES);

$shape_pairs = array_map(function ($line) {
    return [$line[0], $line[2]];
}, $lines);

// Part 1
$total_score = 0;

foreach ($shape_pairs as $pair) {
    $their_shape = $pair[0];
    $my_shape = $pair[1];

    $total_score += getMyRoundScorePart1($their_shape, $my_shape);
}
echo "Part 1. Total score: " . $total_score . PHP_EOL;

// Part 2
$total_score = 0;

foreach ($shape_pairs as $pair) {
    $their_shape = $pair[0];
    $my_shape = $pair[1];

    $total_score += getMyRoundScorePart2($their_shape, $my_shape);
}
echo "Part 2. Total score: " . $total_score . PHP_EOL;
