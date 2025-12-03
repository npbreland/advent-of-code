require "test/unit"

def surface_area(l, w, h)
  lw = 2*l*w
  wh = 2*w*h
  hl = 2*h*l
  return lw + wh + hl + [lw, wh, hl].min / 2
end

def parse_dimensions(line)
  return line.split("x").map {|d| d.to_i}
end

class MyTest < Test::Unit::TestCase

  def test_surface_area
    assert_equal(58, surface_area(2, 3, 4))
    assert_equal(43, surface_area(1, 1, 10))
  end

  def test_parse_dimensions
    assert_equal([3, 11, 24], parse_dimensions("3x11x24"))
  end

end

lines = File.readlines("input.txt")
surface_area = 0
lines.each do |line|
  dimensions = parse_dimensions(line.chomp)
  surface_area += surface_area(*dimensions)
end

puts "Total surface area %s" % surface_area



