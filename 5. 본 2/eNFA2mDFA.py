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
	
	run이 1일 때 입력된 Q, SIG, delta, qz, Fin을 그대로 넣어준다.
	1이 아닐 때는 모두 초기 상태로 설정한다. 이는 처음 선언에 데이터를 입력하지 않고, 나중에 직접적인 접근을 하기 위해서이다.
	'''
	def __init__(self, run, Q, SIG, delta, qz, Fin):
		if run == 1:
			self.Qset = Q
			self.Sset = SIG
			self.ddic = delta
			self.qzr = qz
			self.Fset = Fin
		else:
			self.Qset = set()
			self.Sset = set()
			self.ddic = dict()
			self.qzr = None
			self.Fset = set()
	
	''' printing: state(Q), input symbol(SIGMA), state transition function(delta), initial state(q0), final state(F) 순서대로 출력하는 함수. '''
	def printing(self):
		tmp = None
		print("State(Q): {0}".format(self.Qset))
		print("Input Symbol(SIGMA): {0}".format(self.Sset))
		print("State Transition Function(delta)")
		sorted_ddic = dict(sorted(self.ddic.items(), key = operator.itemgetter(0))) # key sorting
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
		print("\nInitial State(q0): {0}".format(self.qzr))
		print("Final State(F): {0}".format(self.Fset))
	
	
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

''' eNFA2mDFA: DFA2mDFA(eNFA2DFA(eNFA)) '''
def eNFA2mDFA(eNFA):
	return DFA2mDFA(eNFA2DFA(eNFA))