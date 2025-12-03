require "test/unit"
require "digest"

def increment_until_suffix_found(key)
  suffix = 1

  loop do
    hash = Digest::MD5.hexdigest key + suffix.to_s
    break if has_five_leading_zeroes(hash)
    suffix +=1
  end

  suffix
end

def has_five_leading_zeroes(string)
  string[0, 5] == "00000"
end

class MyTest < Test::Unit::TestCase

  def test_has_five_leading_zeroes
    key = "00000abcdef"
    assert_true(has_five_leading_zeroes(key))
  end

  def test_increment_until_suffix_found
    key = "abcdef"
    assert_equal(609043, increment_until_suffix_found(key))
  end
  
end


input = "iwrupvqb"
puts "Lowest positive number: %s" % increment_until_suffix_found(input)
