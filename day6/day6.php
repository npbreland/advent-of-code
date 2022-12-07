<?php

/**
 * Get the first marker, defined as the first series of unique characters of
 * the given length
 *
 * @param resource $fp file pointer
 * @param int $len length of marker
 *
 * @return array [
 *  "marker" => string: the marker,
 *  "position" => int: position of last char
 *  ]
 */
function findMarker($fp, $len)
{
    $last = [];

    // Stop when there are no duplicates to remove
    while (count(array_unique($last)) !== $len) {
        $char = fgetc($fp);
        array_push($last, $char);

        // We only look at last $len, so remove the oldest one
        if (count($last) > $len) {
            array_shift($last);
        }
    }

    return [
        'marker' => implode("", $last),
        'position' => ftell($fp)
    ];
}

$fp = fopen('input', 'r');

$p1 = findMarker($fp, 4);
$p2 = findMarker($fp, 14);

echo "Part 1. First start-of-packet marker ends at: " . $p1['position'] . " (". $p1["marker"] . ")" . PHP_EOL;
echo "Part 2. First start-of-message marker ends at: " . $p2['position'] . " (". $p2["marker"] . ")" . PHP_EOL;
