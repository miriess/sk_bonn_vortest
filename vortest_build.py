"""Skriptung für die Übungsblatterstellung"""

from vortest import TestMath

from sympy import *

x = symbols('x')

M = TestMath('mathStart_170209')
M.bruch(12)
M.SP(12)
M.quadG(12)
for i in range(8):
    M.lgsEq(dim=2, entryrange=10, maxdet=12)
for i in range(4):
    M.lgsEq(dim=3)
M.final(cleanup=0)
