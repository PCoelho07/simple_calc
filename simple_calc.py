# -*- coding: utf-8 -*-

from pyparsing import *

def BNF():
	global bnf

	coef = Combine(Word(nums) + Word(alphas))
	numero = Word(nums)
	espacos = OneOrMore(White()).suppress()
	mais = Literal('+')
	menos = Literal('-')
	igual = Literal('=')
	operator = (mais | menos)
	atomo = (coef | numero)

	expr = Forward()
	expr_final = Forward()

	expr <<	atomo + ZeroOrMore(operator + atomo)

	expr_final << expr + igual + numero

	bnf = expr_final
	return bnf


def handle_terms(parsed_expr):
 	coef_list = []
 	numbers = []
 	for st in parsed_expr:
 		if st.find("x") > -1:
 			coef_list.append(st)
 		elif isinstance(int(st), int) :
 			numbers.append(st)
 	
 	return numbers, coef_list





op = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
}



if __name__ == '__main__':
	psrd_expr = BNF().parseString(raw_input('Digite a equacao: '))
	print handle_terms(psrd_expr)