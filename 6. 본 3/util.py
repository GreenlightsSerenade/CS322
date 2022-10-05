first = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] # 초성
second = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"] # 중성
third = [" ", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄿ", "ㄾ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"] # 종성
vowel = ['ㅣ', '.', 'ㅡ'] # 천지인 키보드 모음
cons = ['ㄱ', 'ㄴ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅇ'] # 천지인 키보드 자음
ARAEA = [".", ".."] # 아래아, 쌍아래아. unicode: 4510, 4514
CC = {(1, 19): 3, (17, 19): 18, (4, 22): 5, (4, 27): 6, (8, 1): 9, (8, 16): 10, (8, 17): 11, (8, 19): 12, (8, 25): 13, (8, 26): 14, (8, 27): 15}
# ㄳ ㅄ ㄵ ㄶ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ

# Mealy Machine
class MealyM:
	'''
	Qset(Q-set): 상태들의 유한 집합 (set)
	Sset(Sigma-set): 입력문자들의 유한 집합 (set)
	Pset(Pi-set): 출력문자들의 유한 집합 (set)
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

'''
make: buffer로 string을 만드는 함수
Lettermake를 이용하여 buffer를 string으로 변환하여 반환한다.
글자를 계산하는 기준은 모음의 index이다.
'''
def make(buffer, flag = 1):
	f_index = [] # 글자의 시작인 초성의 index들을 저장
	ret = ""
	
	l = len(buffer) # length of buffer
	if l == 0: # buffer에 아무것도 없을 때 빈 string return
		return ''
	elif l == 1: # l == 1이면 그대로 return
		return Lettermake([buffer[0]])
	# buffer list를 읽으면서 buffer[i]가 모음(혹은 아래아)이라면 그 앞 index를 저장 => 모음 바로 앞의 자음은 항상 초성!
	for i in range(l):
		if (buffer[i] in second or buffer[i] in ARAEA) and buffer[i - 1] in first:
			f_index.append(i - 1)
	f_index.append(l) # slicing의 편리를 위해 l append
	
	lf = len(f_index) # length of f_index = 글자를 만들 수 있는 초성의 갯수 + 1
	if lf == 1: # 초성의 갯수가 0개 = buffer가 모두 미완성 글자들로 이루어진 상태
		for i in range(l):
			ret += Lettermake([buffer[i]])
		return ret
	
	if f_index[0] != 0: # 첫 초성이 buffer의 처음이 아님 = buffer에서 첫 초성 이전의 element가 모두 미완성 글자들로 이루어진 상태
		for i in range(f_index[0]):
			ret += Lettermake([buffer[i]])
	
	# idx: buffer[f_index[i]:f_index[i] + idx]가 하나의 글자로 완성될 때, 이를 만족하는 최대값
	# f_index[i] ~ f_index[i] + idx 까지의 buffer가 하나의 글자가 됨
	for i in range(lf - 1):
		idx = makecheck(buffer[f_index[i]:f_index[i + 1]], True)
		if f_index[i] + idx == f_index[i + 1]:
			if i == lf - 2: # 초성우선이라면 마지막 출력 처리에서만 초성우선출력하면 된다
				ret += Lettermake(buffer[f_index[i]:f_index[i + 1]], flag)
			else:
				ret += Lettermake(buffer[f_index[i]:f_index[i + 1]])
		else:
			ret += Lettermake(buffer[f_index[i]:f_index[i] + idx])
			for j in range(f_index[i] + idx, f_index[i + 1]):
				ret += Lettermake([buffer[j]])
	return ret

'''
makecheck: buf[:idx]가 한 '글자'로 완성될 때, 최대 idx 값을 찾는 함수
flag가 True일 땐 첫 실행 파트 작업을, False일 땐 반복 실행 파트 작업을 한다.
'''
def makecheck(buf, flag):
	if flag:
		for i in range(2, len(buf) + 1):
			sw = makecheck(buf[:i], False)
			if not sw:
				return i - 1
		return len(buf)
	else:
		if len(buf) == 2:	# 자음 + [모음]
			return buf[1] in second or buf[1] in ARAEA
		elif len(buf) == 3:	# 초성 + 중성 + [종성]
			return buf[2] in third
		elif len(buf) == 4:	# 초성 + 중성 + [자음 + 자음 = 겹받침]
			return buf[3] in third and (third.index(buf[2]), third.index(buf[3])) in CC
		else: # 그 이상은 무조건 False
			return False
	
'''
Lettermake: buffer로 한 글자, 혹은 한 글자 + 자음 (type: string)을 만드는 함수
buffer의 length, flag(초성우선/받침우선), buffer[n]이 초/중/종성 중 무엇인가 등을 기준으로 생성한다.
'''
def Lettermake(buffer, flag = 1):
	if len(buffer) == 1: # 글자 하나\
		return buffer[0] if not buffer[0] in ARAEA else chr(4510 + ARAEA.index(buffer[0]) * 4)
	elif len(buffer) == 2 and buffer[1] in ARAEA: # 초성 + 아래아(., ..)\
		return buffer[0] + chr(4510 + ARAEA.index(buffer[1]) * 4)
	elif len(buffer) == 2: # 초성 + 아래아가 아닌 중성
		return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28)
	elif len(buffer) == 3: # 초성 + 중성 + 결정되지 않은 자음
		if buffer[2] in third and flag == 1: # 결정되지 않은 자음이 종성으로 가능한 자음이면서 받침우선방식일 때 한 글자로 합쳐서 출력
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + third.index(buffer[2]))
		else: # 결정되지 않은 자음이 종성이 불가능하거나, 초성우선방식일 때 결정되지 않은 자음을 따로 출력
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28) + buffer[2]
	elif len(buffer) == 4: # 초성 + 중성 + 결정된 자음 + 결정되지 않은 자음
		# 1. 결정되지 않은 자음이 종성으로 불가능할 때
		# 2. 결정된 + 결정되지 않은 자음이 겹받침으로 만들어지지 않을 때
		# 3. 초성우선방식일 때
		# 결정되지 않은 자음을 따로 출력
		if (not buffer[3] in third) or (not (third.index(buffer[2]), third.index(buffer[3])) in CC) or flag == 0:
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + third.index(buffer[2])) + buffer[3]
		else: # 나머지 case (결정된 + 결정되지 않은 자음이 겹받침으로 만들어 질 때) 한 글자로 합쳐서 출력
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + CC[third.index(buffer[2]), third.index(buffer[3])])
	elif len(buffer) == 5: # 초성 + 중성 + 겹받침(자음 + 자음) + 자음 case
		return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + CC[third.index(buffer[2]), third.index(buffer[3])]) + buffer[4]
	else:
		return ''

'''
c_cycle: 자음순환함수
천지인 자판에서는 7개의 기본 자음 자판을 여러번 입력하는 작업을 통해 비슷한 계열의 자음을 생성하는데, 이를 실행하는 함수이다.
base-add가 같은 계열에 존재하지 않는다면, None을 반환한다.
'''
def c_cycle(base, add):
	cycle_dic = {'ㄱ': ['ㄱ', 'ㅋ', 'ㄲ'], 'ㄴ': ['ㄴ', 'ㄹ'], 'ㄷ': ['ㄷ', 'ㅌ', 'ㄸ'], 'ㅂ': ['ㅂ', 'ㅍ', 'ㅃ'], 'ㅅ': ['ㅅ', 'ㅎ', 'ㅆ'], 'ㅈ': ['ㅈ', 'ㅊ', 'ㅉ'], 'ㅇ': ['ㅇ', 'ㅁ']}
	
	now = cycle_dic[add]
	if base in now:
		idx = now.index(base)
		size = len(now)
		return cycle_dic[add][(idx + 1) % size]
	return None

'''
v_change: 모음합성함수
천지인 자판에서는 3개의 기본 모음 자판을 통해 모음을 생성하는데, 이를 실행하는 함수이다.
base-add로 모음이 생성되지 않는 case라면, None을 반환한다.
'''
def v_change(base, add):
	tmp1 = ['ㅏ', 'ㅑ', 'ㅜ', 'ㅠ']
	tmp2 = {'ㅏ': 'ㅐ', 'ㅑ': 'ㅒ', 'ㅓ': 'ㅔ', 'ㅕ': 'ㅖ', 'ㅗ': 'ㅚ', 'ㅜ': 'ㅟ', 'ㅠ': 'ㅝ'}
	if base == '.':		# . + (ㅣ, ㅡ, .) = (ㅓ, ㅗ, ..)
		if add == 'ㅣ':
			return 'ㅓ'
		elif add == 'ㅡ':
			return 'ㅗ'
		elif add == '.':
			return '..'
	elif base == '..':	# .. + (ㅣ, ㅡ) = (ㅕ, ㅛ)
		if add == 'ㅣ':
			return 'ㅕ'
		elif add == 'ㅡ':
			return 'ㅛ'
	elif base == 'ㅡ':	# ㅡ + (., ㅣ) = (ㅜ, ㅢ)
		if add == '.':
			return 'ㅜ'
		elif add == 'ㅣ':
			return 'ㅢ'
	elif base == 'ㅣ' and add == '.':	# ㅣ + . = ㅏ
		return 'ㅏ'
	if base in tmp1 and add == '.':		# (ㅏ, ㅑ, ㅜ, ㅠ) + . = (ㅑ, ㅏ, ㅠ, ㅜ)
		idx = tmp1.index(base)
		return tmp1[(idx - idx % 2) * 2 + 1 - idx]
	if base in tmp2 and add == 'ㅣ':		# (ㅏ, ㅑ, ㅓ, ㅕ, ㅗ, ㅜ, ㅠ) + ㅣ = (ㅐ, ㅒ, ㅔ, ㅖ, ㅚ, ㅟ, ㅝ)
		return tmp2[base]
	# ㅚ + . = ㅘ / ㅘ + ㅣ = ㅙ / ㅝ + ㅣ = ㅞ 
	elif base == 'ㅚ' and add == '.':
		return 'ㅘ'
	elif base == 'ㅘ' and add == 'ㅣ':
		return 'ㅙ'
	elif base == 'ㅝ' and add == 'ㅣ':
		return 'ㅞ'
	return None

'''
erase: buffer에서 글자 element 삭제
자음인 경우에는 겹자음은 따로 buffer에 저장했으므로 그냥 pop하면 되며, 모음의 경우에는 각자 다르다(dictionary v 참조)
'''
def erase(buffer):
	v = {"ㅏ": 'ㅣ', "ㅐ" : 'ㅏ', "ㅑ": 'ㅏ', "ㅒ": 'ㅑ', "ㅓ": '.', "ㅔ": 'ㅓ', "ㅕ": '..', "ㅖ": 'ㅕ'
			, "ㅗ": '.', "ㅘ": 'ㅚ', "ㅙ": 'ㅘ', "ㅚ": 'ㅗ', "ㅛ": '..', "ㅜ": 'ㅡ', "ㅝ": 'ㅠ', "ㅞ": 'ㅝ', "ㅟ": 'ㅜ', "ㅠ": 'ㅜ', "ㅢ": 'ㅡ', "..": '.'}
	elem = buffer.pop()
	if elem in v:
		buffer.append(v[elem])
	return buffer
			
	