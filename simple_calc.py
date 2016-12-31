# -*- coding: utf-8 -*-

from pyparsing import *
import re

exprStack = []

def pushElement(s, loc, tok):
	exprStack.append(tok[0])
	print(exprStack)

def BNF():
	global bnf

	coef = Combine(Word(nums) + Word(alphas))
	numero = Word(nums)
	espacos = OneOrMore(White()).suppress()
	mais = Literal('+')
	menos = Literal('-')
	igual = Literal('=')
	operator = (mais | menos)
	atomo = (coef | numero).setParseAction(pushElement)

	expr = Forward()
	expr_final = Forward()

	expr <<	atomo + ZeroOrMore((operator + atomo).setParseAction(pushElement))

	expr_final << expr + igual + numero

	bnf = expr_final
	return bnf


def handle_terms(parsed_expr):
 	coef_list = []
 	numbers = []
 	equal = []

 	equal.append(parsed_expr[len(parsed_expr)-1])

 	for st in range(0, len(parsed_expr)-2):
 		if parsed_expr[st].find("x") > -1:
 			coef_list.append(parsed_expr[st])
 		elif parsed_expr[st].isdigit():
 			numbers.append(parsed_expr[st])



 	return numbers, coef_list, equal, parsed_expr


def evaluate(s): 
	op = s.pop()
	if op in "+-":
		op2 = evaluate(s)
		op1 = evaluate(s)
		return operations[op](op1, op2)

	elif re.search('^[0-9]*[a-zA-Z]$', op):
		st = []
		for x in list(op):
			if x.isdigit():
				st.append(x)

		st = ''.join(st)
		return int(st)

	elif op.isdigit():
		return int(op)
		


operations = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
}



if __name__ == '__main__':
	psrd_expr = BNF().parseString(raw_input('Digite a equacao: '))
	print handle_terms(psrd_expr)