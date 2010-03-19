#!/usr/bin/env python

from egfrd import *
from bd import *
from surface import *
from gfrdbase import *
from logger import *
import sys


N = 300

L = 5e-6
#L = 2e-6
#L = 5e-8
#L = 3e-7

w = World(L, int((N * 6) ** (1. / 3.)))
s = EGFRDSimulator(w)
#s = BDSimulator()


box1 = CuboidalRegion([0,0,0], [L,L,L])
# not supported yet
#s.addSurface(box1)

m = ParticleModel()
S = m.new_species_type('S', 1.5e-12, 5e-9)
P = m.new_species_type('P', 1e-12, 7e-9)
r1 = createBindingReactionRule(S, S, P, 1e7 / N_A)
r2 = createUnbindingReactionRule(P, S, S, 1e3)
m.network_rules.add_reaction_rule(r1)
m.network_rules.add_reaction_rule(r2)
m.set_all_repulsive()

s.setModel(m)

s.throwInParticles(S, N / 2, box1)
s.throwInParticles(P, N / 2, box1)

l = Logger(s, 'dimer')
l.setParticleOutInterval(1e-7)
l.log()


#while s.t < 100:
#    s.step()

#s.dumpPopulation()
#l.log()

import myrandom
myrandom.seed(0)


def profrun():
    #while s.stepCounter < 6000:
    for _ in xrange(15000):
        s.step()
        #l.log()
        #logging.info(s.dumpPopulation())

PROFMODE=True

if PROFMODE:
    try:
        import cProfile as profile
    except:
        import profile
    profile.run('profrun()', 'fooprof')
    s.print_report()

    import pstats
    pstats.Stats('fooprof').sort_stats('time').print_stats(40)

else:
    profrun()
    s.print_report()
