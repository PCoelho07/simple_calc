# -*- coding: utf-8 -*-

from __future__ import division
from pyparsing import *
import re

exprStack = []


operations = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
}

types = {
	1: 'num',
	2: 'coef',
}

def pushElement(s, loc, tok):
	exprStack.append(tok[0])
	#print(exprStack)

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


def evaluate(s, resultStack): 
	op = s.pop()
	t1 = ' '
	t2 = ' '
	if op in "+-":
		op2, t2 = evaluate(s, resultStack) #
		op1, t1 = evaluate(s, resultStack) #
		if t2 == t1:
			resultStack.append((operations[op](op1, op2), t1))
			return operations[op](op1, op2), t1
		elif t2 != t1:
			resultStack.append((op2, t2))
			resultStack.append((op1, t1))
			return (op2, t2)

	elif re.search('^[0-9]*[a-zA-Z]$', op):
		st = []
		for x in list(op):
			if x.isdigit():
				st.append(x)

		st = ''.join(st)
		resultStack.append((int(st), types[2]))
		return int(st), types[2]

	elif op.isdigit():
		resultStack.append((int(op), types[1]))
		return int(op), types[1]


def calculate(psrd_expr):
	stack = []
	evaluate(exprStack, stack)
	number = 0
	cof = 0

	print(stack)
	term = psrd_expr[len(psrd_expr)-1]

	if len(stack) == 1:
		cof = stack.pop()[0]

	else:
		t1 = stack.pop()
		t2 = stack.pop()

		if t1[1] == 'num':
			number = t1[0]
			cof = t2[0]
		else:
			number = t2[0]
			cof = t1[0]

	if number > 0:
		variable = (int(term) - number)/cof
	else:
		variable = (int(term) + number)/cof

	return variable

	



if __name__ == '__main__':
	psrd_expr = BNF().parseString(raw_input('Digite a equacao: '))
	result = calculate(psrd_expr)
	print("Valor da icognita: " + str(result))

