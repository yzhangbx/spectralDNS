__author__ = "Mikael Mortensen <mikaem@math.uio.no>"
__date__ = "2014-11-07"
__copyright__ = "Copyright (C) 2014-2016 " + __author__
__license__  = "GNU Lesser GPL version 3 or any later version"

from .create_profile import create_profile
from .memoryprofiler import MemoryUsage
from time import time

class Timer(object):

    def __init__(self):
        self.fastest_timestep = 1e8
        self.slowest_timestep = 0
        self.t0 = time()
        self.tic = self.t0
        
    def __call__(self):
        self.t1 = time()
        dt = self.t1 - self.t0
        self.fastest_timestep = min(dt, self.fastest_timestep)
        self.slowest_timestep = max(dt, self.slowest_timestep)
        self.t0 = self.t1

    def final(self, MPI, rank):
        # Get min/max of fastest and slowest process
        comm = MPI.COMM_WORLD
        fast = (comm.reduce(self.fastest_timestep, op=MPI.MIN, root=0),
                comm.reduce(self.slowest_timestep, op=MPI.MIN, root=0))
        slow = (comm.reduce(self.fastest_timestep, op=MPI.MAX, root=0),
                comm.reduce(self.slowest_timestep, op=MPI.MAX, root=0))
        
        toc = time() - self.tic
        if rank == 0:
            print("Time = {}".format(toc))
            print("Fastest = {}".format(fast))
            print("Slowest = {}".format(slow))

def reset_profile(prof):
    prof.code_map = {}
    prof.last_time = {}
    prof.enable_count = 0
    for func in prof.functions:
        prof.add_function(func)
