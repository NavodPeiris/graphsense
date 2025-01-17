
from math import sqrt
from maths.greatest_common_divisor import gcd_by_iterative

def is_prime(number: int) -> bool:

    assert isinstance(number, int) and (number >= 0), (
        "'number' must been an int and positive"
    )

    status = True

    if number <= 1:
        status = False

    for divisor in range(2, int(round(sqrt(number))) + 1):
        if number % divisor == 0:
            status = False
            break

    assert isinstance(status, bool), "'status' must been from type bool"

    return status


def sieve_er(n):

    assert isinstance(n, int) and (n > 2), "'N' must been an int and > 2"
    begin_list = list(range(2, n + 1))
    ans = []  

    for i in range(len(begin_list)):
        for j in range(i + 1, len(begin_list)):
            if (begin_list[i] != 0) and (begin_list[j] % begin_list[i] == 0):
                begin_list[j] = 0

    ans = [x for x in begin_list if x != 0]

    assert isinstance(ans, list), "'ans' must been from type list"
    return ans


def get_prime_numbers(n):
    assert isinstance(n, int) and (n > 2), "'N' must been an int and > 2"
    ans = []

    for number in range(2, n + 1):
        if is_prime(number):
            ans.append(number)

    assert isinstance(ans, list), "'ans' must been from type list"
    return ans


def prime_factorization(number):
    assert isinstance(number, int) and number >= 0, "'number' must been an int and >= 0"
    ans = []  

    factor = 2
    quotient = number

    if number in {0, 1}:
        ans.append(number)
    elif not is_prime(number):
        while quotient != 1:
            if is_prime(factor) and (quotient % factor == 0):
                ans.append(factor)
                quotient /= factor
            else:
                factor += 1
    else:
        ans.append(number)

    assert isinstance(ans, list), "'ans' must been from type list"
    return ans


def greatest_prime_factor(number):
    assert isinstance(number, int) and (number >= 0), (
        "'number' must been an int and >= 0"
    )

    ans = 0   
    prime_factors = prime_factorization(number)
    ans = max(prime_factors)

    assert isinstance(ans, int), "'ans' must been from type int"
    return ans


def smallest_prime_factor(number): 
    assert isinstance(number, int) and (number >= 0), (
        "'number' must been an int and >= 0"
    )

    ans = 0
    prime_factors = prime_factorization(number)
    ans = min(prime_factors)

    assert isinstance(ans, int), "'ans' must been from type int"
    return ans


def is_even(number):
    assert isinstance(number, int), "'number' must been an int"
    assert isinstance(number % 2 == 0, bool), "compare must been from type bool"

    return number % 2 == 0


def is_odd(number):
    assert isinstance(number, int), "'number' must been an int"
    assert isinstance(number % 2 != 0, bool), "compare must been from type bool"

    return number % 2 != 0


def goldbach(number):
    assert isinstance(number, int) and (number > 2) and is_even(number), (
        "'number' must been an int, even and > 2"
    )

    ans = []  
    prime_numbers = get_prime_numbers(number)
    len_pn = len(prime_numbers)

    i = 0
    j = None

    loop = True

    while i < len_pn and loop:
        j = i + 1

        while j < len_pn and loop:
            if prime_numbers[i] + prime_numbers[j] == number:
                loop = False
                ans.append(prime_numbers[i])
                ans.append(prime_numbers[j])

            j += 1

        i += 1

    
    assert (
        isinstance(ans, list)
        and (len(ans) == 2)
        and (ans[0] + ans[1] == number)
        and is_prime(ans[0])
        and is_prime(ans[1])
    ), "'ans' must contains two primes. And sum of elements must been eq 'number'"

    return ans


