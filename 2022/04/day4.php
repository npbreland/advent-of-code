<?php

$lines = file('input', FILE_IGNORE_NEW_LINES);

$pairs = array_map(function ($line) {
    return explode(",", $line);
}, $lines);

$pairs = array_map(function ($pair) {
    return [ explode("-", $pair[0]), explode("-", $pair[1]) ];
}, $pairs);

$fully_contained_pairs = array_filter($pairs, function ($pair) {
    return ($pair[0][0] <= $pair[1][0] && $pair[0][1] >= $pair[1][1])
        ||($pair[1][0] <= $pair[0][0] && $pair[1][1] >= $pair[0][1]);
});

$overlapping_pairs = array_filter($pairs, function ($pair) {
    return $pair[0][0] <= $pair[1][1] && $pair[0][1] >= $pair[1][0];
});

$fcp_ct = count($fully_contained_pairs);
$overlap_ct = count($overlapping_pairs);

echo <<<MSG
Part 1. Pairs in which one is fully contained by the other: $fcp_ct
MSG;
echo PHP_EOL;

echo <<<MSG
Part 2. Pairs in which one overlaps the other: $overlap_ct
MSG;
echo PHP_EOL;
