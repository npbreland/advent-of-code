<?php

$instructions = file("input", FILE_IGNORE_NEW_LINES);

define('ROW_LENGTH', 40);

$cycle = 0;
$x = 1;

$sum_signals = 0;

$CRT_display = '';

function advanceCycle(int $num = 1)
{
    global $cycle, $x, $sum_signals, $CRT_display;

    for ($i = 0; $i < $num; $i++) {
        $pixel = $cycle % ROW_LENGTH;
        drawPixel($pixel);

        $cycle++;


        if (in_array($cycle, [20, 60, 100, 140, 180, 220])) {
            $signal_strength = getSignalStrength();
            $sum_signals += $signal_strength;
            // echo "Cycle $cycle: X = $x, $signal_strength = $signal_strength" . PHP_EOL;
        }

        // echo "Cycle $cycle: $x" . PHP_EOL;
        if ($cycle % 40 === 0) {
            $CRT_display .= PHP_EOL;
        }
    }
}

function drawPixel($pixel)
{
    global $x, $CRT_display;
    $CRT_display .= $pixel > $x - 2 && $pixel < $x + 2 ? "#" : ".";
}

function doNoop()
{
    advanceCycle();
}

function doAddX($value)
{
    global $x;
    advanceCycle(2);
    $x += $value;
}

function getSignalStrength()
{
    global $cycle, $x;
    return $cycle * $x;
}

// echo "Starting X: $x" . PHP_EOL;

foreach ($instructions as $line) {
    $instruction = substr($line, 0, 4);

    if ($instruction === "noop") {
        doNoop();
    } elseif ($instruction === "addx") {
        $value = intval(substr($line, 4));
        doAddX($value);
    }
}

// echo "Final X: $x" . PHP_EOL;
echo "Part 1. Sum signals: $sum_signals" . PHP_EOL;
echo "Part 2." . PHP_EOL;
echo $CRT_display;
