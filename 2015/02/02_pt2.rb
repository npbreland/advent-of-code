require "test/unit"

def surface_area(l, w, h)
  lw = 2*l*w
  wh = 2*w*h
  hl = 2*h*l
  lw + wh + hl + [lw, wh, hl].min / 2
end

def perimeter(l, w)
  2*(l+w)
end

def ribbon_length(l, w, h)
  [perimeter(l, w), perimeter(w, h), perimeter(h, l)].min
end

def bow_length(l, w, h)
  l * w * h
end

def total_ribbon(l, w, h)
  ribbon_length(l, w, h) + bow_length(l, w, h)
end

def parse_dimensions(line)
  line.split("x").map {|d| d.to_i}
end

class MyTest < Test::Unit::TestCase

  def test_surface_area
    assert_equal(58, surface_area(2, 3, 4))
    assert_equal(43, surface_area(1, 1, 10))
  end

  def test_parse_dimensions
    assert_equal([3, 11, 24], parse_dimensions("3x11x24"))
  end

  def test_perimeter
    assert_equal(10, perimeter(2, 3))
  end

  def test_ribbon_length
    assert_equal(10, ribbon_length(2, 3, 4))
  end

  def test_bow_length
    assert_equal(24, bow_length(2, 3, 4))
  end

  def test_total_ribbon
    assert_equal(34, total_ribbon(2, 3, 4))
    assert_equal(14, total_ribbon(1, 1, 10))
  end

end

lines = File.readlines("input.txt")
total_ribbon = 0
lines.each do |line|
  dimensions = parse_dimensions(line.chomp)
  total_ribbon += total_ribbon(*dimensions)
end

puts "Total feet of ribbon: %s" % total_ribbon



