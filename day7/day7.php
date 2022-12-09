<?php

$lines = file("input", FILE_IGNORE_NEW_LINES);

class DirNode
{
    public string $name;
    public int $size = 0;

    public ?DirNode $parent = null;
    public array $children = [];

    public function __construct(string $name)
    {
        $this->name = $name;
    }

    public function setParent(DirNode $dir): void
    {
        $this->parent = $dir;
    }

    public function addChild(DirNode $dir): void
    {
        $this->children[] = $dir;
    }

    public function getParent(): DirNode
    {
        return $this->parent;
    }

    public function addToSize(int $size): void
    {
        $this->size += $size;
    }

    public function getSizeRecursive(): int
    {
        return
            $this->size +
            array_reduce($this->children, function ($acc, $child) {
                return $acc + $child->getSizeRecursive();
            });
    }

    public function getChild(string $name): DirNode|false
    {
        $key = array_search($name, array_column($this->children, 'name'));
        if ($key === false) {
            return false;
        }
        return $this->children[$key];
    }
}

$nodes = [];

foreach ($lines as $line) {
    if (substr($line, 0, 4) === "$ cd") {
        $dir = substr($line, 5);

        if ($dir === "..") {
            $curnode = $curnode->getParent();
        } elseif (!isset($curnode)) {
            $curnode = new DirNode($dir);
            $nodes[] = $curnode;
        } else {
            $child = $curnode->getChild($dir);
            if ($child) {
                $curnode = $child;
            } else {
                $child = new DirNode($dir);
                $child->setParent($curnode);
                $curnode->addChild($child);
                $nodes[] = $child;
                $curnode = $child;
            }
        }
    } elseif (preg_match("/^[0-9]+/", $line, $matches)) {
        $curnode->addToSize($matches[0]);
    }
}

$dir_sizes = array_map(function ($node) {
    return $node->getSizeRecursive();
}, $nodes);

$at_most_100k = array_filter($dir_sizes, function ($size) {
    return $size <= 100000;
});

$at_most_100k_sum = array_sum($at_most_100k);

echo "Part 1. Sum of sizes of dirs over 100000: " . $at_most_100k_sum . PHP_EOL;

$total_disk_space   = 70000000;
$update_space       = 30000000;
$used = $nodes[0]->getSizeRecursive();

$unused = $total_disk_space - $used;
$to_free = $update_space - $unused;

$enough_to_free = array_filter($dir_sizes, function ($size) use ($to_free) {
    return $size >= $to_free;
});

$smallest_to_free = min($enough_to_free);

echo "Part 2. Smallest dir that will free: " . $smallest_to_free . PHP_EOL;
