<?php

define('SAND_SOURCE_X', 500);
define('SAND_SOURCE_Y', 0);

$lines = file('input', FILE_IGNORE_NEW_LINES);

// Parse input where each pair of numbers are vertices on a line segment
$pointGroups = [];
foreach ($lines as $line) {
    $matches = [];
    preg_match_all('/\d+,\d+/', $line, $matches);
    $pointGroups[] = array_map(function ($match) {
        return array_map('intval', explode(',', $match));
    }, $matches[0]);
}

// Fill in grid using the line segments bormed by the point groups
// We use a hash table for easy lookup later based on the x,y coordinates
function buildGrid($pointGroups)
{
    $lowestY = PHP_INT_MIN; // Keep track of the lowest y value
    foreach ($pointGroups as $group) {
        for ($i = 1; $i < count($group); $i++) {
            $point = $group[$i];
            $prevPoint = $group[$i - 1];

            $x1 = $prevPoint[0];
            $y1 = $prevPoint[1];
            $x2 = $point[0];
            $y2 = $point[1];

            // Get all integer points on the line segment
            if ($x1 === $x2) {
                $yMin = min($y1, $y2);
                $yMax = max($y1, $y2);
                for ($y = $yMin; $y <= $yMax; $y++) {
                    $grid[$x1][$y] = true;
                    if ($y > $lowestY) {
                        $lowestY = $y;
                    }
                }
            } elseif ($y1 === $y2) {
                $xMin = min($x1, $x2);
                $xMax = max($x1, $x2);
                for ($x = $xMin; $x <= $xMax; $x++) {
                    $grid[$x][$y1] = true;
                    if ($y1 > $lowestY) {
                        $lowestY = $y1;
                    }
                }
            }
        }
    }

    return [
        'grid' => $grid,
        'lowestY' => $lowestY,
    ];
}

$gridResult = buildGrid($pointGroups);
$grid = $gridResult['grid'];
$lowestY = $gridResult['lowestY'];
$grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
$grainsAtRest = 0;

while ($grain[1] < $lowestY) {
    $down = [$grain[0], $grain[1] + 1];
    $downLeft = [$grain[0] - 1, $grain[1] + 1];
    $downRight = [$grain[0] + 1, $grain[1] + 1];
    if (!isset($grid[$down[0]][$down[1]])) {
        $grain = $down;
    } elseif (!isset($grid[$downLeft[0]][$downLeft[1]])) {
        $grain = $downLeft;
    } elseif (!isset($grid[$downRight[0]][$downRight[1]])) {
        $grain = $downRight;
    } else {
        /* Grain can't move. Stays in place, so we put it in the grid and start
         * over with a new grain */
        $grid[$grain[0]][$grain[1]] = true;
        $grainsAtRest++;
        $grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
    }
}

echo "Part 1. Grains at rest: $grainsAtRest" . PHP_EOL;

// Part 2
$lowestY = $lowestY + 2;
$grainsAtRest = 0;

$gridResult = buildGrid($pointGroups);
$grid = $gridResult['grid'];

$grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
while (!isset($grid[SAND_SOURCE_X][SAND_SOURCE_Y])) {
    if ($grain[1] + 1 === $lowestY) {
        /* Grain can't move. Stays in place, so we put it in the grid and start
         * over with a new grain */
        $grid[$grain[0]][$grain[1]] = true;
        $grainsAtRest++;
        $grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
        continue;
    }

    $down = [$grain[0], $grain[1] + 1];
    $downLeft = [$grain[0] - 1, $grain[1] + 1];
    $downRight = [$grain[0] + 1, $grain[1] + 1];
    if (!isset($grid[$down[0]][$down[1]]) && $down[1]) {
        $grain = $down;
    } elseif (!isset($grid[$downLeft[0]][$downLeft[1]])) {
        $grain = $downLeft;
    } elseif (!isset($grid[$downRight[0]][$downRight[1]])) {
        $grain = $downRight;
    } else {
        /* Grain can't move. Stays in place, so we put it in the grid and start
         * over with a new grain */
        $grid[$grain[0]][$grain[1]] = true;
        $grainsAtRest++;
        $grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
    }
}

echo "Part 2. Grains at rest: $grainsAtRest" . PHP_EOL;
