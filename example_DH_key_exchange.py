import random

prime = 8695223
base = 13
# alice and bob pick a random number
alice_secret_num = random.randint(1, prime)
bob_secret_num = random.randint(1, prime)

# they both generate a secret key they can send over a network
alice_key = (base**alice_secret_num) % prime
bob_key = (base**bob_secret_num) % prime

# alice calculates the shared key
s = (bob_key ** alice_secret_num) % prime
print(s)
# bob calculates the shared key
s = (alice_key ** bob_secret_num) % prime
print(s)
