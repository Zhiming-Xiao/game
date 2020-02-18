import pyCardDeck
from typing import List
from pyCardDeck.cards import PokerCard

class Player:

	def __init__(self,name):
		self.hand = []
		self.name = name

	def __str__(self):
		return self.name
	
	def show_hand(self):
		i = 0
		for card in self.hand:
			print(f"{i}: {card}")
			i += 1
			
	def replace_card(self,index,table):
		old_card = self.hand[index]
		new_card = table.deck.draw()
		self.hand[index] = new_card
		table.deck.discard(old_card)
	
	def count(self):
		r = []
		s = []
		for item in self.hand:
			s.append(item.suit)
			r.append(item.rank)

		mark = 0
		bigcard = max(r)

		# analysis suit
		set_s = set(s)
		if len(set_s) == 1:
			mark += 9	#Flush

		# analysis rank
		min_r = min(r)
		new_list = list(range(min_r,min_r+5))
		new_list.sort()
		new_rank = r[:]
		new_rank.sort()

		if new_list == new_rank:
			mark += 8	#Straight

		dict_r = dict()
		for k in r:
			dict_r[k] = dict_r.get(k,0) + 1

		_trm = []
		for k, v in dict_r.items():
			if v == 4:
				mark += 11	#four
				bigcard = k
			elif v == 3:
				mark += 7	#three
				bigcard = k
			elif v == 2:
				mark += 3	#two
				_trm.append(k)
				bigcard = max(_trm)

		return [mark,bigcard]

class PokerTable:

	def __init__(self, players: List[Player]):
		self.deck = pyCardDeck.Deck(
			cards=generate_deck(),
			name="Poker deck",
			reshuffle=False)
		self.players = players
		print(f"Created a table with {len(self.players)} players")

	def deal_cards(self,number):
		for player in self.players:
			print(f"\n{player}\'s card is:")
			for _ in range(number):
				card = self.deck.draw()
				player.hand.append(card)
				print(card)
			
				
	def cleanup(self):
		for player in self.players:
			for card in player.hand:
				self.deck.discard(card)
		for card in self.table_cards:
			self.deck.discard(card)
		self.deck.shuffle_back()
		print("Cleanup done")

def generate_deck():
	suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
	ranks = {"Ace":14,
					 "Two":2,
					 "Three":3,
					 "Four":4,
					 "Five":5,
					 "Six":6,
					 "Seven":7,
					 "Eight":8,
					 "Nine":9,
					 "Ten":10,
					 "Jack":11,
					 "Queen":12,
					 "King":13}
	cards = []
	for suit in suits:
		for name,rank in ranks.items():
			cards.append(PokerCard(suit, rank, name))
	print("Generated deck of cards for the table")
	return cards

def start():
	you = Player("You")
	jack = Player("Jack")
	ben = Player("Ben")
	mike = Player("Mike")
	table = PokerTable([you,jack,ben,mike])
	table.deck.shuffle()
	table.deal_cards(5)
	print("\nyour hand is:")
	you.show_hand()
	print("\ndo you want to replace Card?")
	print("all the index you want to replace without any seperation")
	while True:
			c_input = input(">>")
			if c_input.isdigit():
				c_l = list(c_input)
				c_l = list(map(int,c_l))
				t_l = list(filter(lambda x: x<5,c_l))
				if len(t_l) == len(c_l):
					break
	for i in c_l:
		you.replace_card(i,table)
		
	print("\nyour hand is:")
	you.show_hand()
	
	_tl = []
	winner = [0,0]
	for player in table.players:
		tmp = player.count()
		if tmp[0] > winner[0]:
			winner = tmp[:]
			truewinner = player
		elif tmp[0] == winner[0]:
			if tmp[1] > winner[1]:
				winner = tmp[:]
				truewinner = player
			elif tmp[1] == winner[1]:
				_tl.append(player)
	
	_wl = []
	for ite in _tl:
		if ite.count() == truewinner.count():
			_wl.append(ite)
	_wl.append(truewinner)
	winners = " & ".join("%s" % name for name in _wl)
	print(f"And the winner is...{winners}!")
	
	
if __name__ == "__main__":
	
	while True:
		j_input = input("enter random key to start, enter q to quit >> ")
		if j_input == "q":
			break
		start()
					
	
	


