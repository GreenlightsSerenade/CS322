import RE2mDFA
import MealyM
from util import *

'''
mDFA2MealyM: mDFA를 '이 프로그램에 알맞은' Mealy Machine으로 변환하는 함수
Qset, Sset, lset, ddic, ldic, qzr을 입력한다
Qset, ddic, qzr은 동일하며 Sset은 mDFA의 Sset(0~9)에 *, #, ' '을 추가, ldic은 10개의 천지인 자판이며
ldic은 ddic(state, char)에 대응되는 천지인 자판(PI_list)이다.
'''
def mDFA2MealyM(mDFA):
	SIG = mDFA.Sset
	PI_list = ['ㅣ', '.', 'ㅡ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅇ']
	lam = dict()
	for key in mDFA.ddic.keys():
		lam[key] = PI_list[(int(key[1]) - 1) % 10]
	
	return MealyM.MealyM(mDFA.Qset, mDFA.Sset | {'*', '#', ' '}, set(PI_list), mDFA.ddic, lam, mDFA.qzr)

'''
Kor3X4Auto:

'''
def Kor3X4Auto(input, MM, flag):
	state = MM.qzr
	states = []
	buffer = []
	output = ""

	for ch in input:
		if not ch in MM.Sset:
			print("Error: The letter " + ch + " does not exist in Input Symbol Set.")
			continue
			
		elif ch == '#': # backspace
			if len(buffer) == 0:
				if len(output) != 0:
					output = output[:-1]
				print(output)
				continue
			else:
				victim = buffer[-1]
				victim_s = states[-1]
				if victim in second and len(victim_s) > 1:
					state = victim_s.pop()
				else:
					state = (states.pop())[0]
				buffer = erase(buffer)
				
		elif ch == '*': # -> (문장종료)
			output += make(buffer, 1)
			buffer = []
			state = 'q0'
		
		elif ch == ' ': # space
			output += (make(buffer, 1) + ' ')
			buffer = []
			state = 'q0'
		
		elif MM.ddic[(state, ch)] == "DEAD":
			output += (make(buffer, flag))
			
			buffer = [MM.ldic[('q0', ch)]]
			state = MM.ddic[('q0', ch)]
			states.append([state])
			
		elif (state, ch) in MM.ddic:
			old_s = state
			state = MM.ddic[(state, ch)]
			op = MM.ldic[(state, ch)]
			
			if len(buffer) == 0:
				buffer.append(op)
				states.append([old_s])
			else:
				buf = buffer[-1]
				if op in vowel:
					if buf in second or buf in ARAEA:
						buf_second = buffer.pop()
						buffer.append(v_change(buf_second, op))
						states[-1].append(old_s)
					else:
						buffer.append(op)
						states.append([old_s])
				else:
					new_c = c_cycle(buffer[-1], op)
					if new_c is None:
						buffer.append(op)
						states.append([old_s])
					else:
						buffer.pop()
						buffer.append(new_c)

		else:
			print("Error: Wrong grammer")
			return;
		
		#print("output: {0}".format(output))
		#print("bufferlist: {0}".format(buffer))
		#print("states: {0}".format(states))
		#print("buffer: {0}".format(Lettermake(buffer)))
		print(output + make(buffer, flag))
	if flag == 0 and not (buffer[-1] in second or buffer[-1] in ARAEA):
		print(output + make(buffer, 1))
						
def main():
	TXT = "RE.txt"
	f = open(TXT, 'r')
	re = f.readline()
	f.close()
	mDFA = RE2mDFA.RE2mDFA(re)
	MM = mDFA2MealyM(mDFA)
	flag = True
	print("본 프로젝트 3. 3X4 한글자판을 위한 한글모아쓰기 오토마타")
	print("키보드는 천지인 키보드를 기준으로 하며, 123456789*0#으로 대응됩니다.")
	print("iOS의 천지인을 기준으로 만들어졌기에 *은 글자띄어쓰기(글자종료)입니다.")
	print("Backspace는 '#'입니다.")
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