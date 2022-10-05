import operator

''' e-NFA to m-DFA 변환기 '''
class FA:
	'''
	active: 실행시킬 수 있는 FA인가? (boolean)
	run: 어떤 방식으로 입력받을 것인가? (boolean)
	Qset(Q-set): 상태들의 유한 집합 (set)
	Sset(Sigma-set): 입력 문자들의 유한 집합 (set)
	ddic(delta-dictionary): 상태변화함수. (qN, sM) tuple을 key로, qM을 Value로 하는 dictionary (dict)
	qzr(q-zero): 초기 상태 (str)
	Fset(Final-set): 최종 상태들의 유한 집합 (set)
	
	run이 1일 때 입력된 Q, SIG, delta, qz, Fin을 적당한 작업을 통해 Qset, Sset, ddic, qzr, Fset으로 변환한다.
	1이 아닐 때는 모두 초기 상태로 설정한다. 이는 처음 선언에 데이터를 입력하지 않고, 나중에 직접적인 접근을 하기 위해서이다.
	active는 정상적인 상황에서 True이며, ErrorMessage에 진입하였을 때 False가 된다.
	Qset와 Sset는 중괄호 ({})을 슬라이싱한 후 ', '을 기준으로 스플릿하면 입력을 원소로 가지는 list가 되며, 그를 set으로 형변환 된다.
	ddic은 마찬가지로 슬라이싱/스플릿 과정을 거친 후 in2df 메서드를 이용하여 dict type, 혹은 ErrorMessage(1 or 2)를 return한다.
	qzr은 입력된 값이 Qset에 있다면 입력된 값을, Qset에 없다면 ErrorMessage(3)를 return한다.
	Fset는 Fsetcheck 메서드를 통해 검사를 거친 후 set type, 혹은 ErrorMessage(4)를 return한다.
	'''
	def __init__(self, run, Q, SIG, delta, qz, Fin):
		self.active = True
		if run == 1:
			self.Qset = str2set(Q)
			self.Sset = str2set(SIG)
			self.ddic = self.in2df(str2set(delta))
			self.qzr = qz if qz in self.Qset else self.ErrorMessage(3)
			self.Fset = self.Fsetcheck(Fin)
		else:
			self.Qset = set()
			self.Sset = set()
			self.ddic = dict()
			self.qzr = None
			self.Fset = set()
	
	'''
	in2df: input을 dictionary type으로 변환하는 메서드
	newdel은 {qX|sY|sZ(d(qX, sY) = sZ), qU|sV|e(d(qU, sV) = e), qA|e|qB(d(qA, e) = qB),...} 형식으로
	입력된 input을 슬라이싱/스플릿하여 'X|Y|Z' 와 같은 형태의 string을 원소로 가지는 list이다
	이 원소들을 다시 |을 매개로 스플릿하여 3개의 원소를 가지는 list로 만든 후, 몇 개의 검사를 거친다.
	1. tmp[0](X)가 Qset에 없거나, tmp[2](Z)이 e가 아니면서 Qset에 없다면 ErrorMessage(1)
	2. tmp[1](Y)이 Sset에 없거나 e가 아니라면 ErrorMessage(2)
	이 검사를 거친 후 Error 조건을 만족하지 않는다면, (X, Y) tuple을 value로, d(X, Y)들이 원소인 set을 key로 dic에 넣고 return한다.
	'''
	def in2df(self, newdel):
		dic = dict()
		tmp = list()
		for str in newdel:
			tmp = str.split("|")
			if tmp[0] not in self.Qset or (tmp[2] not in self.Qset and tmp[2] != 'e'):
				self.ErrorMessage(1)
				return None
			elif tmp[1] not in self.Sset and tmp[1] != 'e':
				self.ErrorMessage(2)
				return None
			if (tmp[0], tmp[1]) in dic:
				dic[(tmp[0], tmp[1])].add(tmp[2])
			else:
				dic[(tmp[0], tmp[1])] = set([tmp[2]])
		return dic
	
	'''
	Fsetcheck: 입력(Fin)을 검사하여 정상적이라면 set을, 아니라면 ErrorMessage를 return
	입력을 슬라이싱/스플릿 한 후, set type을 형변환하여
	F - Qset가 공집합이라면 (F in Q) list를
	공집합이 아니라면 (F not in Q) ErrorMessage(4)를 return한다
	'''
	def Fsetcheck(self, Fin):
		tmp = str2set(Fin)
		if len(tmp - self.Qset) == 0:
			return tmp
		else:
			self.ErrorMessage(4)
			return None
	
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
			print("상태변화함수 오류: Q에 존재하지 않는 state 입력")
		elif num == 2:
			print("상태변화함수 오류: SIGMA에 존재하지 않는 input symbol 입력")
		elif num == 3:
			print("Initial state 오류: Q에 존재하지 않는 state 입력")
		elif num == 4:
			print("Final state 오류: Q에 존재하지 않는 state 입력")
	
