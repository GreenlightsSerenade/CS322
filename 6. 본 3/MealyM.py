''' Mealy Machine 시뮬레이터 '''
class MealyM:
	'''
	Qset(Q-list): 상태들의 유한 집합 (set)
	Sset(Sigma-list): 입력문자들의 유한 집합 (set)
	Pset(Pi-list): 출력문자들의 유한 집합 (set)
	ddic(delta-dictionary): 상태변화함수. (qX, sX) tuple을 key로, qY를 value로 하는 dictionary (dict)
	ldic(lambda-dictionary): 출력함수. (qX, sX) tuple을 key로, pX를 value로 하는 dictionary (dict)
	qzr(q-zero): 초기 상태 (str)
	'''
	def __init__(self, Q, SIG, PI, delta, lam, qz):
		self.Qset = Q
		self.Sset = SIG
		self.Pset = PI
		self.ddic = delta
		self.ldic = lam
		self.qzr = qz