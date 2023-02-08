<?php

class Tree
{
    public int $x;
    public int $y;
    public int $height;

    public int $up;
    public int $down;
    public int $left;
    public int $right;

    public function __construct(int $x, int $y, int $height)
    {
        $this->x = $x;
        $this->y = $y;
        $this->height = $height;
    }

    public function getScenicScore()
    {
        return $this->down * $this->up * $this->left * $this->right;
    }
}

function treeAlreadyAdded(array $visible, Tree $tree)
{
    foreach ($visible as $visible_tree) {
        if ($visible_tree->x === $tree->x
            && $visible_tree->y === $tree->y) {
            return true;
        }
    }
}

$rows = file("input", FILE_IGNORE_NEW_LINES);

$trees = [];
$visible = [];

for ($y = 0; $y < count($rows); $y++) {
    $heights = str_split($rows[$y]);


    // From left
    $curmax = -1;
    for ($x = 0; $x < count($heights); $x++) {
        $height = $heights[$x];
        $tree = new Tree($x, $y, $height);
        $trees[] = $tree;

        if ($height > $curmax) {
            $visible[] = $tree;
            $curmax = $height;
        }
    }

    // From right
    $curmax = -1;
    for ($x = count($heights) - 1; $x >= 0; $x--) {
        $height = $heights[$x];
        if ($height > $curmax) {
            $curmax = $height;
            $tree = new Tree($x, $y, $height);
            if (!treeAlreadyAdded($visible, $tree)) {
                $visible[] = $tree;
            }
        }
    }
}

$num_cols = count(str_split($rows[0]));

for ($x = 0; $x < $num_cols; $x++) {
    $col_trees = array_filter($trees, function ($tree) use ($x) {
        return $tree->x === $x;
    });

    // From top
    $curmax = -1;
    foreach ($col_trees as $tree) {
        if ($tree->height > $curmax) {
            $curmax = $tree->height;
            if (!treeAlreadyAdded($visible, $tree)) {
                $visible[] = $tree;
            }
        }
    }

    // From bottom
    $curmax = -1;
    foreach (array_reverse($col_trees) as $tree) {
        if ($tree->height > $curmax) {
            $curmax = $tree->height;
            if (!treeAlreadyAdded($visible, $tree)) {
                $visible[] = $tree;
            }
        }
    }
}

//foreach ($visible as $tree) {
//    echo "($tree->x, $tree->y), height = $tree->height" . PHP_EOL;
//}
echo "Part 1. Visible Trees: " . count($visible) . PHP_EOL;

foreach ($trees as $tree1) {
    $col_trees = array_filter($trees, function ($tree2) use ($tree1) {
        return $tree1->x === $tree2->x;
    });
    $col_trees = array_values($col_trees);

    // Viewing distance down
    if ($tree1->y === count($col_trees) - 1) {
        $tree1->down = 0;
    } else {
        $y = $tree1->y + 1;
        while (
            $y < count($col_trees) - 1
            && $tree1->height > $col_trees[$y]->height
        ) {
            $y++;
        }
        $tree1->down = $y - $tree1->y;
    }

    // Viewing distance up
    if ($tree1->y === 0) {
        $tree1->up = 0;
    } else {
        $y = $tree1->y - 1;
        while ($y > 0 && $tree1->height > $col_trees[$y]->height) {
            $y--;
        }
        $tree1->up = $tree1->y - $y;
    }

    $row_trees = array_filter($trees, function ($tree2) use ($tree1) {
        return $tree1->y === $tree2->y;
    });
    $row_trees = array_values($row_trees);

    // Viewing distance right
    if ($tree1->x === count($row_trees) - 1) {
        $tree1->right = 0;
    } else {
        $x = $tree1->x + 1;
        while ($x < count($row_trees) - 1
            && $tree1->height > $row_trees[$x]->height) {
            $x++;
        }
        $tree1->right = $x - $tree1->x;
    }

    // Viewing distance left
    if ($tree1->x === 0) {
        $tree1->left = 0;
    } else {
        $x = $tree1->x - 1;
        while ($x > 0 && $tree1->height > $row_trees[$x]->height) {
            $x--;
        }
        $tree1->left = $tree1->x - $x;
    }
}

/*
foreach ($trees as $tree) {
    echo "($tree->x, $tree->y)" . PHP_EOL .
        " - height: $tree->height" . PHP_EOL .
        " - up: $tree->up" . PHP_EOL .
        " - down: $tree->down" . PHP_EOL .
        " - left: $tree->left" . PHP_EOL .
        " - right: $tree->right" . PHP_EOL .
        " - SCENIC_SCORE: " . $tree->getScenicScore() . PHP_EOL;
}
 */

$top_scenic_score = max(array_map(function ($tree) {
    return $tree->getScenicScore();
}, $trees));

echo "Part 2. Top scenic score: $top_scenic_score" . PHP_EOL;
