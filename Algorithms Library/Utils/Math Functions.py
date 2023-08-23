from functools import reduce

def gcd(x, y): #Greatest Common Divisor
   while(y):
       x, y = y, x % y
   return x

def get_gcd(number_list):
    return reduce(gcd, number_list)

def lcm(x, y): # Lowest Common Multiple
    return x * y // gcd(x, y)

def get_lcm(number_list):
    return reduce(lcm, number_list)

def prime_gen():
    yield 2
    yield 3
    prime_list = [2,3]
    while True:
        i = 2
        while True:
            isprime = True
            n = prime_list[-1] + i
            for p in prime_list:
                if p > n ** 0.5:
                    break
                if not n % p:
                    isprime = False
                    break
            if isprime == True:
                prime_list.append(n)
                break
            i += 2
        yield prime_list[-1]
            
def get_nth_prime(n):
    i = 0
    for p in prime_gen():
        i += 1
        if i == n:
            return p

from functools import *

def factors(n): #This function returns ALL the factors of a number
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

import itertools as it
def erat3( ): #Best prime gen
    D = { 9: 3, 25: 5 }
    yield 2
    yield 3
    yield 5
    MASK= 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS= frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )

    for q in it.compress(
            it.islice(it.count(7), 0, None, 2),
            it.cycle(MASK)):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D or (x%30) not in MODULOS:
                x += 2*p
            D[x] = p

def get_recur_string(dividend, divisor): #Returns the raw recurring section of a division quotient
    quotients = [0]
    recur_value = dividend
    quotient = ""

    while recur_value not in quotients:
        quotients.append(recur_value)
        wq, recur_value = divmod(recur_value, divisor)
        quotient += str(wq)
        recur_value *= 10

    if not recur_value:
        return None
    
    return quotient[quotients.index(recur_value)-1:]


def get_recur_len(dividend, divisor): #Returns the raw length of the recurring section of a division quotient
    quotients = {0: 0}
    recur_value = dividend
    recur_len = 0

    while recur_value not in quotients:
        quotients[recur_value] = recur_len
        recur_value = recur_value % divisor * 10
        recur_len += 1

    if not recur_value:
        return 0

    recur_len -= quotients[recur_value]
    
    return recur_len