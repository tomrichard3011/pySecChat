import random
# 7 digits is a good amount of time.
prime = 8695223
base = 5

alice_secret = random.randint(1, prime)
bob_secret = random.randint(1, prime)

A = (base**alice_secret)%prime
B = (base**bob_secret)%prime

s = (B ** alice_secret) % prime
print(s)
s = (A ** bob_secret) % prime
print(s)
