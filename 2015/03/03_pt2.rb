require "test/unit"

class SantaDispatcher

  def initialize(santas)
    @santas = santas
    @santa_index = 0
  end

  def get_next_santa
    @santas[@santa_index % @santas.length]
  end

  def parse_input(input)
    input.split("").each do |c|
      santa = get_next_santa
      santa.parse_input(c)
      @santa_index += 1
    end
  end

  def reconcile_house_count
    all_keys = @santas.reduce([]) { |acc, santa| acc + santa.presents.keys }
    all_keys.uniq.length
  end
end


class SantaTracker
  attr_reader :x, :y, :presents

  def initialize(x, y)
    @x = x
    @y = y
    @presents = {}
    add_presents # add present at starting position
  end

  def add_presents
    if @presents.key?(get_position_hash(@x, @y))
      @presents[get_position_hash(@x, @y)] += 1
    else
      @presents[get_position_hash(@x, @y)] = 1
    end
  end

  def move_up
    @y += 1
    add_presents
  end

  def move_down
    @y -= 1
    add_presents
  end

  def move_left
    @x -= 1
    add_presents
  end

  def move_right
    @x += 1
    add_presents
  end

  def get_position_hash(x, y)
    "%{x},%{y}" % {x: x, y: y}
  end

  def get_houses_with_at_least_one_present
    presents.keys.length
  end

  def parse_input(input)
    input.split("").each do |c|
      if c == "^"
        move_up
      elsif c == "v"
        move_down
      elsif c == "<"
        move_left
      elsif c == ">"
        move_right
      end
    end
  end
end

class MyTest < Test::Unit::TestCase

  def test_move_up
    tracker = SantaTracker.new(0, 0)
    tracker.move_up()
    assert_equal(0, tracker.x)
    assert_equal(1, tracker.y)
  end

  def test_move_down
    tracker = SantaTracker.new(0, 0)
    tracker.move_down()
    assert_equal(0, tracker.x)
    assert_equal(-1, tracker.y)
  end

  def test_move_left
    tracker = SantaTracker.new(0, 0)
    tracker.move_left()
    assert_equal(-1, tracker.x)
    assert_equal(0, tracker.y)
  end

  def test_move_right
    tracker = SantaTracker.new(0, 0)
    tracker.move_right()
    assert_equal(1, tracker.x)
    assert_equal(0, tracker.y)
  end

  def test_position_hash
    tracker = SantaTracker.new(0, 0)
    assert_equal("0,0", tracker.get_position_hash(0, 0))
  end

  def test_get_houses_with_at_least_one_present
    tracker = SantaTracker.new(0, 0)
    tracker.move_right()
    assert_equal(2, tracker.get_houses_with_at_least_one_present())

    tracker.move_right()
    assert_equal(3, tracker.get_houses_with_at_least_one_present())

    tracker.move_left()
    assert_equal(3, tracker.get_houses_with_at_least_one_present())

    tracker.move_up()
    assert_equal(4, tracker.get_houses_with_at_least_one_present())
  end

  def test_parse_input
    tracker = SantaTracker.new(0, 0)
    tracker.parse_input("^")
    assert_equal(0, tracker.x)
    assert_equal(1, tracker.y)

    tracker.parse_input(">")
    assert_equal(1, tracker.x)
    assert_equal(1, tracker.y)

    tracker.parse_input("v")
    assert_equal(1, tracker.x)
    assert_equal(0, tracker.y)

    tracker.parse_input("<")
    assert_equal(0, tracker.x)
    assert_equal(0, tracker.y)
  end

  def test_dispatch
    santa = SantaTracker.new(0, 0)
    robo = SantaTracker.new(0, 0)

    dispatcher = SantaDispatcher.new([santa, robo])
    dispatcher.parse_input("^v")

    assert_equal(3, dispatcher.reconcile_house_count)

    santa = SantaTracker.new(0, 0)
    robo = SantaTracker.new(0, 0)

    dispatcher = SantaDispatcher.new([santa, robo])
    dispatcher.parse_input("^>v<")

    assert_equal(3, dispatcher.reconcile_house_count)

    santa = SantaTracker.new(0, 0)
    robo = SantaTracker.new(0, 0)

    dispatcher = SantaDispatcher.new([santa, robo])
    dispatcher.parse_input("^v^v^v^v^v")

    assert_equal(11, dispatcher.reconcile_house_count)
  end

end

santa = SantaTracker.new(0, 0)
robo = SantaTracker.new(0, 0)
dispatcher = SantaDispatcher.new([santa, robo])
input = File.read("input.txt")
dispatcher.parse_input(input)

puts "Houses: %s" % dispatcher.reconcile_house_count
