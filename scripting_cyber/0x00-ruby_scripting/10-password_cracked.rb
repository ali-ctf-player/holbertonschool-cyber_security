#!/usr/bin/env ruby
require 'digest'

if ARGV.length < 2
  puts "Usage: 10-password_cracked.rb HASHED_PASSWORD DICTIONARY_FILE"
  exit
end

hashed_password = ARGV[0]
dictionary_file = ARGV[1]

found = false

File.foreach(dictionary_file) do |word|
  word = word.chomp
  if Digest::SHA256.hexdigest(word) == hashed_password
    puts "Password found: #{word}"
    found = true
    break
  end
end

puts "Password not found in dictionary." unless found
