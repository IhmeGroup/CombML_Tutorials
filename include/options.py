class options:
    # Common attributes
    env_type = ''
    t_fin = 0.0
    output_file = ''
    moves_file = ''
    write_output = False

    # Full reactor attributes
    cti_file = ''
    palette = ''
    mixture = ''
    pres = 101325.0
    temp = 300.0
    phi = 1.0
    volume = 0.01
    fwhm = 0.2
    amplitude = 0.1
    t0 = 0.1
    valve_coefficient = 1.0

    # One-step steady attributes
    Tin = 300.0
    HV_p = 0.0
    E_a_p = 2.0
    Da_p_min = 0.01
    write_plots = False

    def __init__(self,config):

        self.env_type = config["env_type"]
	self.t_fin = config["final_time"]
	self.output_file = config["output_file"]
	self.moves_file = config["moves_file"]
	self.write_output = config["write_output"]

        if (self.env_type == 'full'):
	    self.palette = config["palette"]
	    self.comp = config["composition"]
	    self.cti_file = config["cti_file"]
	    self.mixture = config["mixture_name"]
	    self.phi = config["equivalence_ratio"]
	    self.pres = config["pressure"]
	    self.temp = config["temperature"]
	    self.volume = config["volume"]
	    self.fwhm = config["fwhm"]
	    self.amplitude = config["amplitude"]
	    self.t0 = config["start_time"]
	    self.valve_coefficient = config["valve_coefficient"]

        elif (self.env_type == 'onestep_steady'):
	    self.Tin = config["temperature"]
            self.HV_p = config["non_dimensional_heating_value"]
            self.E_a_p = config["non_dimensional_activation_energy"]
            self.Da_p_min = config["minimum_non_dimensional_damkohler_number"]
            self.write_plots = config["write_plots"]
            self.render_from = config["render_from"]

    def dump(self):
        # Print common attributes
        print "Common Attributes:"
        print "" 
	print "environment type: ", self.env_type
	print "final_time: ", self.t_fin
	print "output_file: ", self.output_file
	print "moves_file: ", self.moves_file
	print "write_output: ", self.write_output

        # Print environment related variables
        print ""
        print "Specific Attributes:"
        print ""

        if (self.env_type == 'full'):
	    print "cti_file: ", self.cti_file
	    print "palette: ", self.palette
	    print "composition: ", self.comp
	    print "mixture_name: ", self.mixture
	    print "equivalence_ratio: ", self.phi
	    print "initial pressure: ", self.pres
	    print "initial temperature: ", self.temp
	    print ""
	    print "combustor volume: ", self.volume
	    print ""
	    print "fwhm: ", self.fwhm
	    print "amplitude: ", self.amplitude
	    print "igniter start time: ", self.t0
	    print ""
	    print "valve coefficient: ", self.valve_coefficient

	elif (self.env_type == 'onestep_steady'):
            print "initial temperature: ", self.Tin
            print "non_dimensional_heating_value: ", self.HV_p
            print "non_dimensional_activation_energy: ", self.E_a_p
            print "minimum_non_dimensional_damkohler_number: ", self.Da_p_min
            print "write_plots: ", self.write_plots

