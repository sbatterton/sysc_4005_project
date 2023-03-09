from random import randint

#adapted from instructions in chapter 7, slide 12

#function for generating the random numbers, with n being the amount
def combined_linear_congruential_generator(n):
    #empty list which will hold the random numbers
    randoms = []

    #assigning values for m and a
    m1 = 2147483563
    a1 = 40014
    m2 = 2147483399
    a2 = 40692

    #using python random library to generate the seed
    x1 = randint(1, m1 - 1)
    x2 = randint(1, m2 - 1)

    for i in range(0, n):
        #step 2
        x1 = a1 * x1 % m1
        x2 = a2 * x2 % m2

        #step 3
        x = (x1 - x2) % (m1 - 1)

        #step 4
        if x > 0:
            randoms.append(x / m1)
        else:
            randoms.append((m1 - 1) / m1)
    
    return randoms

for n in combined_linear_congruential_generator(300):
    print(n)