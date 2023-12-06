<?php

use Tester\Assert;

require_once __DIR__ . "/../vendor/autoload.php";

$rows = file(__DIR__ . "/input", FILE_IGNORE_NEW_LINES);
$exampleRows = file(__DIR__ . "/example-input", FILE_IGNORE_NEW_LINES);

$grid = array_map('str_split', $rows);
$exampleGrid = array_map('str_split', $exampleRows);

Assert::same(['4', '6', '7', '.', '.', '1', '1', '4', '.', '.'], $exampleGrid[0]);

function getParts(array $grid): array
{
    $symbolPositions = [];
    foreach ($grid as $y => $row) {
        foreach ($row as $x => $col) {
            if (preg_match('/[^\d.]/', $col)) {
                $symbolPositions[] = [$y, $x];
            }
        }
    }

    // Check all around symbol for a digit
    $parts = [];
    foreach ($symbolPositions as $symbolPosition) {
        $y = $symbolPosition[0];
        $x = $symbolPosition[1];

        // Scan immediate surroundings
        $surroundings = [
            [$y-1, $x],
            [$y+1, $x],
            [$y, $x-1],
            [$y, $x+1],
            [$y-1, $x-1],
            [$y-1, $x+1],
            [$y+1, $x-1],
            [$y+1, $x+1],
        ];

        $skip = [];

        foreach ($surroundings as $key => $surrounding) {
            if (in_array($key, $skip)) {
                continue;
            }

            $y = $surrounding[0];
            $x = $surrounding[1];

            if (isset($grid[$y][$x]) && is_numeric($grid[$y][$x])) {
                $partNumberArray = [$grid[$y][$x]];

                // Scan left and right of the digit
                for ($i = $x-1; $i >= 0; $i--) {
                    if (! is_numeric($grid[$y][$i])) {
                        break;
                    }

                    // Skip this position in the surroundings
                    foreach ($surroundings as $key2 => $surrounding2) {
                        $ys = $surrounding2[0];
                        $xs = $surrounding2[1];

                        if ($ys === $y && $xs === $i) {
                            $skip[] = $key2;
                        }
                    }
                    array_unshift($partNumberArray, $grid[$y][$i]);
                }

                for ($i = $x+1; $i < count($grid[$y]); $i++) {
                    if (! is_numeric($grid[$y][$i])) {
                        break;
                    }

                    // Skip this position in the surroundings
                    foreach ($surroundings as $key2 => $surrounding2) {
                        $ys = $surrounding2[0];
                        $xs = $surrounding2[1];

                        if ($ys === $y && $xs === $i) {
                            $skip[] = $key2;
                        }
                    }
                    $partNumberArray[] = $grid[$y][$i];
                }

                $partNumber = implode('', $partNumberArray);
                $parts[] = $partNumber;
            }
        }

    }

    $parts = array_map('intval', $parts);
    sort($parts);
    return $parts;
}

Assert::same([
    35,
    467,
    592,
    598,
    617,
    633,
    664,
    755,
], getParts($exampleGrid));

Assert::truthy(preg_match('/[^\d.]/', '#'));
Assert::truthy(preg_match('/[^\d.]/', '='));
Assert::truthy(preg_match('/[^\d.]/', '-'));
Assert::truthy(preg_match('/[^\d.]/', '+'));
Assert::truthy(preg_match('/[^\d.]/', '@'));
Assert::truthy(preg_match('/[^\d.]/', '%'));
Assert::truthy(preg_match('/[^\d.]/', '$'));
Assert::truthy(preg_match('/[^\d.]/', '/'));

Assert::falsey(preg_match('/[^\d.]/', '.'));

$examplePartsSum = array_sum(getParts($exampleGrid));

Assert::same(4361, $examplePartsSum);

//var_dump(getParts($grid));

$partsSum = array_sum(getParts($grid));

echo "Answer (part 1): $partsSum\n";

function getGearRatios(array $grid): array
{
    $symbolPositions = [];
    foreach ($grid as $y => $row) {
        foreach ($row as $x => $col) {
            if (preg_match('/\*/', $col)) {
                $symbolPositions[] = [$y, $x];
            }
        }
    }

    // Check all around symbol for a digit
    $gearRatios = [];
    foreach ($symbolPositions as $symbolPosition) {
        $y = $symbolPosition[0];
        $x = $symbolPosition[1];

        // Scan immediate surroundings
        $surroundings = [
            [$y-1, $x],
            [$y+1, $x],
            [$y, $x-1],
            [$y, $x+1],
            [$y-1, $x-1],
            [$y-1, $x+1],
            [$y+1, $x-1],
            [$y+1, $x+1],
        ];

        $skip = [];
        $gears = [];

        foreach ($surroundings as $key => $surrounding) {
            if (in_array($key, $skip)) {
                continue;
            }

            $y = $surrounding[0];
            $x = $surrounding[1];

            if (isset($grid[$y][$x]) && is_numeric($grid[$y][$x])) {
                $partNumberArray = [$grid[$y][$x]];

                // Scan left and right of the digit
                for ($i = $x-1; $i >= 0; $i--) {
                    if (! is_numeric($grid[$y][$i])) {
                        break;
                    }

                    // Skip this position in the surroundings
                    foreach ($surroundings as $key2 => $surrounding2) {
                        $ys = $surrounding2[0];
                        $xs = $surrounding2[1];

                        if ($ys === $y && $xs === $i) {
                            $skip[] = $key2;
                        }
                    }
                    array_unshift($partNumberArray, $grid[$y][$i]);
                }

                for ($i = $x+1; $i < count($grid[$y]); $i++) {
                    if (! is_numeric($grid[$y][$i])) {
                        break;
                    }

                    // Skip this position in the surroundings
                    foreach ($surroundings as $key2 => $surrounding2) {
                        $ys = $surrounding2[0];
                        $xs = $surrounding2[1];

                        if ($ys === $y && $xs === $i) {
                            $skip[] = $key2;
                        }
                    }
                    $partNumberArray[] = $grid[$y][$i];
                }

                $partNumber = implode('', $partNumberArray);
                $gears[] = $partNumber;
            }
        }

        if (count($gears) === 2) {
            $gearRatios[] = $gears[0] * $gears[1];
        }

    }

    $gearRatios = array_map('intval', $gearRatios);
    sort($gearRatios);
    return $gearRatios;
}

$exampleGearRatiosSum = array_sum(getGearRatios($exampleGrid));
Assert::same(467835, $exampleGearRatiosSum);

$gearRatiosSum = array_sum(getGearRatios($grid));
echo "Answer (part 2): $gearRatiosSum\n";