'''
set2str: set을 string으로 변환하는 함수.
Set {'a', 'b', 'c'}를 string "{a, b, c}"와 같이 변환한다.
'''
def set2str(set):
	str = "{"
	lst = list(set)
	lst.sort()
	for s in lst:
		str += (s + ", ")
	return str[:-2] + "}"

'''
str2set: string을 set으로 변환하는 함수.
string "{a, b, c}"를 Set {'a', 'b', 'c'}와 같이 변환한다.
'''
def str2set(str):
	return set(str[1:len(str) - 1].split(", "))

''' emove: eNFA의 state를 key로, state와 e(state)들을 원소로 하는 set을 value로 하는 dictionary를 return하는 함수. '''
def emove(eNFA):
	emove = dict()
	for s in eNFA.Qset:
		tmp = set()
		if (s, 'e') in eNFA.ddic:
			tmp = eNFA.ddic[(s, 'e')]
		tmp.add(s)
		emove[s] = tmp
	return emove

'''
estar(emove): 함수 emove를 통해 생성된 dictionary emove를 이용하여 state를 key로,
e*(state)를 value로 하는 dictionary를 return하는 함수.
'''
def estar(emove):
	eclret = dict()
	for s in emove:
		tmp = set()
		for ss in emove[s]:
			tmp.add(ss)
		eclret[s] = tmp
	for s in emove:
		for ss in emove[s]:
			eclret[s].update(list(emove[ss]))
	if eclret == emove:
		return eclret
	else:
		return estar(eclret)

''' eNFA2DFA: e-NFA를 DFA로 변환하는 함수 '''
def eNFA2DFA(NFA):
	ecl = estar(emove(NFA))						# e-closure dictionary
	DFA = FA(0, None, None, None, None, None)	# DFA 선언(run == 0)
	
	DFA.Sset = NFA.Sset				# Sset 설정
	DFA.qzr = set2str(ecl[NFA.qzr])	# qzr 설정
	DFA.Qset = set([DFA.qzr])		# Qset을 qzr를 첫 원소로 한다
	
	next = set([DFA.qzr])			# next: state(Qset)에 있지 않은 새로운 loop 이후의 state
	while len(next):				# next가 빈 set이 아닐 때 loop
		tmp = set()					# tmp: 새로운 loop 이후의 state일 수 있는 state들의 set (tmp 내의 state는 Qset에 있는 state일 수 있음)
		for state in next:			# for p in Q_eNFA
			sets = str2set(state)
			for sym in DFA.Sset:	# for a in SIGMA
				for s in sets:
					if (s, sym) in NFA.ddic and 'e' not in NFA.ddic[(s, sym)]:
						# (d_DFA(P, a) = e*(d_eNFA(P, a))) subseteq d_DFA
						if not (state, sym) in DFA.ddic:
							DFA.ddic[(state, sym)] = set()
						for x in NFA.ddic[(s, sym)]:
							DFA.ddic[(state, sym)].update(ecl[x])
				
				if (state, sym) in DFA.ddic:
					tmp.add(set2str(DFA.ddic[(state, sym)]))
				else: # Dead state((s, sym) not in d_NFA or 'e' in d_NFA(P, a))
					DFA.Qset.add("{DEAD}")
					DFA.ddic[(state, sym)] = set(["DEAD"])
		
		next = set()
		# 중복되지 않은 state를 Q와 next에 add (e*(d_eNFA(P, a)) in Q_DFA)
		# 즉, 더 이상의 발견되지 않은 state가 없을 때, loop 종료
		for state in tmp:
			if not state in DFA.Qset:
				DFA.Qset.add(state)
				next.add(state)
	
	# DEAD state 처리
	if "{DEAD}" in DFA.Qset:
		for sym in DFA.Sset:
			DFA.ddic[("{DEAD}", sym)] = set(["DEAD"])
	
	# set->string 변환
	for (key, value) in DFA.ddic.items():
		DFA.ddic[key] = set2str(value)
	
	# F_DFA 처리
	for state in DFA.Qset:
		if len(str2set(state) & NFA.Fset):
			DFA.Fset.add(state)
			
	return DFA

