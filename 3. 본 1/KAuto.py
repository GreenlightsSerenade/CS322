import first_priority
import third_priority

SIGMA = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ", "ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ", "ㅐ", "ㅔ", "ㅒ", "ㅖ", " ", "B", "b"]

def init_dfunc(txt):
	delta_func = dict()
	f = open(txt, 'r')
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		line_split = line.split(' ')
		line_ssplit = line_split[1].split('+')
		for symbol in line_ssplit:
			delta_func[(line_split[0], symbol)] = line_split[2]
	f.close()
	return delta_func

def init_lfunc(txt):
	lambda_func = dict()
	f = open(txt, 'r')
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		line_split = line.split(' ')
		line_ssplit = line_split[1].split('+')
		for symbol in line_ssplit:
			lambda_func[(line_split[0], symbol)] = line_split[2]
	f.close()
	return lambda_func

def KAutoMealyM(SIGMA, delta_func, lambda_func, qz, L, flag):
	c = input("입력 바랍니다(백스페이스: B or b): ") # string
	state = qz
	states = [] # state list
	output = ""
	
	for ch in c:
		# 입력된 문자가 SIGMA에 존재하지 않는 case
		if not ch in SIGMA:
			print("Error: The letter " + ch + " does not exist in Input Symbol Set.")
			continue
		# 입력된 문자가 space(' ')
		elif ch == ' ':
			# 공백을 만들었으므로 현재까지의 buffer는 완성된 글자가 된다.
			# 초성 우선일 시 Lettermake, 받침 우선일 시 make를 이용한다.
			if flag == 0:
				output += (L.Lettermake() + ' ')
			else:
				output += (L.make() + ' ')
			L.erase(1) # buffer 초기화
			state = 'S' # state 초기화
			states.append(state)
		# 입력된 문자가 B 또는 b(backspace)
		elif ch == 'B' or ch == 'b':
			# 아무것도 입력되지 않은 상황에서의 backspace: 변화 없음
			if len(output) == 0 and len(L.last_buffer) == 0:
				state = 'S'
				states.append(state)
				print("")
				continue
			# buffer에 아무것도 존재하지 않는다면(모두 완성된 글자라면) 글자 전체를 지운다
			elif len(L.last_buffer) == 0:
				output = output[:-1]
			# buffer에 글자 element가 존재한다면 글자 element 하나씩 삭제한다.
			else:
				L.erase(0)

			# last_buffer의 길이 상황에 따라 state가 달라진다.
			if len(L.last_buffer) == 0:
				state = 'S'
			elif len(L.last_buffer) == 1:
				state = 'V'
			else: # 현재의 state를 제거하고, 그 전의 state를 사용한다.
				states = states[:-1]
				state = states[-1]
				
		# Automata에 알맞은 입력
		elif (state, ch) in delta_func:
			x = state, lambda_func[(state, ch)]
			output = getattr(L, lambda_func[(state, ch)])(output, ch)
			state = delta_func[(state, ch)]
			states.append(state)
		
		# Automata에 알맞지 않은 입력
		else:
			print("Error: Wrong grammer")
			return 0
			# L.CompoundCheck(ch)
		
		print(output + L.make())
	
	# 초성 우선 방식일 시, 마지막 글자 완성 보정 (ex) 완전한인가ㄴ -> 완전한인간)
	if len(L.last_buffer) > 2 and flag == 0:
		print(output + L.Lettermake())

df1 = init_dfunc("fp_delta.txt")
df2 = init_dfunc("tp_delta.txt")
lf1 = init_lfunc("fp_lambda.txt")
lf2 = init_lfunc("tp_lambda.txt")
flag = True

print("본 프로젝트 1. 한글모아쓰기 Mealy/Moore Machine")
print("한글을 자모음을 쪼개 입력하면 과정이 출력됩니다")
while flag:
	x = int(input("초성 우선 방식을 원하시면 0을, 받침 우선 방식을 원하시면 1을, 종료를 원하시면 -1을 입력해주세요: "))
	if x == -1:
		flag = False
	elif x == 0:
		L = first_priority.Letter()
		KAutoMealyM(SIGMA, df1, lf1, 'S', L, x)
	elif x == 1:
		L = third_priority.Letter()
		KAutoMealyM(SIGMA, df2, lf2, 'S', L, x)
	else:
		print("잘못된 입력입니다")
		flag = False