<?php

define('ROW_TO_CHECK', 2000000);

function manhattanDistance($x1, $x2, $y1, $y2)
{
    return abs($x1 - $x2) + abs($y1 - $y2);
}

class Sensor
{
    public $x;
    public $y;
    public $beaconX;
    public $beaconY;

    public function __construct($x, $y, $beaconX, $beaconY)
    {
        $this->x = $x;
        $this->y = $y;
        $this->beaconX = $beaconX;
        $this->beaconY = $beaconY;
    }

    public function getMinX()
    {
        return $this->x - $this->getDistanceFromBeacon();
    }

    public function getMaxX()
    {
        return $this->x + $this->getDistanceFromBeacon();
    }

    private function getDistanceFromBeacon(): int
    {
        return manhattanDistance(
            $this->x,
            $this->beaconX,
            $this->y,
            $this->beaconY
        );
    }

    public function getEmptyZoneOnRow(int $minX, int $maxX, int $row): array
    {
        $distanceFromBeacon = $this->getDistanceFromBeacon();

        $emptyZone = [];
        for ($x = $minX; $x <= $maxX; $x++) {
            if ($x === $this->beaconX && $row === $this->beaconY) {
                // Skip the place where the beacon actually is
                continue;
            }
            $distance = manhattanDistance($x, $this->x, $row, $this->y);
            if ($distance <= $distanceFromBeacon) {
                $emptyZone[] = $x;
            }
        }

        return $emptyZone;
    }
}

$lines = file('input', FILE_IGNORE_NEW_LINES);

$sensors = [];
foreach ($lines as $line) {
    $regex = <<<RGX
/Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
RGX;
    preg_match($regex, $line, $matches);
    $xs = (int) $matches[1];
    $ys = (int) $matches[2];
    $xb = (int) $matches[3];
    $yb = (int) $matches[4];
    $sensors[] = new Sensor($xs, $ys, $xb, $yb);
}

/* Keep track of the min and max X values of the beacons. We want the domain
of the "empty zone" scan to be the same for each iteration. */
$minX = array_reduce($sensors, function ($carry, $sensor) {
    return min($carry, $sensor->getMinX());
}, PHP_INT_MAX);

$maxX = array_reduce($sensors, function ($carry, $sensor) {
    return max($carry, $sensor->getMaxX());
}, PHP_INT_MIN);

$emptyZone = array_unique(array_reduce($sensors, function ($carry, $sensor) use ($minX, $maxX) {
    return array_merge($carry, $sensor->getEmptyZoneOnRow($minX, $maxX, ROW_TO_CHECK));
}, []));
sort($emptyZone);

echo "Part 1. # spaces where a sensor cannot exist on row " . ROW_TO_CHECK. ": " . count($emptyZone) . PHP_EOL;
