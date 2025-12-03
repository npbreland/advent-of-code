require "test/unit"

def count_vowels(string)
  vowels = "aeiou"
  string.split("").reduce(0) { |sum, c| (vowels.include? c) ? sum + 1 : sum }
end

def has_at_least_three_vowels(string)
  count_vowels(string) >= 3
end

def contains_letter_twice_in_a_row(string)
  buffer = nil
  string.split("").each do |c|
    if buffer == nil
      buffer = c
    elsif c == buffer
      return true
    else
      buffer = c
    end
  end

  false
end

def contains_naughty_string(string)
  naughty_strings = ["ab", "cd", "pq", "xy"]

  i = 0
  loop do
    break if i == string.length - 1

    pair = string[i, 2]
    return true if naughty_strings.include? pair

    i += 1
  end

  return false
end

def string_is_nice(string)
  return has_at_least_three_vowels(string) &&
    contains_letter_twice_in_a_row(string) &&
    !contains_naughty_string(string)
end

class MyTest < Test::Unit::TestCase
  def test_count_vowels
    assert_equal(2, count_vowels("ae"))
    assert_equal(0, count_vowels("xyx"))
    assert_equal(3, count_vowels("abcdefghi"))
  end

  def test_has_at_least_three_vowels
    assert_false(has_at_least_three_vowels("ae"))
    assert_false(has_at_least_three_vowels("xyx"))
    assert_true(has_at_least_three_vowels("abcdefghi"))
  end

  def test_contains_letter_twice_in_a_row
    assert_false(contains_letter_twice_in_a_row("ae"))
    assert_false(contains_letter_twice_in_a_row("abcdefghi"))
    assert_true(contains_letter_twice_in_a_row("xyxx"))
  end

  def test_contains_naughty_strings
    assert_true(contains_naughty_string("haegwjzuvuyypxyu"))
    assert_false(contains_naughty_string("jchzalrnumimnmhp"))
    assert_true(contains_naughty_string("jchzalrnumimnpqmhp"))
  end

  def test_string_is_nice
    assert_true(string_is_nice("ugknbfddgicrmopn"))
    assert_true(string_is_nice("aaa"))
    assert_false(string_is_nice("jchzalrnumimnmhp"))
    assert_false(string_is_nice("haegwjzuvuyypxyu"))
    assert_false(string_is_nice("dvszwmarrgswjxmb"))
  end
end

lines = File.readlines("input.txt")
nice_strings = 0
lines.each do |line|
  nice_strings += 1 if string_is_nice(line.chomp)
end

puts "Nice strings: %s" % nice_strings
