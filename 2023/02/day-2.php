<?php

use Tester\Assert;

require_once __DIR__ . "/../vendor/autoload.php";

$lines = file(__DIR__ . "/input", FILE_IGNORE_NEW_LINES);
$exampleLines = file(__DIR__ . "/example-input", FILE_IGNORE_NEW_LINES);

function parseLine($line)
{
    $game = (int) substr(explode(":", $line)[0], strlen("Game "));
    $sets = array_map(function ($set) {
        $matches = [];

        preg_match("/(\d+) blue/", $set, $matches);
        if (isset($matches[1])) {
            $blue = (int) $matches[1];
        } else {
            $blue = 0;
        }

        preg_match("/(\d+) green/", $set, $matches);
        if (isset($matches[1])) {
            $green = (int) $matches[1];
        } else {
            $green = 0;
        }

        preg_match("/(\d+) red/", $set, $matches);
        if (isset($matches[1])) {
            $red = (int) $matches[1];
        } else {
            $red = 0;
        }

        return [
            'blue' => $blue,
            'green' => $green,
            'red' => $red,
        ];

    }, explode("; ", explode(": ", $line)[1]));


    return [
        'game' => $game,
        'sets' => $sets
    ];
}

Assert::same([
    'game' => 1,
    'sets' => [
        [
            'blue' => 3,
            'green' => 0,
            'red' => 4,
        ],
        [
            'blue' => 6,
            'green' => 2,
            'red' => 1,
        ],
        [
            'blue' => 0,
            'green' => 2,
            'red' => 0,
        ],
    ]
], parseLine("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"));

Assert::same([
    'game' => 2,
    'sets' => [
        [
            'blue' => 1,
            'green' => 2,
            'red' => 0,
        ],
        [
            'blue' => 4,
            'green' => 3,
            'red' => 1,
        ],
        [
            'blue' => 1,
            'green' => 1,
            'red' => 0,
        ],
    ]
], parseLine("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"));


function gameIsPossible($maxCubes, $game)
{
    foreach ($game['sets'] as $set) {
        foreach ($set as $color => $cubes) {
            if ($cubes > $maxCubes[$color]) {
                return false;
            }
        }
    }
    return true;
}


$exampleGames = array_map(function ($line) {
    return parseLine($line);
}, $exampleLines);

$maxCubes = [
    'blue' => 14,
    'green' => 13,
    'red' => 12,
];

Assert::same(true, gameIsPossible($maxCubes, $exampleGames[0]));
Assert::same(true, gameIsPossible($maxCubes, $exampleGames[1]));
Assert::same(false, gameIsPossible($maxCubes, $exampleGames[2]));
Assert::same(false, gameIsPossible($maxCubes, $exampleGames[3]));
Assert::same(true, gameIsPossible($maxCubes, $exampleGames[4]));

function solve($lines): int
{
    $maxCubes = [
        'blue' => 14,
        'green' => 13,
        'red' => 12,
    ];

    $games = array_map(function ($line) {
        return parseLine($line);
    }, $lines);

    $possibleGames = array_filter($games, function ($game) use ($maxCubes) {
        return gameIsPossible($maxCubes, $game);
    });

    return array_reduce($possibleGames, function ($carry, $game) {
        return $carry + $game['game'];
    }, 0);
}

Assert::same(8, solve($exampleLines));

echo "Answer (part 1): " . solve($lines) . "\n";

function maximumCubesInGame($sets)
{
    $maxCubes = [
        'blue' => 0,
        'green' => 0,
        'red' => 0,
    ];

    foreach ($sets as $set) {
        foreach ($set as $color => $cubes) {
            if ($cubes > $maxCubes[$color]) {
                $maxCubes[$color] = $cubes;
            }
        }
    }

    return $maxCubes;
}

Assert::same([
    'blue' => 6,
    'green' => 2,
    'red' => 4,
], maximumCubesInGame($exampleGames[0]['sets']));

Assert::same([
    'blue' => 4,
    'green' => 3,
    'red' => 1,
], maximumCubesInGame($exampleGames[1]['sets']));

function solve2($lines)
{
    $games = array_map(function ($line) {
        return parseLine($line);
    }, $lines);

    return array_reduce($games, function ($carry, $game) {
        $maxCubes = maximumCubesInGame($game['sets']);
        return $carry + $maxCubes['blue'] * $maxCubes['green'] * $maxCubes['red'];
    }, 0);
}

Assert::same(2286, solve2($exampleLines));

echo "Answer (part 2): " . solve2($lines) . "\n";

