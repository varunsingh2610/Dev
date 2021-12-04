n = 0
for i in range(1, 101):

    if i % 3 == 0:
        print("Fizz")
        n += 1
    if i % 5 == 0:
        print("Buzz")
    if i % 15 == 0:
        print("FizzBuzz")

# print(n)
