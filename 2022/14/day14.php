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

/**
 * Fill in grid using the line segments bormed by the point groups.
 * We use a hash table for easy lookup later based on the x,y coordinates.
 * Returns the grid and the max y (in physical terms, the lowest) value.
 *
 * @param array $pointGroups Groups of x, y coordinates that connect end to end
 *
 * @return array [grid, maxY]
 */
function buildGrid(array $pointGroups): array
{
    $maxY = PHP_INT_MIN; // Keep track of the lowest y value
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
                    if ($y > $maxY) {
                        $maxY = $y;
                    }
                }
            } elseif ($y1 === $y2) {
                $xMin = min($x1, $x2);
                $xMax = max($x1, $x2);
                for ($x = $xMin; $x <= $xMax; $x++) {
                    $grid[$x][$y1] = true;
                    if ($y1 > $maxY) {
                        $maxY = $y1;
                    }
                }
            }
        }
    }

    return [ $grid, $maxY ];
}

// Initialize values
list($grid, $maxY) = buildGrid($pointGroups);
$grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
$grainsAtRest = 0;

function moveGrain($grid, $grain): array
{
    // Possible moves
    $down = [$grain[0], $grain[1] + 1];
    $downLeft = [$grain[0] - 1, $grain[1] + 1];
    $downRight = [$grain[0] + 1, $grain[1] + 1];

    if (!isset($grid[$down[0]][$down[1]])) {
        return [ $down, true ];
    }
    if (!isset($grid[$downLeft[0]][$downLeft[1]])) {
        return [ $downLeft, true ];
    }
    if (!isset($grid[$downRight[0]][$downRight[1]])) {
        return [ $downRight, true ];
    }

    return [ $grain, false ];
}

while ($grain[1] < $maxY) {
    list($grain, $moved) = moveGrain($grid, $grain);
    if ($moved) {
        continue;
    }
    /* Grain can't move. Stays in place, so we put it in the grid and start
     * over with a new grain */
    $grid[$grain[0]][$grain[1]] = true;
    $grainsAtRest++;
    $grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
}

echo "Part 1. Grains at rest: $grainsAtRest" . PHP_EOL;

// Part 2
$maxY = $maxY + 2;
// Refresh values
$grainsAtRest = 0;
list($grid) = buildGrid($pointGroups);
$grain = [SAND_SOURCE_X, SAND_SOURCE_Y];

function moveGrain2($grid, $grain, $maxY)
{
    if ($grain[1] + 1 === $maxY) {
        return [ $grain, false ];
    }

    return moveGrain($grid, $grain);
}

while (!isset($grid[SAND_SOURCE_X][SAND_SOURCE_Y])) {
    list($grain, $moved) = moveGrain2($grid, $grain, $maxY);
    if ($moved) {
        continue;
    }
    $grid[$grain[0]][$grain[1]] = true;
    $grainsAtRest++;
    $grain = [SAND_SOURCE_X, SAND_SOURCE_Y];
}

echo "Part 2. Grains at rest: $grainsAtRest" . PHP_EOL;
