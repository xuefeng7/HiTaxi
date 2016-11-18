
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


# create command lines
command_list = []

for index in 0..11
	command_list << "python trip_processing.py #{index}"
end 

launcher = Launcher.new(command_list)
launcher.execute()