def kg_v(number1, number2):
    assert (
        isinstance(number1, int)
        and isinstance(number2, int)
        and (number1 >= 1)
        and (number2 >= 1)
    ), "'number1' and 'number2' must been positive integer."

    ans = 1  

    if number1 > 1 and number2 > 1:
        
        prime_fac_1 = prime_factorization(number1)
        prime_fac_2 = prime_factorization(number2)

    elif number1 == 1 or number2 == 1:
        prime_fac_1 = []
        prime_fac_2 = []
        ans = max(number1, number2)

    count1 = 0
    count2 = 0

    done = []  

    for n in prime_fac_1:
        if n not in done:
            if n in prime_fac_2:
                count1 = prime_fac_1.count(n)
                count2 = prime_fac_2.count(n)
                for _ in range(max(count1, count2)):
                    ans *= n
            else:
                count1 = prime_fac_1.count(n)
                for _ in range(count1):
                    ans *= n

            done.append(n)

    
    for n in prime_fac_2:
        if n not in done:
            count2 = prime_fac_2.count(n)
            for _ in range(count2):
                ans *= n

            done.append(n)

    
    assert isinstance(ans, int) and (ans >= 0), (
        "'ans' must been from type int and positive"
    )

    return ans


def get_prime(n):
    assert isinstance(n, int) and (n >= 0), "'number' must been a positive int"

    index = 0
    ans = 2  

    while index < n:
        index += 1
        ans += 1  

        while not is_prime(ans):
            ans += 1

    assert isinstance(ans, int) and is_prime(ans), (
        "'ans' must been a prime number and from type int"
    )

    return ans


def get_primes_between(p_number_1, p_number_2):
    assert (
        is_prime(p_number_1) and is_prime(p_number_2) and (p_number_1 < p_number_2)
    ), "The arguments must been prime numbers and 'pNumber1' < 'pNumber2'"

    number = p_number_1 + 1  
    ans = []  

    while not is_prime(number):
        number += 1

    while number < p_number_2:
        ans.append(number)
        number += 1

        while not is_prime(number):
            number += 1

    assert (
        isinstance(ans, list)
        and ans[0] != p_number_1
        and ans[len(ans) - 1] != p_number_2
    ), "'ans' must been a list without the arguments"

    return ans


def get_divisors(n):
    assert isinstance(n, int) and (n >= 1), "'n' must been int and >= 1"
    ans = []  

    for divisor in range(1, n + 1):
        if n % divisor == 0:
            ans.append(divisor)

    assert ans[0] == 1 and ans[len(ans) - 1] == n, "Error in function getDivisiors(...)"
    return ans


def is_perfect_number(number):
    assert isinstance(number, int) and (number > 1), (
        "'number' must been an int and >= 1"
    )

    divisors = get_divisors(number)

    assert (
        isinstance(divisors, list)
        and (divisors[0] == 1)
        and (divisors[len(divisors) - 1] == number)
    ), "Error in help-function getDivisiors(...)"

    return sum(divisors[:-1]) == number


def simplify_fraction(numerator, denominator):
    assert (
        isinstance(numerator, int)
        and isinstance(denominator, int)
        and (denominator != 0)
    ), "The arguments must been from type int and 'denominator' != 0"

    gcd_of_fraction = gcd_by_iterative(abs(numerator), abs(denominator))

    assert (
        isinstance(gcd_of_fraction, int)
        and (numerator % gcd_of_fraction == 0)
        and (denominator % gcd_of_fraction == 0)
    ), "Error in function gcd_by_iterative(...,...)"

    return (numerator // gcd_of_fraction, denominator // gcd_of_fraction)


def factorial(n):
    return 1 if n == 1 else n * factorial(n - 1)


def fib(n: int) -> int:
    assert isinstance(n, int) and (n >= 0), "'n' must been an int and >= 0"

    tmp = 0
    fib1 = 1
    ans = 1  

    for _ in range(n - 1):
        tmp = ans
        ans += fib1
        fib1 = tmp

    return ans


if __name__ == "__main__":
    import doctest

    doctest.testmod()
