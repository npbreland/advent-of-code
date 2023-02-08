<?php

class Position
{
    public int $x;
    public int $y;

    public function __construct(int $x, int $y)
    {
        $this->x = $x;
        $this->y = $y;
    }
}

class Knot
{
    public Position $pos;

    public function __construct()
    {
        $this->pos = new Position(0, 0);
    }
}

class Head extends Knot
{
    public function moveByOne(string $direction)
    {
        switch ($direction) {
            case 'U':
                $this->pos->y++;
                break;
            case 'D':
                $this->pos->y--;
                break;
            case 'L':
                $this->pos->x--;
                break;
            case 'R':
                $this->pos->x++;
                break;
        }
    }
}

class Tail extends Knot
{
    public Knot $head;
    public array $visited = [];

    public function __construct(Knot $head)
    {
        $this->pos = new Position(0, 0);
        $this->head = $head;
        $this->tallyPosition();
    }

    private function tallyPosition(): void
    {
        $x = $this->pos->x;
        $y = $this->pos->y;
        $key = "($x, $y)";

        if (isset($this->visited[$key])) {
            $this->visited[$key]++;
        } else {
            $this->visited[$key] = 1;
        }
    }

    public function getVisitedStr(): string
    {
        $visited_str = '';
        foreach ($this->visited as $key => $tally) {
            $visited_str .= "$key, $tally" . PHP_EOL;
        }
        return $visited_str;
    }

    public function printGrid(): void
    {
        for ($y = 4; $y >= 0; $y--) {
            for ($x = 0; $x < 6; $x++) {
                if ($this->head->pos->x === $x
                    && $this->head->pos->y === $y) {
                    echo 'H';
                } elseif ($this->pos->x === $x && $this->pos->y === $y) {
                    echo 'T';
                } elseif ($x === 0 && $y === 0) {
                    echo 's';
                } else {
                    echo '.';
                }
            }
            echo PHP_EOL;
        }
    }

    public function getVisited(): array
    {
        return $this->visited;
    }

    private function getXDiff(): int
    {
        return $this->head->pos->x - $this->pos->x;
    }

    private function getYDiff(): int
    {
        return $this->head->pos->y - $this->pos->y;
    }

    public function printPos(): void
    {
        echo "$this->pos->x $this->pos->y" . PHP_EOL;
    }

    public function followHead(): void
    {
        $xdiff = $this->getXDiff();
        $ydiff = $this->getYDiff();

        if (abs($xdiff) > 1 || abs($ydiff) > 1) {
            $this->pos->x += $xdiff <=> 0;
            $this->pos->y += $ydiff <=> 0;
        }

        $this->tallyPosition();
    }
}

$instructions = file("input", FILE_IGNORE_NEW_LINES);

$head = new Head();
$tail = new Tail($head);

$instructions = array_map(function ($row) {
    $arr = explode(" ", $row);
    return [
        'direction' => $arr[0],
        'num' => $arr[1]
    ];
}, $instructions);

foreach ($instructions as $row) {
    for ($i = 0; $i < $row['num']; $i++) {
        $head->moveByOne($row['direction']);
        $tail->followHead();
        //$tail->printGrid();
    }
}

echo "Part 1. Positions visited at least once: " . count($tail->getVisited()) . PHP_EOL;

$head = new Head();
$knots = [ $head ];

for ($i = 1; $i < 10; $i++) {
    $knots[] = new Tail($knots[$i - 1]);
}

foreach ($instructions as $row) {
    for ($i = 0; $i < $row['num']; $i++) {
        $head->moveByOne($row['direction']);

        /** @var Tail **/
        foreach (array_slice($knots, 1) as $knot) {
            $knot->followHead();
        }
    }
}

echo "Part 2. Positions visited at least once: " . count(end($knots)->getVisited()) . PHP_EOL;
