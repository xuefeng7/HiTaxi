
class Launcher

  def initialize(commands_list)
    #Expected to be an array of command string
    @commands_list = commands_list
  end

    def execute
    p_threads = @commands_list.map do |command|
      Process.detach(Process.spawn(command))
    end
    p_threads.each(&:join)
   end

end

# offset lists
offset = [8, 308, 608, 908, 1208, 1508]
# skip lists
skip = [0, 14242, 8232, 0, 0, 2970]
# create command lines
command_list = []

for index in 0..5
	command_list << "python trip_processing.py #{index} #{offset[index]} #{skip[index]}"
end 

launcher = Launcher.new(command_list)
launcher.execute()