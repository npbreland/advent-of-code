require "test/unit"

class SantaTracker
  attr_reader :x, :y, :presents

  def initialize(x, y)
    @presents = {"0,0": 1}
    @x = x
    @y = y
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
    filtered_hash = @presents.select { |_, presents| presents >= 1 }
    filtered_hash.length
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

  # def test_track_presents
  #   tracker = SantaTracker.new(0, 0)
  #   tracker.move_right()
  #   assert_equal(1, tracker.get_presents_at(1, 0))
  # end

end

tracker = SantaTracker.new(0, 0)
input = File.read("input.txt")
tracker.parse_input(input)

puts "Houses: %s" % tracker.get_houses_with_at_least_one_present()
