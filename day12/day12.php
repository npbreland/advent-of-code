<?php

class Node
{
    public $x;
    public $y;
    public $elevation;
    public $connections = [];
    public $visited = false;
    public $distance = INF;
    public $parent = null;

    public function __construct(int $x, int $y, string $elevation)
    {
        $this->x = $x;
        $this->y = $y;

        if ($elevation === 'S') {
            $elevation = 'a';
        } elseif ($elevation === 'E') {
            $elevation = 'z';
        }

        $this->elevation = $elevation;
    }

    public function addConnectionsFromGraph(array $graph): void
    {
        $neighbors = [
            $graph[$this->x][$this->y - 1] ?? null,
            $graph[$this->x][$this->y + 1] ?? null,
            $graph[$this->x - 1][$this->y] ?? null,
            $graph[$this->x + 1][$this->y] ?? null,
        ];

        $neighbors = array_filter($neighbors, function ($node) {
            return $node !== null;
        });

        // Neighbors are only connected if their elevation is at most 1 higher
        $this->connections = array_filter($neighbors, function ($node) {
            return (ord($node->elevation) - ord($this->elevation)) <= 1;
        });
    }
}


function buildNodes(): array
{
    $lines = file('input', FILE_IGNORE_NEW_LINES);
    $graph = [];
    $nodes = [];

    /* Parse input into nodes. $graph is a 2D array of nodes, indexed by x and y.
     * this will make it easier to find neighbors. $nodes is a flat array of all
     * nodes, which is easier to loop through. */
    foreach ($lines as $y => $line) {
        $chars = str_split($line);
        foreach ($chars as $x => $char) {
            $node = new Node($x, $y, $char);
            $graph[$x][$y] = $node;
            $nodes[] = $node;
            if ($char === 'S') {
                $start = $node;
            } elseif ($char === 'E') {
                $end = $node;
            }
        }
    }

    // Add connections to nodes
    foreach ($nodes as $node) {
        $node->addConnectionsFromGraph($graph);
    }

    return [
        'nodes' => $nodes,
        'start' => $start,
        'end' => $end
    ];
}


// Find shortest path using Dijkstra's algorithm
function findShortestPath(array $nodes, Node $start, Node $end)
{
    $aux = function ($current) use (&$aux, $nodes, $start, $end) {
        $current->visited = true;

        foreach ($current->connections as $cxn) {
            $distance = $current->distance + 1;
            if ($distance < $cxn->distance) {
                $cxn->distance = $distance;
                $cxn->parent = $current;
            }
        }

        $unvisited = array_filter($nodes, function ($node) {
            return !$node->visited;
        });

        $minDistance = min(array_column($unvisited, 'distance'));

        if ($minDistance === INF) {
            return [
                'path' => false,
                'distance' =>  INF,
            ];
        }

        if ($minDistance === $end->distance) {
            // Next node could be the end node, so we have the shortest path
            // Trace back to start node
            $path = [];
            $traceNode = $end;
            while ($traceNode !== $start) {
                $path[] = $traceNode;
                $traceNode = $traceNode->parent;
            }

            $path[] = $start;
            return [
                'path' => array_reverse($path),
                'distance' => $end->distance
            ];
        }

        foreach ($unvisited as $node) {
            if ($node->distance === $minDistance) {
                return $aux($node);
            }
        }
    };

    $start->distance = 0;
    return $aux($start);
}

function resetNodes(array $nodes): void
{
    foreach ($nodes as $node) {
        $node->visited = false;
        $node->distance = INF;
        $node->parent = null;
    }
}

$nodeResult = buildNodes();
$start = $nodeResult['start'];
$end = $nodeResult['end'];
$nodes = $nodeResult['nodes'];

$result = findShortestPath($nodes, $start, $end);

echo 'Part 1. Distance: ' . $result['distance'] . PHP_EOL;

// Part 2
resetNodes($nodes);

// Find the shortest path from a node with elevation 'a' to the end node
$aNodes = array_filter($nodes, function ($node) {
    return $node->elevation === 'a';
});

$shortest = INF;
foreach ($aNodes as $aNode) {
    $result = findShortestPath($nodes, $aNode, $end);
    if ($result['distance'] < $shortest) {
        $shortest = $result['distance'];
    }
    resetNodes($nodes); // Need to reset before finding next path
}

echo 'Part 2. Distance: ' . $shortest . PHP_EOL;
