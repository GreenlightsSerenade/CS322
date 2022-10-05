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
		self.last_buffer.append(cons)
		return prints
	
	# Consonant + Vowel
	def Consowel(self, prints, vowel):
		if len(self.last_buffer) > 1:
			prints += self.Lettermake(-1)
			self.last_buffer = self.last_buffer[-1:]
		self.last_buffer.append(vowel)
		return prints
	
	# Consonant + Vowel + Vowel
	def Convovowel(self, prints, vowel):
		ch_vowel_index = second.index(self.last_buffer.pop())
		vowel_index = second.index(vowel)
		self.last_buffer.append(second[CV[ch_vowel_index, vowel_index]])
		return prints
		
	# Letter + Consonant
	def Lettant(self, prints, cons):
		prints += self.Lettermake()
		self.last_buffer = [cons]
		return prints
		
	# Consonant + Vowel(+ Vowel) + Consonant + Consonant
	def Covoconant(self, prints, cons):
		self.last_buffer.append(cons)
		return prints
	
	def erase(self, x):
		if x == 0:
			element = self.last_buffer.pop()
			comp = None
			if len(self.last_buffer) == 1:
				comp = self.value2key(second.index(element), CV)
			if not comp is None:
				self.last_buffer.append(second[comp[0]])
		else:
			self.last_buffer = []
		
	def make(self):
		if len(self.last_buffer) == 1:
			return self.last_buffer[0]
		elif len(self.last_buffer) == 2:
			return chr(44032 + (first.index(self.last_buffer[0]) * 21 + second.index(self.last_buffer[1])) * 28)
		elif len(self.last_buffer) == 3:
			return chr(44032 + (first.index(self.last_buffer[0]) * 21 + second.index(self.last_buffer[1])) * 28) + self.last_buffer[2]
		elif len(self.last_buffer) == 4:
			return chr(44032 + (first.index(self.last_buffer[0]) * 21 + second.index(self.last_buffer[1])) * 28 + third.index(self.last_buffer[2])) + self.last_buffer[3]
		else:
			return ''
	
	def Lettermake(self, x = None):
		buffer = self.last_buffer if x is None else self.last_buffer[:x]
		if len(buffer) == 2:
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28)
		elif len(buffer) == 3:
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + third.index(buffer[2]))
		elif len(buffer) == 4:
			return chr(44032 + (first.index(buffer[0]) * 21 + second.index(buffer[1])) * 28 + CC[third.index(buffer[2]), third.index(buffer[3])])
		else:
			return ''
		
	def value2key(self, element, what):		
		for key, value in getattr(what, "items")():
			if value == element:
				return key
		return None
			
			