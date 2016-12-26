# -*- coding: utf-8 -*-

from pyparsing import *

expr = Forward()
expr_final = Forward()

coef = Word(nums) + Word(alphas)
numero = Word(nums)
espacos = OneOrMore(White()).suppress()
mais = Literal('+')
menos = Literal('-')
igual = Literal('=')
operator = mais | menos

atomo = numero | coef

expr << ( atomo |
		 atomo + espacos + operator + espacos + atomo)

expr_final << (Group(expr) + espacos + igual + espacos + numero)

op = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
}



print expr_final.parseString(raw_input('Digite a equacao: '))