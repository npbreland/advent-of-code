<?php

function chunkElvesCalories($lines)
{
    // Chunk calorie counts into one array per elf
    $key = 0;
    $elves_calories = [[]];

    for ($i = 0; $i < count($lines); $i++) {
        if ($lines[$i] === "") {
            // Initialize new elf
            $key++;
            $elves_calories[$key] = [];
        } else {
            $elves_calories[$key][] = $lines[$i];
        }
    }
    return $elves_calories;
}

function getSums($elves_calories)
{
    return array_map(function ($elf_calories) {
        return array_sum($elf_calories);
    }, $elves_calories);
}

$lines = file('input', FILE_IGNORE_NEW_LINES);
$calorie_sums = getSums(chunkElvesCalories($lines));

// Part 1: Get calories of elf with most
echo "Part 1. Calories of elf with most: \t" . max($calorie_sums) . PHP_EOL;

// Part 2: Get total calories of the three elves with the most
sort($calorie_sums);
$total = array_sum(array_slice($calorie_sums, -3, 3));
echo "Part 2. Total calories of top three: \t" . $total  . PHP_EOL;
