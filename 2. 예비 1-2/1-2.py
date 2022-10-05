''' Mealy Machine 시뮬레이터 '''
class MealyM:
	'''
	active: 실행시킬 수 있는 DFA인가? (boolean)
	Qlst(Q-list): 상태들의 유한 집합 (list)
	Slst(Sigma-list): 입력문자들의 유한 집합 (list)
	Plst(Pi-list): 출력문자들의 유한 집합 (list)
	ddic(delta-dictionary): 상태변화함수. (qX, sX) tuple을 key로, qY를 value로 하는 dictionary (dict)
	ldic(lambda-dictionary): 출력함수. (qX, sX) tuple을 key로, pX를 value로 하는 dictionary (dict)
	qzr(q-zero): 초기 상태 (str)
	
	active는 정상적인 상황에서 True이며, ErrorMessage에 진입하였을 때 False가 된다.
	Qlst, Slst, Plst는 중괄호 ({})을 슬라이싱한 후 ', '을 기준으로 스플릿하면 입력을 원소로 가지는 list가 된다.
	ddic와 ldic은 마찬가지로 슬라이싱/스플릿 과정을 거친 후 in2df 메서드를 이용하여 dict type, 혹은 ErrorMessage를 return한다.
	qzr은 입력된 값이 Qlst에 있다면 입력된 값을, Qlst에 없다면 ErrorMessage를 return한다.
	'''
	def __init__(self, Q, SIG, PI, delta, lam, qz):
		self.active = True
		self.Qlst = Q[1:len(Q) - 1].split(", ")
		self.Slst = SIG[1:len(SIG) - 1].split(", ")
		self.Plst = PI[1:len(PI) - 1].split(", ")
		self.ddic = self.in2df(delta[1:len(delta) - 1].split(", "), 0)
		self.ldic = self.in2df(lam[1:len(lam) - 1].split(", "), 1)
		self.qzr = qz if qz in self.Qlst else self.ErrorMessage(6)
	
	'''
	in2df: input을 dictionary type으로 변환하는 메서드
	flag 값에 따라 Q를 가져와야 할지, Pi를 가져와야 할지가 결정된다.
	
	newfun은 {X|Y|Z} 형식으로 X in Qlst / Y in Slst / Z in Qlst or Plst를 검사하여
	정상적인 상황이 아닐 시에 알맞은 ErrorMessage(n)을 호출한다.
	알맞은 경우에는 (X, Y) tuple을 value로, Z를 key로 가지는 원소들을 dic에 넣고 return한다.
	'''
	def in2df(self, newfun, flag):
		dic = dict()
		tmp = list()
		lst = self.Qlst if flag == 0 else self.Plst
		for str in newfun:
			tmp = str.split("|")
			if tmp[0] not in self.Qlst:
				self.ErrorMessage(1 + flag * 2)
			elif tmp[1] not in self.Slst:
				self.ErrorMessage(2 + flag * 2)
			elif tmp[2] not in lst:
				self.ErrorMessage(1 + flag * 4)
			else:
				dic[(tmp[0], tmp[1])] = tmp[2]
		return dic
	
	'''
	act: Mealy Machine를 string을 통해 실행
	Mealy Mahcine을 시뮬레이팅한다.
	만약 (state, x[i])가 delta 혹은 lambda function의 정의역에 존재하지 않는다면 None을 반환한다.
	'''
	def act(self, x):
		if x == "-1":
			self.active = False
			return None
		state = self.qzr
		for i in range(len(x)):
			if (state, x[i]) not in self.ddic or (state, x[i]) not in self.ldic:
				return None
			else:
				print("state:", state, "input:", x[i], "output:", self.ldic[(state, x[i])])
				state = self.ddic[(state, x[i])]
				
	'''
	ErrorMessage: num에 따라 알맞은 오류 메시지를 출력하는 메서드
	active를 False로 바꿔준다. num은 다음과 같은 case를 의미한다.
	1: q_n not in Q in delta function
	2: s_n not in SIGMA in delta function
	3: q_n not in Q in lambda function
	4: s_n not in SIGMA in lambda function
	5: p_n not in PI in lambda function
	6: q_0 not in Q
	'''
	def ErrorMessage(self, num):
		self.active = False
		Errorname = ["상태변화함수 오류", "출력함수 오류", "초기상태 오류"]
		Errordetail = ["Q에 존재하지 않는 상태 입력", "SIGMA에 존재하지 않는 입력문자 입력", "PI에 존재하지 않는 출력문자 입력"]
		if num <= 2:
			return print(Errorname[0] + ": " + Errordetail[num - 1])
		elif num <= 5:
			return print(Errorname[1] + ": " + Errordetail[num - 3])
		elif num == 6:
			return print(Errorname[2] + ": " + Errordetail[0])
		else:
			return None
		
print("\nMealy Machine 시뮬레이터입니다. 입력 예시, 방식은 다음과 같습니다.")
print("Q: {q0, q1, q2, ...}")
print("SIGMA: {s0, s1, s2, ...}")
print("PI: {p1, p2, p3, ...}")
print("delta: {qX|sY|qZ, qA|sB|qC, ...}")
print("lambda: {qX|sY|pZ, qA|sB|pC, ...}")
print("q0: qN")
print("string: a0a1a2a3...")
print("종료하실 때는 string에 -1을 입력해주세요\n")
Q = input("Q: ")
SIG = input("SIGMA: ")
PI = input("PI: ")
delta = input("delta: ")
lam = input("lambda: ")
qz = input("q0: ")

D = MealyM(Q, SIG, PI, delta, lam, qz)

while D.active:
	x = input("\nstring: ")
	D.act(x)