''' DFA2mDFA: DFA를 m-DFA로 변환하는 함수 '''
def DFA2mDFA(DFA):
	mDFA = FA(0, None, None, None, None, None)	# mDFA 선언 (run == 0)
	mDFA.Sset = DFA.Sset						# Sset 설정
	
	# Step 1 and Step 2
	table = dict()
	copy_table = dict()
	Qlst = list(DFA.Qset)
	
	# marked: 1, unmarked: 0
	for i in range(len(Qlst) - 1):
		for j in range(i + 1, len(Qlst)):
			# Q_i in F and Q_j not in F or vice versa
			if (Qlst[i] in DFA.Fset and Qlst[j] not in DFA.Fset) or (Qlst[i] not in DFA.Fset and Qlst[j] in DFA.Fset):
				table[(Qlst[i], Qlst[j])] = 1
			else:
				table[(Qlst[i], Qlst[j])] = 0
	
	# Step 3
	copy_table = table.copy()
	flag = True
	while flag:
		for (key, value) in table.items():
			# if there unmarked pair (Q_i, Q_j), 
			if value == 0:
				for sym in DFA.Sset: # for A in SIGMA
					pair = DFA.ddic[(key[0], sym)], DFA.ddic[(key[1], sym)]
					if not pair in table:
						pair = pair[1], pair[0]
					# mark it if the pair {d(Q_i, A), d(Q_j, A)}
					if pair[0] != pair[1] and table[pair] == 1:
						copy_table[key] = 1
						break
		# Repeat this step until we cannot mark anymore states
		if copy_table == table:
			flag = False
		else:
			table = copy_table.copy()
	
	# Step 4
	unmarked = []		# unmarked: table에 남아있는 unmarked set의 list
	umk_state = set()	# umk_state: unmarked state의 set
	mk_state = set()	# mk_state: marked state의 set
	
	for (key, value) in table.items():
		if value == 0:
			unmarked.append(set(key))
			umk_state.update(key)
	mk_state = DFA.Qset - umk_state
	
	# Combine all the unmarked pair (Q_i, Q_j) and make them a single state in the reduced DFA
	x = 0
	copy_unmarked = unmarked[:]		# copy_unmarked: copy of unmarked
	while x < len(copy_unmarked):	# 모든 state가 combine 연산을 할 때까지 loop 
		for y in range(x + 1, len(unmarked)):
			for el in unmarked[x]:	
				if el in unmarked[y]:
					copy_unmarked[x] = copy_unmarked[x] | unmarked[y]	# union
					del copy_unmarked[copy_unmarked.index(unmarked[y])]	# 합쳐진 set은 copy_unmarked에서 삭제
					
		unmarked = copy_unmarked[:]	# unmarked 갱신
		x += 1
	
	umk_s_new = set()	# umk_s_new: 새로운 이름(qN)을 가진 unmarked state set 
	mk_s_new = set()	# mk_s_new: 새로운 이름(qN)을 가진 marked state set
	s2ns = dict()		# s2ns: state -> new state dictionary(key: string, value: string)
	ns2s = dict()		# ns2s: new state -> state dictionary(key: string, 
	
	x = 0
	for el in unmarked:
		name = 'q' + str(x)
		umk_s_new.add(name)
		for ell in el:
			s2ns[ell] = name
		ns2s[name] = el
		x += 1
	
	for el in mk_state:
		name = 'q' + str(x)
		mk_s_new.add(name)
		s2ns[el] = name
		ns2s['q' + str(x)] = set()
		ns2s['q' + str(x)].add(el)
		x += 1
	
	# mDFA_q0의 state name가 q0가 아니라면, q0로 바꿔주는 과정
	tmpqzr = s2ns[DFA.qzr]
	if s2ns[DFA.qzr] != "q0":
		tmp = ns2s["q0"]
		ns2s["q0"] = ns2s[tmpqzr]
		ns2s[tmpqzr] = tmp
		for (key, value) in s2ns.items():
			if value == "q0":
				s2ns[key] = tmpqzr
			elif value == tmpqzr:
				s2ns[key] = "q0"
	mDFA.qzr = "q0"
	
	mDFA.Qset = umk_s_new | mk_s_new	# Qset(Q_mDFA) 설정. union of umk_s_new and mk_s_new
	# ddic(d_mDFA) 설정
	for state in mDFA.Qset:
		for sym in mDFA.Sset:
			mDFA.ddic[(state, sym)] = s2ns[DFA.ddic[(list(ns2s[state])[0], sym)]]
	# Fset(F_mDFA) 설정
	for s in DFA.Fset:
		mDFA.Fset.add(s2ns[s])
		
	return mDFA

