import RE2mDFA
from util import *

'''
mDFA2MealyM: mDFA를 '이 프로그램에 알맞은' Mealy Machine으로 변환하는 함수
Qset, ddic, qzr은 동일하며 Sset은 mDFA의 Sset(0~9)에 *, #, ' '을 추가, ldic은 10개의 천지인 자판이며
ldic은 ddic(state, char)에 대응되는 천지인 자판(PI_list)이다.
'''
def mDFA2MealyM(mDFA):
	SIG = mDFA.Sset
	PI_list = ['ㅣ', '.', 'ㅡ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅇ']
	lam = dict()
	for key in mDFA.ddic.keys():
		lam[key] = PI_list[(int(key[1]) - 1) % 10]
	
	return MealyM(mDFA.Qset, mDFA.Sset | {'*', '#', ' '}, set(PI_list), mDFA.ddic, lam, mDFA.qzr)

'''
Kor3X4Auto: 입력된 input과 Mealy Machine을 바탕으로 알맞은 한글 string을 변환하여 반환하는 함수
flag: 0일 때 초성우선, 1일 때 받침우선방식이다.
'''
def Kor3X4Auto(input, MM, flag):
	state = MM.qzr	# state
	states = []		# buffer에 대응되는 list로, buffer[n]이 입력되기 전의 state들을 저장하는 list list.
	buffer = []		# buffer: make되지 않은 buffer list
	output = ""		# output: make된 buffer들의 string

	for ch in input:
		# 입력된 문자가 SIGMA에 존재하지 않는 case
		if not ch in MM.Sset:
			print("Error: The letter " + ch + " does not exist in Input Symbol Set.")
			continue

		# 입력된 문자가 # (backspace)
		elif ch == '#':
			# buffer에 아무것도 존재하지 않을 때
			if len(buffer) == 0:
				# output (완성된 글자)가 존재하면 지운다
				if len(output) != 0:
					output = output[:-1]
				print(output)
				continue
			# buffer에 글자 element가 존재하면 하나씩 삭제한다.
			# state는 states list를 이용한다.
			else:
				victim = buffer[-1]
				victim_s = states[-1]
				if victim in second and len(victim_s) > 1:
					state = victim_s.pop()
				else:
					state = (states.pop())[0]
				buffer = erase(buffer)
		
		# 입력된 문자가 * (->, 글자넘김)
		# buffer를 string으로 변환하여 output에 저장하고, buffer와 state를 초기 상태로
		elif ch == '*':
			output += make(buffer)
			buffer = []
			state = 'q0'
		
		# 입력된 문자가 ' ' (공백)
		# buffer + ' '을 string으로 변환하여 output에 저장하고, buffer와 state를 초기 상태로
		elif ch == ' ':
			output += (make(buffer) + ' ')
			buffer = []
			state = 'q0'
		
		# Automata에 알맞은 입력(d(s, c)가 존재)
		elif (state, ch) in MM.ddic:
			old_s = state
			state = MM.ddic[(state, ch)]
			op = MM.ldic[(state, ch)]
			
			if state == "DEAD": # dead state 처리
				buffer.append(op)
				state = MM.ddic[('q0', ch)]
				states.append([state])
			elif len(buffer) == 0: # buffer에 아무것도 없을 때
				buffer.append(op)
				states.append([old_s])
			else:
				buf = buffer[-1]
				if op in vowel: # 입력 문자가 모음
					if buf in second or buf in ARAEA: # 합성모음일 때
						buf_second = buffer.pop()
						buffer.append(v_change(buf_second, op))
						states[-1].append(old_s)
					else: # 합성모음이 아닐 때
						buffer.append(op)
						states.append([old_s])
				else: # 입력 문자가 자음
					new_c = c_cycle(buffer[-1], op)
					if new_c is None:
						buffer.append(op)
						states.append([old_s])
					else:
						buffer.pop()
						buffer.append(new_c)
		
		# Automata에 알맞지 않은 입력
		else:
			print("Error: Wrong grammer")
			return;
		
		#print(buffer)
		print(output + make(buffer, flag))
		
	# 초성 우선 방식일 시, 마지막 글자 완성 보정 (ex) 완전한인가ㄴ -> 완전한인간)	
	if flag == 0 and not (buffer[-1] in second or buffer[-1] in ARAEA):
		print(output + make(buffer))

# main: 실행 함수.		
def main():
	TXT = "RE.txt"
	f = open(TXT, 'r')
	re = f.readline()
	f.close()
	mDFA = RE2mDFA.RE2mDFA(re)
	MM = mDFA2MealyM(mDFA)
	flag = True
	print("본 프로젝트 3. 3X4 한글자판을 위한 한글모아쓰기 오토마타")
	print("키보드는 천지인 키보드(iOS 10키 키보드)를 기준으로 하며, 123456789*0#으로 대응됩니다.")
	print("*은 글자넘김, #은 Backspace입니다.")
	while flag:
		x = input("초성 우선 방식을 원하시면 0을, 받침 우선 방식을 원하시면 1을, 종료를 원하시면 -1을 입력해주세요: ")
		if x == "-1":
			flag = False
		elif x == '0' or x == '1':
			string = input("입력 바랍니다: ")
			Kor3X4Auto(string, MM, int(x))
		else:
			print("잘못된 입력입니다")
			flag = False

main()