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

    public function incX(int $num = 1): void
    {
        $this->x += $num;
    }

    public function decX(int $num = 1): void
    {
        $this->x -= $num;
    }

    public function incY(int $num = 1): void
    {
        $this->y += $num;
    }

    public function decY(int $num = 1): void
    {
        $this->y -= $num;
    }

    public function setX(int $x): void
    {
        $this->x = $x;
    }

    public function setY(int $y): void
    {
        $this->y = $y;
    }

    public function getX(): int
    {
        return $this->x;
    }

    public function getY(): int
    {
        return $this->y;
    }
}

class Head
{
    private Position $pos;

    public function __construct()
    {
        $this->pos = new Position(0, 0);
    }

    public function getPos(): Position
    {
        return $this->pos;
    }

    public function moveByOne(string $direction)
    {
        switch ($direction) {
            case 'U':
                $this->pos->incY();
                break;
            case 'D':
                $this->pos->decY();
                break;
            case 'L':
                $this->pos->decX();
                break;
            case 'R':
                $this->pos->incX();
                break;
        }
    }
}

class Tail
{
    private Position $pos;
    private Head $head;
    private array $visited = [];

    public function __construct(Head $head)
    {
        $this->pos = new Position(0, 0);
        $this->head = $head;
        $this->tallyPosition();
    }

    private function tallyPosition(): void
    {
        $x = $this->pos->getX();
        $y = $this->pos->getY();
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
                if ($this->head->getPos()->getX() === $x
                    && $this->head->getPos()->getY() === $y) {
                    echo 'H';
                } elseif ($this->pos->getX() === $x && $this->pos->getY() === $y) {
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
        return $this->head->getPos()->getX() - $this->pos->getX();
    }

    private function getYDiff(): int
    {
        return $this->head->getPos()->getY() - $this->pos->getY();
    }

    private function adjacentToHead(): bool
    {
        // On the same point or touching
        return abs($this->getXDiff()) <= 1 && abs($this->getYDiff()) <= 1;
    }

    public function printPos(): void
    {
        $x = $this->pos->getX();
        $y = $this->pos->getY();
        $key = "$x $y";
        echo $key . PHP_EOL;
    }


    public function moveToBeAdjacent(): void
    {
        if ($this->adjacentToHead()) {
            return;
        }

        $head_x = $this->head->getPos()->getX();
        $head_y = $this->head->getPos()->getY();

        if (abs($this->getYDiff()) > 1) {
            $this->pos->setX($head_x);

            if ($this->getYDiff() > 1) {
                $this->pos->setY($head_y - 1);
            } else {
                $this->pos->setY($head_y + 1);
            }
        } else {
            $this->pos->setY($head_y);

            if ($this->getXDiff() > 1) {
                $this->pos->setX($head_x - 1);
            } else {
                $this->pos->setX($head_x + 1);
            }
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
        $tail->moveToBeAdjacent();
    }
}

echo "Part 1. Positions visited at least once: " . count($tail->getVisited()) . PHP_EOL;