''' printing: parameter로 받은 FA를 state(Q), input symbol(SIGMA), state transition function(delta), initial state(q0), final state(F) 순서대로 출력하는 함수. '''
def printing(FA):
	tmp = None
	print("State(Q):", end = " ")
	print(FA.Qset)
	print("Input Symbol(SIGMA):", end = " ")
	print(FA.Sset)
	print("State Transition Function(delta)")
	sorted_ddic = dict(sorted(FA.ddic.items(), key = operator.itemgetter(0))) # key sorting
	for (key, value) in sorted_ddic.items():
		if tmp != key[0] and tmp != None:
			print()
		elif tmp == key[0]:
			print("|", end = " ")
		print('d', end = "")
		print(key, end = "")
		print(" = ", end = "")
		print(value, end = " ")
		tmp = key[0]
	print("\nInitial State(q0):", end = " ")
	print(FA.qzr)
	print("Final State(F):", end = " ")
	print(FA.Fset)
	
print("e-NFA to m-DFA 변환기입니다. 입력 예시, 방식은 다음과 같습니다.")
print("Q: {q0, q1, q2, ...}")
print("SIGMA: {s0, s1, s2, ...}")
print("delta: {qX|sY|sZ(d(qX, sY) = sZ), qU|sV|e(d(qU, sV) = e), qA|e|qB(d(qA, e) = qB),...}")
print("q0: qN")
print("F: {qA, qB, ...}\n")

Q = input("Q: ")
SIG = input("SIGMA: ")
delta = input("delta: ")
qz = input("q0: ")
Fin = input("F: ")

eNFA = FA(1, Q, SIG, delta, qz, Fin)

if eNFA.active:
	DFA = eNFA2DFA(eNFA)
	mDFA = DFA2mDFA(DFA)

	print("\nm-DFA 결과")
	printing(mDFA)

x = input("\nPlease press enter to exit: ")
	