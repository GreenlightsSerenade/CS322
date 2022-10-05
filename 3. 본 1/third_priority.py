first = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
second = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
third = [" ", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄿ", "ㄾ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
CC = {(1, 19): 3, (17, 19): 18, (4, 22): 5, (4, 27): 6, (8, 1): 9, (8, 16): 10, (8, 17): 11, (8, 19): 12, (8, 25): 13, (8, 26): 14, (8, 27): 15}
# ㄳ ㅄ ㄵ ㄶ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ
CV = {(8, 0): 9, (8, 1): 10, (8, 20): 11, (13, 4): 14, (13, 5): 15, (13, 20): 16, (18, 20): 19}
# ㅘ ㅙ ㅚ ㅝ ㅞ ㅟ ㅢ

class Letter:
	def __init__(self):
		self.last_buffer = []
	
	# Consonant
	def Consonant(self, prints, cons):
		if len(self.last_buffer) > 1:
			prints += self.make()
			self.last_buffer = []
		self.last_buffer.append(first.index(cons))
		return prints
	
	# Consonant + Vowel
	def Consowel(self, prints, vowel):
		self.last_buffer.append(second.index(vowel))
		return prints

	# Consonant + Vowel + Consonant
	def Covonant(self, prints, cons):
		self.last_buffer.append(third.index(cons))
		return prints

	# Consonant + Vowel + Vowel
	def Convovowel(self, prints, vowel):
		ch_vowel = self.last_buffer.pop()
		vowel_index = second.index(vowel)
		self.last_buffer.append(CV[(ch_vowel, vowel_index)])
		return prints
		
	# Consonant + Vowel(+ Vowel) + Consonant + Consonant
	def Covoconant(self, prints, cons):
		ch_final = self.last_buffer.pop()
		final_index = third.index(cons)
		self.last_buffer.append(CC[(ch_final, final_index)])
		return prints

	# Consonant + Vowel(+ Vowel) + Consonant(+ Consonant) + Vowel
	def Consowel2(self, prints, vowel):
		ch_cons = self.last_buffer.pop()
		media_index = second.index(vowel)
		
		if third[ch_cons] in first:
			prints += self.make()
			self.last_buffer = []
			self.last_buffer.append(first.index(third[ch_cons]))
			self.last_buffer.append(media_index)
			return prints
		else:
			comp_c = self.value2key(ch_cons, CC)
			self.last_buffer.append(comp_c[0])
			prints += self.make()
			self.last_buffer = []
			self.last_buffer.append(first.index(third[comp_c[1]]))
			self.last_buffer.append(media_index)
			return prints
	
	def erase(self, x):
		if x == 0:
			element = self.last_buffer.pop()
			comp = None
			if len(self.last_buffer) == 2:
				comp = self.value2key(element, CC)
			elif len(self.last_buffer) == 1:
				comp = self.value2key(element, CV)
			if not comp is None:
				self.last_buffer.append(comp[0])
		else:
			self.last_buffer = []
		
	def make(self):
		if len(self.last_buffer) == 1:
			return first[self.last_buffer[0]]
		elif len(self.last_buffer) == 2:
			return chr(44032 + (self.last_buffer[0] * 21 + self.last_buffer[1]) * 28)
		elif len(self.last_buffer) == 3:
			return chr(44032 + (self.last_buffer[0] * 21 + self.last_buffer[1]) * 28 + self.last_buffer[2])
		else:
			return ''
	
	def value2key(self, element, what):		
		for key, value in getattr(what, "items")():
			if value == element:
				return key
		return None
	
	'''
	def CompoundCheck(self, ch):
		if ch in second:
			x = second.index(self.last_buffer[-1]), second.index(ch)
			if x in CV:
				self.last_buffer[-1] = second(CV[x])
			else:
				self.last_buffer.append(ch)
		else:
			self.last_buffer.append(ch)
	'''
			