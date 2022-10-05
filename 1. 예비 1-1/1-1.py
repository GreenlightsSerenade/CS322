''' DFA 시뮬레이터 '''
class DFA:
	'''
	active: 실행시킬 수 있는 DFA인가? (boolean)
	Qlst(Q-list): 상태들의 유한 집합 (list)
	Slst(Sigma-list): 입력 문자들의 유한 집합 (list)
	ddic(delta-dictionary): 상태변화함수. (qN, sM) tuple을 key로, qM을 Value로 하는 dictionary (dict)
	qzr(q-zero): 초기 상태 (str)
	Flst(Final-list): 최종 상태들의 유한 집합 (list)
	
	active는 정상적인 상황에서 True이며, ErrorMessage에 진입하였을 때 False가 된다.
	Qlst와 Slst는 중괄호 ({})을 슬라이싱한 후 ', '을 기준으로 스플릿하면 입력을 원소로 가지는 list가 된다.
	ddic은 마찬가지로 슬라이싱/스플릿 과정을 거친 후 in2df 메서드를 이용하여 dict type, 혹은 ErrorMessage(1 or 2)를 return한다.
	qzr은 입력된 값이 Qlst에 있다면 입력된 값을, Qlst에 없다면 ErrorMessage(3)를 return한다.
	Flst는 Flstcheck 메서드를 통해 검사를 거친 후 list type, 혹은 ErrorMessage(4)를 return한다.
	'''
	def __init__(self, Q, SIG, delta, qz, Fin):
		self.active = True
		self.Qlst = Q[1:len(Q) - 1].split(", ")
		self.Slst = SIG[1:len(SIG) - 1].split(", ")
		self.ddic = self.in2df(delta[1:len(delta) - 1].split(", "))
		self.qzr = qz if qz in self.Qlst else self.ErrorMessage(3)
		self.Flst = self.Flstcheck(Fin)
	
	'''
	in2df: input을 dictionary type으로 변환하는 메서드
	newdel은 {qX|sY|sZ(d(qX, sY) = sZ), qA|sB| (d(qA, sB) = e),...} 형식으로
	입력된 input을 슬라이싱/스플릿하여 'X|Y|Z' (Z는 공백일 수 있음) 와 같은 형태의 string을 원소로 가지는 list이다
	이 원소들을 다시 |을 매개로 스플릿하여 3개의 원소를 가지는 list로 만든 후, 몇 개의 검사를 거친다.
	1. tmp[0](X)가 Qlst에 없거나, tmp[2](Z)이 공백이 아니면서 Qlst에 없다면 ErrorMessage(1)
	2. tmp[1](Y)이 Slst에 없다면 ErrorMessage(2)
	이 검사를 거친 후 Error 조건을 만족하지 않는다면, (X, Y) tuple을 value로, Z를 key로 가지는 원소들을 dic에 넣고 return한다.
	'''
	def in2df(self, newdel):
		dic = dict()
		tmp = list()
		for str in newdel:
			tmp = str.split("|")
			if tmp[0] not in self.Qlst or (tmp[2] not in self.Qlst and tmp[2] != " "):
				self.ErrorMessage(1)
			elif tmp[1] not in self.Slst:
				self.ErrorMessage(2)
			dic[(tmp[0], tmp[1])] = tmp[2]
		return dic	
	
	'''
	Flstcheck: 입력(Fin)을 검사하여 정상적이라면 list를, 아니라면 ErrorMessage를 return
	입력을 슬라이싱/스플릿 한 후, set type을 형변환하여
	F - Qlst가 공집합이라면 (F in Q) list를
	공집합이 아니라면 (F not in Q) ErrorMessage(4)를 return한다
	'''
	def Flstcheck(self, Fin):
		tmp = Fin[1:len(Fin) - 1].split(", ")
		if len(set(tmp) - set(self.Qlst)) == 0:
			return tmp
		else:
			return self.ErrorMessage(4)
	
	'''
	act: DFA를 string을 통해 실행
	DFA를 시뮬레이팅한다.
	YES case는 Final state가 Flst의 원소일때
	NO case는 Final state가 Flst의 원소가 아니거나, d(q_n, s_n) = e(epsilon)일 때
	'''
	def act(self, x):
		if x == "-1":
			self.active = False
			return None
		state = self.qzr
		for i in range(len(x)):
			if state == " " or (state, x[i]) not in self.ddic:
				return self.NO()
			else:
				state = self.ddic[(state, x[i])]
				
		if state in self.Flst:
			return self.YES()
		else:
			return self.NO()

	''' YES: "네"를 출력하는 메서드 '''
	def YES(self):
		print("네")
	
	''' NO: "아니요"를 출력하는 메서드 '''
	def NO(self):
		print("아니요")
	
	'''
	ErrorMessage: num에 따라 알맞은 오류 메시지를 출력하는 메서드
	active를 False로 바꿔준다. num은 다음과 같은 case를 의미한다.
	1: q_n not in Q in delta function
	2: s_n not in SIGMA in delta function
	3: q_0 not in Q
	4: F not in Q
	'''
	def ErrorMessage(self, num):
		self.active = False
		if num == 1:
			return print("상태변화함수 오류: Q에 존재하지 않는 state 입력")
		elif num == 2:
			return print("상태변화함수 오류: SIGMA에 존재하지 않는 input symbol 입력")
		elif num == 3:
			return print("Initial state 오류: Q에 존재하지 않는 state 입력")
		elif num == 4:
			return print("Final state 오류: Q에 존재하지 않는 state 입력")
		else:
			return None

print("부분함수를 허용하는 DFA 시뮬레이터입니다. 입력 예시, 방식은 다음과 같습니다.")
print("Q: {q0, q1, q2, ...}")
print("SIGMA: {s0, s1, s2, ...}")
print("delta: {qX|sY|qZ(d(qX, sY) = qZ), qA|sB| (d(qA, sB) = e),...}")
print("q0: qN")
print("F: {qA, qB, ...}")
print("string: a0a1a2a3...")
print("종료하실 때는 string에 -1을 입력해주세요\n")
Q = input("Q: ")
SIG = input("SIGMA: ")
delta = input("delta: ")
qz = input("q0: ")
Fin = input("F: ")

D = DFA(Q, SIG, delta, qz, Fin)

while D.active:
	x = input("\nstring: ")
	D.act(x)