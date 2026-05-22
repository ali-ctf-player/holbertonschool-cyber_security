require 'json'

def count_user_ids(path)
  data = JSON.parse(File.read(path))
  
  counts = Hash.new(0)
  data.each { |entry| counts[entry["userId"]] += 1 }
  
  counts.sort.each { |user_id, count| puts "#{user_id}: #{count}" }
end
