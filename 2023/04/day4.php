<?php

use Tester\Assert;

require_once __DIR__ . "/../vendor/autoload.php";

$lines = file(__DIR__ . "/input", FILE_IGNORE_NEW_LINES);
$exampleLines = file(__DIR__ . "/example-input", FILE_IGNORE_NEW_LINES);

function parseCard($line)
{
    $cardNumber = (int) substr(explode(":", $line)[0], strlen("Card "));

    $numbersString = explode(":", $line)[1];

    $winningNumbers = explode(" ", explode("|", $numbersString)[0]);
    $winningNumbers = array_values(array_filter($winningNumbers, function ($number) {
        return $number !== "";
    }));
    $winningNumbers = array_map("intval", $winningNumbers);

    $myNumbers = explode(" ", explode("|", $numbersString)[1]);
    $myNumbers = array_values(array_filter($myNumbers, function ($number) {
        return $number !== "";
    }));
    $myNumbers = array_map("intval", $myNumbers);

    return [
        "cardNumber" => $cardNumber,
        "winningNumbers" => $winningNumbers,
        "myNumbers" => $myNumbers,
    ];
}

function getMyWinningNumbers($card)
{
    $myNumbers = $card["myNumbers"];
    $winningNumbers = $card["winningNumbers"];

    return array_values(array_intersect($myNumbers, $winningNumbers));
}

/* function scoreCard($card) */
/* { */
/*     $myWinningNumbers = getMyWinningNumbers($card); */

/*     if (count($myWinningNumbers) === 0) { */
/*         return 0; */
/*     } */

/*     return 2 ** (count($myWinningNumbers) - 1); */
/* } */

/* function solve($lines) */
/* { */
/*     $cards = array_map("parseCard", $lines); */
/*     $scores = array_map("scoreCard", $cards); */
/*     return array_sum($scores); */
/* } */

/* $cards = array_map("parseCard", $exampleLines); */

/* Assert::same(1, $cards[0]["cardNumber"]); */
/* Assert::same([41, 48, 83, 86, 17], $cards[0]["winningNumbers"]); */
/* Assert::same([83, 86, 6, 31, 17, 9, 48, 53], $cards[0]["myNumbers"]); */
/* Assert::same([83, 86, 17, 48], getMyWinningNumbers($cards[0])); */
/* Assert::same(13, solve($exampleLines)); */


/* echo "Total points (part 1):" . solve($lines) . "\n"; */


Assert::same([11, 12, 13, 14, 15], range(11, 15));

function getNumberOfDescendants($cardsToCheck0, $cards)
{
    $aux = function($cardsToCheck, $numDescendants) use (&$aux, $cards) {

        if (count($cardsToCheck) === 0) {
            return $numDescendants;
        }

        $cardNumber = array_shift($cardsToCheck);
        $card = $cards[$cardNumber - 1];

        $myWinningNumbers = getMyWinningNumbers($card);

        $cardsWonCount = count($myWinningNumbers);

        if ($cardsWonCount > 0) {
            $cardNumbersWon = range($card["cardNumber"] + 1, $card["cardNumber"] + $cardsWonCount);
            $cardsToCheck = array_merge($cardsToCheck, $cardNumbersWon);
        }

        return $aux($cardsToCheck, $numDescendants += $cardsWonCount);
    };

    return $aux($cardsToCheck0, 0);
}

$exampleCards = array_map("parseCard", $exampleLines);

Assert::same(14, getNumberOfDescendants([$exampleCards[0]["cardNumber"]], $exampleCards));
Assert::same(6, getNumberOfDescendants([$exampleCards[1]["cardNumber"]], $exampleCards));
Assert::same(3, getNumberOfDescendants([$exampleCards[2]["cardNumber"]], $exampleCards));
Assert::same(1, getNumberOfDescendants([$exampleCards[3]["cardNumber"]], $exampleCards));
Assert::same(0, getNumberOfDescendants([$exampleCards[4]["cardNumber"]], $exampleCards));
Assert::same(0, getNumberOfDescendants([$exampleCards[5]["cardNumber"]], $exampleCards));

function scoreCards2($cards)
{
    $aux = function ($cardNumbers, $score, $numDescendants) use (&$aux, $cards) {
        // We've run out of cards to count. Return the score.
        if (count($cardNumbers) === 0) {
            return $score;
        }

        // Shift the first card number
        $cardNumber = array_shift($cardNumbers);

        if (isset($numDescendants[$cardNumber])) {
            return $aux($cardNumbers, $score += $numDescendants[$cardNumber], $numDescendants);
        }

        // Conduct a DFS to find the number of descendants




        $score += $numDescendants[$cardNumber] + 1;

        return $aux($cardNumbers, $score, $numDescendants);
    };

    return $aux(array_column($cards, "cardNumber"), 0, []);
}

function solve2($lines)
{
    $cards = array_map("parseCard", $lines);
    return scoreCards2($cards);
}

Assert::same(30, solve2($exampleLines));

//echo "Total points (part 2):" . solve2($lines) . "\n";
