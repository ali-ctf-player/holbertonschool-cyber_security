#!/usr/bin/env ruby
require 'optparse'

TASKS_FILE = 'tasks.txt'

def load_tasks
  File.exist?(TASKS_FILE) ? File.readlines(TASKS_FILE, chomp: true) : []
end

def save_tasks(tasks)
  File.write(TASKS_FILE, tasks.join("\n") + (tasks.empty? ? "" : "\n"))
end

def add_task(task)
  tasks = load_tasks
  tasks << task
  save_tasks(tasks)
  puts "Task '#{task}' added."
end

def list_tasks
  tasks = load_tasks
  puts "Tasks:"
  tasks.each_with_index { |task, i| puts "#{i + 1}. #{task}" }
end

def remove_task(index)
  tasks = load_tasks
  removed = tasks.delete_at(index - 1)
  if removed
    save_tasks(tasks)
    puts "Task '#{removed}' removed."
  else
    puts "Invalid index."
  end
end

OptionParser.new do |opts|
  opts.banner = "Usage: cli.rb [options]"

  opts.on("-a", "--add TASK", "Add a new task") { |task| add_task(task) }
  opts.on("-l", "--list", "List all tasks") { list_tasks }
  opts.on("-r", "--remove INDEX", Integer, "Remove a task by index") { |i| remove_task(i) }
  opts.on("-h", "--help", "Show help") { puts opts; exit }

  opts.parse!(ARGV)
end
