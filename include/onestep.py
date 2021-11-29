import math
import sys
import numpy as np
import scipy.optimize as sciopt
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ml_params_onestep_steady import STATE_BOUNDS

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times'],'size' : 20})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

class OneStep:
    
    # TODO : Appropriately name private variables
    # Only one instance will ever be created. But still doing per-instance
    # https://stackoverflow.com/questions/2714573/instance-variables-vs-class-variables-in-python
    def __init__(self,options):
        # Close any existing plots
        plt.close()

        self.options = options 
        # Unpack options
        self.Tin = self.options.Tin
        self.HV_p = self.options.HV_p
        self.E_a_p = self.options.E_a_p
        self.Da_p_min = self.options.Da_p_min
        self.min_log_Da = math.log10(self.Da_p_min)
        self.end_episode = False
        self.render_from = self.options.render_from

	# set default values
        self.iteration = 0

        # calculate range of S-Curve
        self.min_T = sciopt.brentq(lambda T: 1 - T + (1 - T + self.HV_p)*(self.Da_p_min)*math.exp(-self.E_a_p/T),1.,1+self.HV_p)
        self.T_p = self.min_T + 0.2
        self.log_Da_p = 0
        self.advance()

        # Max temperature is just as much away from fully burnt as min temperature is from unburnt
        self.max_T = (1. + self.HV_p)/self.min_T 
        self.max_log_Da = sciopt.brentq(lambda log_Da_p: 1 - self.max_T + (1 - self.max_T + self.HV_p)*(10**log_Da_p)*math.exp(-self.E_a_p/self.max_T),-100., 100.)

        # Print intervals
        print "Damkohler number range: ", self.min_log_Da, self.max_log_Da
        print "Temperature range: ", self.min_T, self.max_T

        # Get S-Curve
        print "Computing S-Curve for given reactor..."
        self.get_s_curve()

        # Show S-Curve
        self.show_s_curve()

    # TODO : Correct error handling
    def advance(self):
        # Solve steady-state equation
        # http://seitzman.gatech.edu/classes/ae6766/WellStirredReactor.pdf, Slide 8 
	x0, r = sciopt.brentq(lambda log_Da_p: 1 - self.T_p + (1 - self.T_p + self.HV_p)*(10**log_Da_p)*math.exp(-self.E_a_p/self.T_p),-100.,100.,full_output=True)
        if (r.converged):
	    self.log_Da_p = x0
        else:
            print "Root finding algorithm failed to converge"
            sys.exit() 

    # accessors
    def get_Da_p(self):
	return 10**self.log_Da_p

    def temperature(self):
        return self.Tin*self.T_p

    def get_time(self):
        return self.iteration

    # render related function

    def get_s_curve(self):
        self.sy = np.linspace(self.min_T,self.max_T,50)
  
        func = lambda x : sciopt.brentq(lambda log_Da_p: 1 - x + (1 - x + self.HV_p)*(10**log_Da_p)*math.exp(-self.E_a_p/x),
               -100.,100.)
        self.sx = 10**np.array(map(func,self.sy))

    def show_s_curve(self):
        with sns.axes_style("darkgrid"):
            self.fig, self.ax = plt.subplots(1,1)
        # Plot details
        #plt.title('S-Curve')
        plt.xlabel(r'Da',fontsize=20)
        plt.ylabel(r'$T/T_{in}$',fontsize=20)

        plt.semilogx(self.sx,self.sy,label='_nolegend_')
        self.ax.set(xscale='log')
        #sns.lineplot(x=self.sx, y=self.sy)
        self.ax.set_xlim(10**self.min_log_Da, 10**self.max_log_Da)
        self.ax.set_ylim(self.min_T, self.max_T)
        self.fig.set_facecolor((1,1,1))
        self.ax.hold(True)
        # Draw sweet spot
        # self.ax.add_patch(patches.Rectangle((10**(self.min_log_Da + 1.),STATE_BOUNDS[1]/self.Tin),
        #                   10**(self.max_log_Da - 1.) - 10**(self.min_log_Da + 1.),
        #                   (STATE_BOUNDS[2]-STATE_BOUNDS[1])/self.Tin,fill=False))
        plt.semilogx([1e-3,1e10], [STATE_BOUNDS[1]/self.Tin,STATE_BOUNDS[1]/self.Tin],'k--',label='_nolegend_')
        plt.semilogx([1e-3, 1e10], [(STATE_BOUNDS[2])/self.Tin, (STATE_BOUNDS[2])/self.Tin],'k--',label='_nolegend_')

        # self.ax.annotate('Target, High Reward', xy=(10**(self.max_log_Da - 4.), STATE_BOUNDS[2]/self.Tin),
        #                  xytext=(10**(self.max_log_Da - 5.), STATE_BOUNDS[2]/self.Tin + 1.0),
        #                  arrowprops=dict(facecolor='black', shrink=0.05),)
        self.text = plt.text(10 ** (self.max_log_Da - 6.), STATE_BOUNDS[2] / self.Tin + 0.1, 'Target  (High Reward)', fontsize=16)
        # Create updated objects
        #self.point =
        self.text = plt.text(self.Da_p_min*2,self.HV_p*1.1,'Episode %d' % self.render_from, fontsize=16)
        #self.text = plt.text(self.Da_p_min*2,self.HV_p,'n = %d' % self.iteration, fontsize=16)

    # TODO : Convert to graphical plot
    def render(self):
        print "Da_p: ", self.get_Da_p(), "temp: ", self.temperature(), "iteration: ", self.get_time()
        # self.point.set_data(self.get_Da_p(),self.T_p)

        # self.text.set_text('n = %d' % self.iteration)
        if (self.options.write_plots):
            if (self.iteration % 50 == 0):
                self.ax.plot(self.get_Da_p(), self.T_p, 'o', markersize=10, label='n = ' + str(self.iteration))[0]
                if (self.render_from == 100):
                    self.ax.set_xlabel(r'Da', fontsize=20, color = 'black')
                    for i in self.ax.get_yticklabels():
                        i.set_color('black')
                # else:
                #     self.ax.set_xlabel(r'Da', fontsize=20, color = 'white')
                #     for i in self.ax.get_xticklabels():
                #         i.set_color('white')
                if (self.iteration == 0):
                    self.ax.set_ylabel(r'$T/T_{in}$', fontsize=20, color = 'black')
                    for i in self.ax.get_yticklabels():
                        i.set_color('black')
                # else:
                #     self.ax.set_ylabel(r'$T/T_{in}$', fontsize=20, color = 'white')
                #     for i in self.ax.get_yticklabels():
                #         i.set_color('white')
                self.ax.set(xscale='log')
                self.ax.legend(fontsize=12)
                self.fig.savefig('figs/rl_%d.pdf' % self.iteration,bbox_inches='tight')
        else:
            self.fig.canvas.draw()
            plt.pause(0.001)

    # simulation environment

    # Logarithmic variation of Damkohler number
    def step(self,action,ACTION_STEP):
	# Set temperature change based on action
	if (action == 0):
	    self.T_p = self.T_p - ACTION_STEP
	elif (action == 2):
	    self.T_p = self.T_p + ACTION_STEP
        # End episode if outside temperature range
        if (self.T_p <= self.min_T or self.T_p >= self.max_T):
            self.end_episode = True
            return 1

        self.iteration += 1
	self.advance()
	return 1

	 
