# Initial empty list to store blockchain
# Block Property: index, timestamp(UNIX time), a list of transaction,hash of prev block,proof
# Block Chain is Instantiaited: seed it with genesis block
import hashlib
import json
from textwrap import dedent
from uuid import uuid4
from flask import Flask
from time import time


class Blockchain(object):
	# Proof of work
	def proof_of_work(self,last_proof):
		'''
		Find a number p such that hash(pp') contains 4 leading 0's
		p-> previous proof
		p'-> new proof
		'''
		proof = 0
		while self.valid_proof(last_proof,proof) is False:
			proof+=1

		return proof
		pass
	@staticmethod
	def valid_proof(last_proof,proof):
		# validates the proof
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest
		return guess_hash[:4]=="0000"
	def __init__(self):
		self.chain = [];
		self.current_transactions = []
		# create genesis block
		self.new_block(previous_hash=1,proof=100)
		
	def new_block(self,proof,previous_hash=None):
		# creates new block; adds it to chain
		block = {
			'index':len(self.chain)+1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof':proof,
			'previous_hash':self.hash(self.chain[-1])
		}
		# reset the list of transactions
		self.current_transactions = []
		return block
		pass
	def new_transaction(self,sender,recepient,amount):
		'''
		adds new transaction to list of transactions(to go into next mined block)
			sender:Address of the sender
			recepient: Address of the recepient
			amount: Amount
			return-> int : index of the block of current transaction
		'''
		self.current_transactions.append({
			'sender':sender,
			'recipient': recepient,
			'amount': amount,
		})
		return self.last_block['index']+1
	@staticmethod
	def hash(block):
		# generates hash for the block
		'''
		Create a SHA-256 hash of a block
		block: <dict> block
		return str
		'''
		# dict has to be sorted or it'll generate inconsistent hashing
		block_string = json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
		pass
	@property
	def last_block(self):
		# returns last block in the chain
		return self.chain[-1];