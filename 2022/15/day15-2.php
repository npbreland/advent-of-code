<?php

define('MAX_X', 20);
define('MAX_Y', 20);
define('INPUT_FILE', 'test-input');

function manhattanDistance($x1, $x2, $y1, $y2)
{
    return abs($x1 - $x2) + abs($y1 - $y2);
}

function slope($x1, $x2, $y1, $y2)
{
    return ($y2 - $y1) / ($x2 - $x1);
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

    public function getMinY()
    {
        return $this->y - $this->getDistanceFromBeacon();
    }

    public function getMaxY()
    {
        return $this->y + $this->getDistanceFromBeacon();
    }

    public function getDistanceFromBeacon(): int
    {
        return manhattanDistance(
            $this->x,
            $this->beaconX,
            $this->y,
            $this->beaconY
        ) + 1;
    }

    public function getVertices(): array
    {
        return [
            [$this->getMinX(), $this->y],
            [$this->x, $this->getMinY()],
            [$this->getMaxX(), $this->y],
            [$this->x, $this->getMaxY()],
        ];
    }

    public function getEdges(): array
    {
        $vertices = $this->getVertices();
        $edges = [];
        for ($i = 0; $i < count($vertices) - 1; $i++) {
            $j = $i + 1;
            $edges[] = [$vertices[$i], $vertices[$j]];
        }
        // Add the last edge
        $edges[] = [$vertices[count($vertices) - 1], $vertices[0]];

        return $edges;
    }

    private function getScanlineEdge($edge)
    {
        $x1 = $edge[0][0];
        $y1 = $edge[0][1];
        $x2 = $edge[1][0];
        $y2 = $edge[1][1];

        $minY = min($y1, $y2);
        $maxY = max($y1, $y2);
        $xOfMinY = $minY === $y1 ? $x1 : $x2;
        $xOfMaxY = $minY === $y1 ? $x2 : $x1;

        $slope = slope($xOfMinY, $xOfMaxY, $minY, $maxY);

        return [$minY, $maxY, $xOfMinY, 1/$slope];
    }

    public function getScanlineEdges(): array
    {
        $edges = $this->getEdges();
        $scanlineEdges = [];
        foreach ($edges as $edge) {
            $scanlineEdges[] = $this->getScanlineEdge($edge);
        }
        return $scanlineEdges;
    }
}

$lines = file(INPUT_FILE, FILE_IGNORE_NEW_LINES);

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

// Exclusion zones will be represented as polygons, one for each sensor
$polygons = array_map(function ($sensor) {
    /** @var Sensor $sensor */
    return $sensor->getScanlineEdges();
}, $sensors);

$grid = array_fill(0, MAX_X, array_fill(0, MAX_Y, '.'));

// Run scanline algorithm on each polygon
function renderByScanline($grid, $edges): array
{
    // Filter out any edges with slope 0
    $edges = array_filter($edges, function ($edge) {
        return $edge[3] !== 0;
    });

    // Add edges into global edge table according to the following rules:
    // (Adapted from https://www.cs.rit.edu/~icss571/filling/how_to.html)
    // 1. Place the first edge with a slope != 0 into the global edge table
    // 2. Start at index 0 and increase index by 1 each time the edge's minY is
    // greater than the minY of the edge at that index in the global edge table
    // 3. Increase the index onch each time the edge's x value is greater than and
    // the minY value is less than or equal to that of the edge at that index in
    // the global edge table.
    // 4. If the index at any time is equal to the length of the global edge table,
    // do not increase the index
    // 5. Insert the edge data at the index: minY, maxY, xOfMinY, (1/slope)

    $globalEdgeTable = [];

    foreach ($edges as $edge) {
        if (count($globalEdgeTable) === 0) {
            $globalEdgeTable[] = $edge;
            continue;
        }

        $index = 0;
        while ($index < count($globalEdgeTable)) {
            $globalEdge = $globalEdgeTable[$index];
            if ($edge[0] > $globalEdge[0]) {
                $index++;
                continue;
            }

            if ($edge[0] === $globalEdge[0]) {
                if ($edge[2] > $globalEdge[2]) {
                    $index++;
                    continue;
                }
            }

            array_splice($globalEdgeTable, $index, 0, [$edge]);
            break;
        }

        if ($index === count($globalEdgeTable)) {
            $globalEdgeTable[] = $edge;
        }
    }

    // Scanline starts at the top
    //$scanline = max(0, $globalEdgeTable[0][0]);

    $globalEdgeTableSortedByMaxY = $globalEdgeTable;
    usort($globalEdgeTableSortedByMaxY, function ($a, $b) {
        return $b[1] <=> $a[1];
    });
    //$scanlineEnd = min(MAX_Y, $globalEdgeTableSortedByMaxY[0][1]);
    //$scanline = 0;
    $scanline = $globalEdgeTable[0][0];
    $scanlineEnd = MAX_Y;
    $activeEdgeTable = [];

    while ($scanline <= $scanlineEnd) {
        // Remove edges that end on this scanline
        foreach ($activeEdgeTable as $key => $edge) {
            if ($edge[1] === $scanline) {
                unset($activeEdgeTable[$key]);
            }
        }

        // Update x-values of edges in active edge table (moving down slope)
        foreach ($activeEdgeTable as $key => $edge) {
            $activeEdgeTable[$key][2] += $edge[3];
        }

        // Add edges that start on this scanline
        foreach ($globalEdgeTable as $key => $edge) {
            if ($edge[0] === $scanline) {
                $activeEdgeTable[] = $edge;
                unset($globalEdgeTable[$key]);
            }
            if ($edge[0] > $scanline) {
                break;
            }
        }

        //var_dump(memory_get_usage());
        // Sort active edge table by x value
        usort($activeEdgeTable, function ($a, $b) {
            return $a[2] <=> $b[2];
        });


        if (count($activeEdgeTable) === 0) {
            $scanline++;
            continue;
        }

        // Since we are dealing with one diamond at a time, we can assume that
        // the active edge table will always be a single pair
        $x1 = $activeEdgeTable[0][2];
        $x2 = $activeEdgeTable[1][2];

        for ($x = $x1 + 1; $x < $x2 && $x < MAX_X; $x++) {
            if ($x < 0 || $scanline < 0) {
                continue;
            }
            $grid[$scanline][$x] = '#';
            if (isset($grid[$scanline][$x])) {
                unset($grid[$scanline][$x]);
                if (count($grid[$scanline]) === 0) {
                    unset($grid[$scanline]);
                }
            }
        }
        $scanline++;
    }
    return $grid;
}

foreach ($polygons as $edges) {
    $grid = renderByScanline($grid, $edges);
}

$beaconY = array_key_first($grid);
$beaconX = array_key_first($grid[$beaconY]);

$tuningFrequency = $beaconX * 4E6 + $beaconY;

echo "Beacon is at x=$beaconX, y=$beaconY" . PHP_EOL;
echo "Tuning frequency is $tuningFrequency" . PHP_EOL;

/*
foreach ($grid as $key => $row) {
    $padkey = str_pad($key, 2, '0', STR_PAD_LEFT);
    echo "$padkey " . implode('', $row) . PHP_EOL;
}
 */
