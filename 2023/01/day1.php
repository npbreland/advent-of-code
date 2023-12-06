<?php

use Tester\Assert;

require_once __DIR__ . "/../vendor/autoload.php";

$lines = file(__DIR__ . "/input", FILE_IGNORE_NEW_LINES);


function getCalibrationValue(string $line): int {
    preg_match_all('/\d/', $line, $matches);

    $firstDigit = $matches[0][0];
    $lastDigit = $matches[0][count($matches[0]) - 1];

    return (int) $firstDigit . $lastDigit;
}

Assert::same(29, getCalibrationValue($lines[0]));
Assert::same(99, getCalibrationValue($lines[1]));
Assert::same(13, getCalibrationValue($lines[6]));

Assert::same(12, getCalibrationValue('1abc2'));
Assert::same(38, getCalibrationValue('pqr3stu8vwx'));
Assert::same(15, getCalibrationValue('a1b2c3d4e5f'));
Assert::same(77, getCalibrationValue('treb7uchet'));

$sum = array_reduce($lines, function ($carry, $line) {
    return $carry + getCalibrationValue($line);
}, 0);

echo "Sum (part 1): $sum\n";

// Part 2

function getCalibrationValue2(string $line): int {
    preg_match_all('/(?=(\d|one|two|three|four|five|six|seven|eight|nine))/', $line, $matches);

    $digitWords = [
        'one' => 1,
        'two' => 2,
        'three' => 3,
        'four' => 4,
        'five' => 5,
        'six' => 6,
        'seven' => 7,
        'eight' => 8,
        'nine' => 9
    ];

    foreach ($matches[1] as $key => $match) {
        if (is_numeric($match)) {
            $matches[1][$key] = $match;
        } else {
            $matches[1][$key] = $digitWords[$match];
        }
    }

    $firstDigit = $matches[1][0];
    $lastDigit = $matches[1][count($matches[1]) - 1];

    return (int) $firstDigit . $lastDigit;
}

Assert::same(29, getCalibrationValue2('two1nine'));
Assert::same(83, getCalibrationValue2('eighttwothree'));
Assert::same(13, getCalibrationValue2('abcone2threexyz'));
Assert::same(24, getCalibrationValue2('xtwone3four'));
Assert::same(42, getCalibrationValue2('4nineeightseven2'));
Assert::same(14, getCalibrationValue2('zoneight234'));
Assert::same(76, getCalibrationValue2('7pqrstsixteen'));
$testLines = file(__DIR__ . "/input-test", FILE_IGNORE_NEW_LINES);
$sumTest = array_reduce($testLines, function ($carry, $line) {
    return $carry + getCalibrationValue2($line);
}, 0);
Assert::same(281, $sumTest);

Assert::same(55, getCalibrationValue2('fivetwofive'));
Assert::same(52, getCalibrationValue2('five42'));
Assert::same(36, getCalibrationValue2('33six'));
Assert::same(53, getCalibrationValue2('5eight8three5lrhdbsnj3lncs'));
Assert::same(78, getCalibrationValue2('kjzqzdv75eightt'));
Assert::same(81, getCalibrationValue2('eight33threeeight3twonepr'), 'eight33threeeight3twonepr');

$sum2 = array_reduce($lines, function ($carry, $line) {
    return $carry + getCalibrationValue2($line);
}, 0);

echo "Sum (part 2): $sum2\n";
