# -*- coding: utf8 -*-
import numpy as np
#from sympy import *

# "test log function can be solved?"
# x = Symbol('x')
# expr1 = log(5*x+10,10)
# print solve(expr1,x)
# "conclusion is that the first params is num expression,not symbol expression"

x = Symbol('x')
y = Symbol('y')
# 用来存储代入y之后的方程
z = Symbol ('z')
a = 10 
b = 1.2
max = 61.5
expr1 = y*(max-a*(x+y))-b*y
expr2 = x*(max-a*(x+y))-b*x
print "Follwer function:\n",expr1
print "Leader function:\n",expr2

expr3 = solve(diff(expr1,y),y)
print "constraint between Follower and Leader:\n",expr3[0]

expr4 = solve([y-expr3[0],z-expr2],[y,z])
print "Leader fuction while considering the constraint:\n",expr4[z]
print "output of Leader and Follower:"
print solve([y-expr3[0],diff(expr4[z],x)],[x,y])