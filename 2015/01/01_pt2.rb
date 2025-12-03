require "test/unit"


class FloorTracker
  attr_reader :floor, :first_basement_char

  def initialize(floor)
    @floor = floor
  end

  def go_up
    @floor += 1
  end

  def go_down
    @floor -= 1
  end

  def parse_input(input)
    char = 1
    input.split("").each do |c|

      if c == "("
        go_up
      elsif c == ")"
        go_down
      end

      if floor == -1 && !defined? @first_basement_char
        @first_basement_char = char
      end

      char += 1

    end
  end
end

class MyTest < Test::Unit::TestCase
  def test_go_up
    tracker = FloorTracker.new(0)
    tracker.go_up()
    assert_equal(1, tracker.floor)
  end

  def test_go_down
    tracker = FloorTracker.new(1)
    tracker.go_down()
    assert_equal(0, tracker.floor)
  end

  def test_parse_input
    tracker = FloorTracker.new(0)
    tracker.parse_input("(())")
    assert_equal(0, tracker.floor)

    tracker = FloorTracker.new(0)
    tracker.parse_input("()()")
    assert_equal(0, tracker.floor)

    tracker = FloorTracker.new(0)
    tracker.parse_input("(((")
    assert_equal(3, tracker.floor)

    tracker = FloorTracker.new(0)
    tracker.parse_input("(()(()(")
    assert_equal(3, tracker.floor)

    tracker = FloorTracker.new(0)
    tracker.parse_input("())")
    assert_equal(-1, tracker.floor)
    assert_equal(3, tracker.first_basement_char)

    tracker = FloorTracker.new(0)
    tracker.parse_input("))(")
    assert_equal(-1, tracker.floor)
    assert_equal(1, tracker.first_basement_char)

    tracker = FloorTracker.new(0)
    tracker.parse_input(")))")
    assert_equal(-3, tracker.floor)
    assert_equal(1, tracker.first_basement_char)

    tracker = FloorTracker.new(0)
    tracker.parse_input(")())())")
    assert_equal(-3, tracker.floor)
    assert_equal(1, tracker.first_basement_char)
  end
end

tracker = FloorTracker.new(0)
input = File.read("input.txt")
tracker.parse_input(input)

puts "First basement character position: %s" % tracker.first_basement_char


