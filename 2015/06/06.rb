require "test/unit"

# Create length x length grid filled with 0s
def create_grid(length)
  Array.new(length) {Array.new(length, 0)}
end

class Grid
  attr_reader :grid

  def initialize(length)
    @grid = Array.new(length) {Array.new(length, 0)}
  end

  def turn_on(x1, y1, x2, y2)
    rows = (y1..y2).to_a
    columns = (x1..x2).to_a

    rows.each do |row|
      columns.each do |col|
        @grid[row][col] = 1
      end
    end
  end

  def turn_off(x1, y1, x2, y2)
    rows = (y1..y2).to_a
    columns = (x1..x2).to_a

    rows.each do |row|
      columns.each do |col|
        @grid[row][col] = 0
      end
    end
  end
  
  def toggle(x1, y1, x2, y2)
    rows = (y1..y2).to_a
    columns = (x1..x2).to_a

    rows.each do |row|
      columns.each do |col|
        @grid[row][col] = @grid[row][col] == 0 ? 1 : 0
      end
    end
  end

  def lights_lit
    @grid.reduce(0) { |sum, row| sum + row.sum }
  end

  def get_coordinates_from_instruction(instruction)
    instruction.scan(/\d+/).map { |s| s.to_i }
  end

  def get_action_from_instruction(instruction)
    if instruction.include? "on"
      return "on"
    elsif instruction.include? "off"
      return "off"
    elsif instruction.include? "toggle"
      return "toggle"
    end
  end

  def process_instruction(instruction)
    coords = get_coordinates_from_instruction(instruction)
    action = get_action_from_instruction(instruction)

    if action == "on"
      turn_on(*coords)
    elsif action == "off"
      turn_off(*coords)
    elsif action == "toggle"
      toggle(*coords)
    end

  end

end

class MyTest < Test::Unit::TestCase
  def test_create_grid
    grid = Grid.new(1000)
    assert_equal(1000, grid.grid[0].length)
    assert_equal(1000, grid.grid.length)
    assert_equal(0, grid.grid[0][0])
    assert_equal(0, grid.grid[1][0])
  end

  def test_turn_on
    grid = Grid.new(1000)
    assert_equal(0, grid.grid[0][0])

    grid.turn_on(0, 0, 2, 2)
    assert_equal(1, grid.grid[0][0])
  end

  def test_turn_off
    grid = Grid.new(1000)
    assert_equal(0, grid.grid[0][0])

    grid.turn_on(0, 0, 2, 2)
    assert_equal(1, grid.grid[0][0])

    grid.turn_off(0, 0, 2, 2)
    assert_equal(0, grid.grid[0][0])
  end

  def test_toggle
    grid = Grid.new(1000)
    assert_equal(0, grid.grid[0][0])
    grid.turn_on(0, 0, 2, 2)
    grid.turn_off(0, 0, 1, 1)
    grid.toggle(0, 0, 2, 2)
    assert_equal(1, grid.grid[0][0])
    assert_equal(0, grid.grid[2][2])
  end

  def test_lights_lit
    grid = Grid.new(1000)
    assert_equal(0, grid.lights_lit)

    grid.turn_on(0, 0, 2, 2)
    assert_equal(9, grid.lights_lit)

    grid.turn_off(0, 0, 1, 1)
    assert_equal(5, grid.lights_lit)

    grid.toggle(0, 0, 2, 2)
    assert_equal(4, grid.lights_lit)
  end

  def test_get_coordinates_from_instruction
    grid = Grid.new(1000)

    coords = grid.get_coordinates_from_instruction("turn on 489,959 through 759,964")
    assert_equal([489, 959, 759, 964], coords)

    coords = grid.get_coordinates_from_instruction("toggle 0,0 through 999,999")
    assert_equal([0, 0, 999, 999], coords)

    coords = grid.get_coordinates_from_instruction("turn off 499,499 through 500,500")
    assert_equal([499, 499, 500, 500], coords)
  end

  def test_get_action_from_instruction
    grid = Grid.new(1000)

    action = grid.get_action_from_instruction("turn on 489,959 through 759,964")
    assert_equal("on", action)

    action = grid.get_action_from_instruction("toggle 0,0 through 999,0")
    assert_equal("toggle", action)

    action = grid.get_action_from_instruction("turn off 499,499 through 500,500")
    assert_equal("off", action)
  end

  def test_process_instruction
    grid = Grid.new(1000)

    grid.process_instruction("turn on 0,0 through 2,2")
    assert_equal(9, grid.lights_lit)

    grid.process_instruction("turn off 0,0 through 1,1")
    assert_equal(5, grid.lights_lit)

    grid.process_instruction("toggle 0,0 through 2,2")
    assert_equal(4, grid.lights_lit)
  end

end

grid = Grid.new(1000)
lines = File.readlines("input.txt")

lines.each do |line|
  grid.process_instruction(line.chomp)
end

puts "Lights lit: %s" % grid.lights_lit
