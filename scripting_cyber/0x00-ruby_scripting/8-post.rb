require 'net/http'
require 'json'

def post_request(url, body_params = {})
  uri = URI(url)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = uri.scheme == 'https'

  request = Net::HTTP::Post.new(uri.path, 'Content-Type' => 'application/json')
  request.body = JSON.generate(body_params)

  response = http.request(request)

  parsed = JSON.parse(response.body)

  puts "Response status: #{response.code} #{response.message}"
  puts "Response body:"
  if parsed.empty?
    puts "{}"
  else
    puts JSON.pretty_generate(parsed)
  end
end
