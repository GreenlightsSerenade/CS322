import ply.lex as lex
import ply.yacc as yacc
import eNFA2mDFA

# AST Node Class
class AST:
	def __init__(self, value):
		self.left = None
		self.right = None
		self.value = value

'''
lex & yacc part
http://www.dabeaz.com/ply/ply.html 참조
'''
# List of tokens name.	This is always required.
tokens = (
	'LETTER',
	'PLUS',
	'LPAREN',
	'RPAREN',
	'ASTER',
	'NONE'
)

# Regular expression rules for simple tokens
t_LETTER = r"[a-zA-Z0-9]"
t_PLUS = r"\+"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_ASTER = r"\*" 
t_NONE = r"\(\)"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Syntax Diagram
precedence = (
	('left', 'PLUS'),
	('left', 'ASTER')
)

def p_expression(p):
	'expression : term'
	p[0] = p[1]

def p_term(p):
	'term : factor'
	p[0] = p[1]

def p_factor(p):
	'factor : LETTER'
	p[0] = p[1]
	
def p_none(p):
	'factor : NONE'
	p[0] = "EPSILON"
	
def p_plus(p):
	'expression : expression PLUS term'
	p[0] = ['+', [p[1], p[3]]]

def p_series(p):
	'term : term factor'
	p[0] = ["SERIES", [p[1], p[2]]]

def p_parens(p):
	'factor : LPAREN expression RPAREN'
	p[0] = p[2]

def p_asterisk(p):
	'factor : factor ASTER'
	p[0] = ['*', [p[1]]]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

lex.lex()
yacc.yacc()

'''
parse2AST: lex & yacc을 통해 parsing한 list를 AST로 변환하는 함수
만드는 AST는 이진 트리이며, R + S와 RS는 각각 '+' 또는 "SEREIS"가 root, R이 left child, S가 right child인 tree이며
R*은 '*'이 root, R이 left child인 tree가 된다.
AST의 말단 노드는 항상 symbol(LETTER), 혹은 e(EPSILON)이다.
'''
def parse2AST(parse):
	if len(parse) == 1 or parse == "EPSILON":
		return AST(parse)
	else:
		root = AST(parse[0])
		left = parse2AST(parse[1][0])
		root.left = left
		if len(parse[1]) == 2:
			right = parse2AST(parse[1][1])
			root.right = right
		return root

'''
AST2eNFA: AST를 eNFA로 변환하는 함수
root의 값이 + / SERIES / * / symbol(epsilon 포함)로 4가지 case가 있으며
교과서 TP 3장 p12 - p13을 기반으로 프로그래밍하였다.
'''
n = 0 # q_n의 n
def AST2eNFA(root):
	global n
	# 1. R + S
	# 새 state를 두 개 추가하여 하나가 initial state, 하나가 final state이 된다. 그 후
	# 1) 새로운 initial state는 R과 S의 initial state에 e-move를,
	# 2) R과 S의 final states는 새로운 final state에 e-move를 하게 만든다.
	if root.value == '+':
		lefty = AST2eNFA(root.left)		# left child(R)
		righty = AST2eNFA(root.right)	# right child(S)
		lefty.ddic.update(righty.ddic)	# dictionary를 합친다 (새 NFA의 dictionary)
		q0 = "q" + str(n)		# q_initial
		qf = "q" + str(n + 1)	# q_final
		n += 2
		eNFA = eNFA2mDFA.FA(1, lefty.Qset | righty.Qset | {q0, qf}, lefty.Sset | righty.Sset, lefty.ddic , q0, {qf}) # New eNFA
		eNFA.ddic[(q0, 'e')] = {lefty.qzr, righty.qzr} # 1)
		# 2)
		l_fin = list(lefty.Fset)[0]
		r_fin = list(righty.Fset)[0]
		if (l_fin, 'e') in eNFA.ddic:
			eNFA.ddic[(l_fin, 'e')].add(qf)
		else:
			eNFA.ddic[(l_fin, 'e')] = {qf}
		if (r_fin, 'e') in eNFA.ddic:
			eNFA.ddic[(r_fin, 'e')].add(qf)
		else:
			eNFA.ddic[(r_fin, 'e')] = {qf}
		return eNFA
	# 2. RS
	# 새로운 state를 추가하지 않고, R의 initial state가 새 initial state, S의 final state가 새 final state가 된다. 그 후
	# 1) R의 final state는 S의 initial state에 e-move를 하게 만든다
	elif root.value == "SERIES":
		lefty = AST2eNFA(root.left)		# left child(R)
		righty = AST2eNFA(root.right)	# right child(S)
		delta = lefty.ddic.copy()		# new eNFA의 dictionary (update용)
		delta.update(righty.ddic)
		# 1)
		l_fin = list(lefty.Fset)[0]
		if (l_fin, 'e') in delta:
			detla[(l_fin, 'e')].add(righty.qzr)
		else:
			delta[(l_fin, 'e')] = {righty.qzr}
		return eNFA2mDFA.FA(1, lefty.Qset | righty.Qset, lefty.Sset | righty.Sset, delta, lefty.qzr, righty.Fset)
	# 3. R*
	# 새 state를 두 개 추가하여 하나가 initial state, 하나가 final state이 된다. 그 후
	# 1) 새로운 initial state와 2) R의 final state 모두 R의 initial state와 새 final state에 e-move를 하게 만든다.
	elif root.value == '*':
		child = AST2eNFA(root.left)	# child(R)
		q0 = "q" + str(n)		# q_initial
		qf = "q" + str(n + 1)	# q_final
		n += 2
		eNFA = eNFA2mDFA.FA(1, child.Qset | {q0, qf}, child.Sset, child.ddic, q0, {qf})	# new eNFA
		eNFA.ddic[(q0, 'e')] = {child.qzr, qf} # 1)
		# 2)
		fin = list(child.Fset)[0]
		if (fin, 'e') in eNFA.ddic:
			eNFA.ddic[(fin, 'e')].add(child.qzr)
			eNFA.ddic[(fin, 'e')].add(qf)
		else:
			eNFA.ddic[(fin, 'e')] = {child.qzr, qf}
		return eNFA
	# 4. basis (epsilon or symbol)
	# 새 state를 두 개 추가하여 하나가 initial state, 하나가 final state이 된다. 그 후
	# 1) delta(q0, symbol(or epsilon)) = qf
	else:
		eNFA = eNFA2mDFA.FA(0, 0, 0, 0, 0, 0) # new eNFA
		q0 = "q" + str(n)		# q_initial
		qf = "q" + str(n + 1)	# q_final
		n += 2
		eNFA.Qset.add(q0)
		eNFA.Qset.add(qf) # add states in Qset
		if root.value == "EPSILON":	# epsilon
			eNFA.ddic[(q0, 'e')] = {qf}
		else:						# symbol
			eNFA.Sset.add(root.value)
			eNFA.ddic[(q0, root.value)] = {qf}
		eNFA.qzr = q0		# set initial
		eNFA.Fset.add(qf)	# set final
		return eNFA

print("RE to m-DFA 변환기입니다. Epsilon move는 ()입니다.")
string = input("Regular Expression: ")
parse = yacc.parse(string)
root = parse2AST(parse)
eNFA = AST2eNFA(root)
mDFA = eNFA2mDFA.eNFA2mDFA(eNFA)
mDFA.printing()
x = input("\nPlease press enter to exit: ")
