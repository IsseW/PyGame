import re
import parser
import re
from math import sin
from math import cos
from math import tan
from math import asin
from math import acos
from math import atan
from math import log
from math import floor
from math import ceil
from math import gamma
from math import sqrt


e = 2.71828182846
π = pi = 3.14159265359
τ = tau = 2 * pi

def ParseDifferential(input):
	input = input.replace('^', '**').replace('factorial(', 'gamma(1 +').replace('ceiling', 'ceil').replace('y', 'F')
	eq = parser.expr(input).compile()
	return eq

class DiffFunction:
	def __init__(self, input):
		self.equation = ParseDifferential(input)
	def getDerivative(self, value):
		F = value
		return eval(self.equation)
	def getValues(self, startX, startY, min, max, step):
		values = [ ]
		F = startY
		min = min - startX;
		max = max - startX
		ymin = startY
		ymax = startY
		if max < 0:
			for i in range(1, floor(-max / step)):
				x = startX - i * step
				der = eval(self.equation)
				F = F - der * step
			for i in range(1, floor(-min / step)):
				x = max - i * step
				der = eval(self.equation)
				F = F - der * step
				values.append(F)
				if F < ymin: ymin = F
				elif F > ymax: ymax = F
			values = values[::-1]
			values.append(startY)
		elif min > 0:
			for i in range(1, floor(min / step)):
				x = startX + i * step
				der = eval(self.equation)
				F = F + der * step
			for i in range(1, floor(max / step)):
				x = min + i * step
				der = eval(self.equation)
				F = F + der * step
				values.append(F)
				if F < ymin: ymin = F
				elif F > ymax: ymax = F
		else:
			for i in range(1, floor(-min / step)):
				x = startX - i * step
				der = eval(self.equation)
				F = F - der * step
				values.append(F)
				if F < ymin: ymin = F
				elif F > ymax: ymax = F
			values = values[::-1]
			F = startY
			values.append(F)
			for i in range(1, floor(max / step)):
				x = startX + i * step
				der = eval(self.equation)
				F = F + der * step
				values.append(F)
				if F < ymin: ymin = F
				elif F > ymax: ymax = F
		
		return values, ymin, ymax


f = DiffFunction("pi")
f.getValues(0, 100, -50, 100, 0.01)
