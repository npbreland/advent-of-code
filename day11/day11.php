<?php

class Item
{
    public $worry;

    public function __construct($worry)
    {
        $this->worry = $worry;
    }

    public function doOperation(string $op, $num): void
    {
        // Special case. if no number is specified, it's the current worry
        if (is_null($num)) {
            $num = $this->worry;
        }

        switch ($op) {
            case '+':
                $this->worry = bcadd($this->worry, $num);
                break;
            case '*':
                $this->worry = bcmul($this->worry, $num);
                break;
        }
    }

    public function isDivisibleBy($num): bool
    {
        return bcmod($this->worry, $num) == 0;
    }

    public function throwToMonkey(Monkey $monkey): void
    {
        $monkey->addItem($this);
    }

    public function reduceWorry(): void
    {
        $this->worry = bcdiv($this->worry, 3);
    }
}

class Monkey
{
    public $id;
    public $item_list = [];
    public $inspected = 0;

    public function __construct(int $id)
    {
        $this->id = $id;
    }

    public function addItem(Item $item)
    {
        $this->item_list[] = $item;
    }

    public function setItemList(array $item_list): void
    {
        $this->item_list = $item_list;
    }

    public function inspectItems(
        string $op,
        $op_num,
        $div_num,
        Monkey $true_monkey,
        Monkey $false_monkey,
        bool $reduce_worry = true
    ) {
        while (count($this->item_list) > 0) {
            /** @var Item **/
            $item = array_shift($this->item_list);
            $item->doOperation($op, $op_num);

            if ($reduce_worry) {
                $item->reduceWorry();
            }

            if ($item->isDivisibleBy($div_num)) {
                $item->throwToMonkey($true_monkey);
            } else {
                $item->throwToMonkey($false_monkey);
            }

            $this->inspected++;
        }
    }
}


$lines = file("input", FILE_IGNORE_NEW_LINES);

$monkey_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 0, strlen('Monkey')) === 'Monkey';
}));
$start_items_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 2, strlen('Starting items')) === 'Starting items';
}));
$operation_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 2, strlen('Operation')) === 'Operation';
}));
$test_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 2, strlen('Test')) === 'Test';
}));
$true_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 7, strlen('true')) === 'true';
}));
$false_lines = array_values(array_filter($lines, function ($line) {
    return substr($line, 7, strlen('false')) === 'false';
}));

$monkeys = array_map(function ($line) {
    preg_match('/[0-9]+/', $line, $matches);
    return new Monkey($matches[0]);
}, $monkey_lines);

$starting_items_strs = array_map(function ($line) {
    return substr($line, 2 + strlen('Starting items: '));
}, $start_items_lines);

foreach ($starting_items_strs as $key => $items_str) {
    $worry_levels = explode(", ", $items_str);

    $item_list = array_map(function ($worry) {
        return new Item($worry);
    }, $worry_levels);

    $monkeys[$key]->setItemList($item_list);
}

$operations = array_map(function ($line) {
    $op = [];

    if (strpos($line, '*')) {
        $op['operator'] = '*';
    } elseif (strpos($line, '+')) {
        $op['operator'] = '+';
    }

    preg_match('/[0-9]+/', $line, $matches);

    if (isset($matches[0])) {
        $op['num'] = $matches[0];
    } else {
        $op['num'] = null;
    }

    return $op;
}, $operation_lines);

$tests = array_map(function ($line) {
    preg_match('/[0-9]+/', $line, $matches);
    return $matches[0];
}, $test_lines);

$true_monkeys = array_map(function ($line) {
    preg_match('/[0-9]/', $line, $matches);
    return $matches[0];
}, $true_lines);

$false_monkeys = array_map(function ($line) {
    preg_match('/[0-9]/', $line, $matches);
    return $matches[0];
}, $false_lines);

for ($round = 0; $round < 20; $round++) {
    /** @var Monkey */
    foreach ($monkeys as $key => $monkey) {
        $op = $operations[$key];
        $test = $tests[$key];
        $true_monkey = $true_monkeys[$key];
        $false_monkey = $false_monkeys[$key];

        $monkey->inspectItems(
            $op['operator'],
            $op['num'],
            $test,
            $monkeys[$true_monkey],
            $monkeys[$false_monkey],
            true
        );
    }
}

foreach ($monkeys as $key => $monkey) {
    echo "Monkey $key inspected items $monkey->inspected times." . PHP_EOL;
}

$inspected_counts = array_column($monkeys, 'inspected');
rsort($inspected_counts);

$monkey_business = $inspected_counts[0] * $inspected_counts[1];
echo "Part 1. Monkey business: $monkey_business" . PHP_EOL;

/*
// Reset monkeys.
$monkeys = array_map(function ($line) {
    preg_match('/[0-9]+/', $line, $matches);
    return new Monkey($matches[0]);
}, $monkey_lines);

// Reset items
foreach ($starting_items_strs as $key => $items_str) {
    $worry_levels = explode(", ", $items_str);

    $item_list = array_map(function ($worry) {
        return new Item($worry);
    }, $worry_levels);

    $monkeys[$key]->setItemList($item_list);
}

// Part 2
for ($round = 0; $round < 20; $round++) {
    foreach ($monkeys as $key => $monkey) {
        $op = $operations[$key];
        $test = $tests[$key];
        $true_monkey = $true_monkeys[$key];
        $false_monkey = $false_monkeys[$key];

        $monkey->inspectItems(
            $op['operator'],
            $op['num'],
            $test,
            $monkeys[$true_monkey],
            $monkeys[$false_monkey],
            false
        );
    }
}

foreach ($monkeys as $key => $monkey) {
    echo "Monkey $key inspected items $monkey->inspected times." . PHP_EOL;
}

$inspected_counts = array_column($monkeys, 'inspected');
rsort($inspected_counts);

$monkey_business = $inspected_counts[0] * $inspected_counts[1];
echo "Part 2. Monkey business: $monkey_business" . PHP_EOL;
 */
