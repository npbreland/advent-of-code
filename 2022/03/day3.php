<?php

$lines = file('input', FILE_IGNORE_NEW_LINES);

/**
 * Returns an integer value for a given item character following this pattern:
 * a-z: 1-26
 * A-Z: 27-52
 *
 * Does this by taking the ASCII value and subtracting a correction. Correction
 * is different for the lowercase values than for the uppecase values due to
 * their positions in the ASCII table.
 *
 * @param string $item_char Must be single Engish alphabetic letter
 *
 * @return int
 */
function getItemPriority($item_char)
{
    if (strtoupper($item_char) === $item_char) {
        return ord($item_char) - 38;
    } else {
        return ord($item_char) - 96;
    }
}

/**
 * Returns item character that exists in all strings. Assumes
 * that there will only be one (per problem statement).
 *
 * @param array $aos array of strings
 *
 * @return string item char found in both strings
 */
function getCommonItem($aos)
{
    $char_arrs = array_map(function ($str) {
        return str_split($str);
    }, $aos);

    $arr1 = $char_arrs[0];
    $rest = array_slice($char_arrs, 1);

    foreach ($arr1 as $arr1_char) {
        foreach ($rest as $arr2) {
            if (array_search($arr1_char, $arr2) === false) {
                continue 2;
            }
        }
        return $arr1_char;
    }
}

// Part 1
$sum_misplaced = array_reduce($lines, function ($acc, $line) {
    $half = strlen($line) / 2;
    $c1 = substr($line, 0, $half);
    $c2 = substr($line, $half);

    return $acc += getItemPriority(getCommonItem([$c1, $c2]));
});

echo <<<MSG
Part 1. Sum of the priorities of misplaced items: $sum_misplaced 
MSG;
echo PHP_EOL;

// Part 2
$groups = array_chunk($lines, 3);
$sum_badges = array_reduce($groups, function ($acc, $group) {
    return $acc += getItemPriority(getCommonItem($group));
});

echo <<<MSG
Part 2. Sum of the priorities of group badges: $sum_badges 
MSG;
echo PHP_EOL;
