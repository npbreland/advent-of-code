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
    elsif
      c == buffer
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

def contains_at_least_two_instances_of_a_pair(string)
  pairs = {}
  last_pair = nil

  i = 0
  loop do
    break if i >= string.length - 1
    pair = string[i, 2]

    # Skip pair if it overlaps
    if pair == last_pair
      # clear last_pair in case they are next to one another, e.g. "wwww"
      last_pair = nil
      i += 1
      next
    end

    if pairs.key?(pair)
      pairs[pair] += 1
    else
      pairs[pair] = 1
    end

    last_pair = pair
    i += 1
  end

  pairs.values.any? { |n| n > 1 }
end

def contains_letter_twice_in_a_row_with_one_in_between(string)

  i = 0
  loop do
    break if i == string.length - 2

    pair = string[i, 3]
    return true if pair[0] == pair[2] && pair[0] != pair[1]

    i += 1
  end

  false
end

def string_is_nice(string)
  return contains_at_least_two_instances_of_a_pair(string) &&
    contains_letter_twice_in_a_row_with_one_in_between(string)
end


class MyTest < Test::Unit::TestCase
  def test_count_vowels
    assert_equal(2, count_vowels("ae"))
    assert_equal(0, count_vowels("xyx"))
    assert_equal(3, count_vowels("abcdefghi"))
  end

  def test_has_at_least_three_vowels
    assert_true(has_at_least_three_vowels("abcdefghi"))

    assert_false(has_at_least_three_vowels("ae"))
    assert_false(has_at_least_three_vowels("xyx"))
  end

  def test_contains_letter_twice_in_a_row
    assert_true(contains_letter_twice_in_a_row("xyxx"))

    assert_false(contains_letter_twice_in_a_row("ae"))
    assert_false(contains_letter_twice_in_a_row("abcdefghi"))
  end

  def test_contains_naughty_strings
    assert_true(contains_naughty_string("haegwjzuvuyypxyu"))
    assert_true(contains_naughty_string("jchzalrnumimnpqmhp"))

    assert_false(contains_naughty_string("jchzalrnumimnmhp"))
  end

  def test_contains_at_least_two_instances_of_a_pair
    assert_true(contains_at_least_two_instances_of_a_pair("xyxy"))
    assert_true(contains_at_least_two_instances_of_a_pair("aabcdefgaa"))
    assert_true(contains_at_least_two_instances_of_a_pair("xxyxx"))
    assert_false(contains_at_least_two_instances_of_a_pair("aaa"))
  end

  def test_contains_letter_twice_in_a_row_with_one_in_between
    assert_true(contains_letter_twice_in_a_row_with_one_in_between("xxyxx"))
    assert_true(contains_letter_twice_in_a_row_with_one_in_between("xyx"))
    assert_true(contains_letter_twice_in_a_row_with_one_in_between("abcdefeghi"))

    assert_false(contains_letter_twice_in_a_row_with_one_in_between("aaa"))
    assert_false(contains_letter_twice_in_a_row_with_one_in_between("uurcxstgmygtbstg"))
  end

  def test_string_is_nice
    assert_true(string_is_nice("qjhvhtzxzqqjkmpb"))
    assert_true(string_is_nice("xxyxx"))
    assert_true(string_is_nice("xckozymymezzarpy"))
    assert_true(string_is_nice("cxoaaphylmlyljjz"))
    assert_true(string_is_nice("rxexcbwhiywwwwnu"))


    assert_false(string_is_nice("uurcxstgmygtbstg"))
    assert_false(string_is_nice("ieodomkazucvgmuy"))

    assert_false(string_is_nice("aaa"))
  end

end

lines = File.readlines("input.txt")
nice_strings = 0

lines.each do |line|
  nice_strings += 1 if string_is_nice(line.chomp)
end

puts "Nice strings: %s" % nice_strings
