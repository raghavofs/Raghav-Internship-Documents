from numpy import random

flag = True
count = 0

while flag:
    x = random.rand()
    count += 1
    if x > random.rand():
        flagy = True
        flagz = True
        y = random.randint(count * x * random.rand() * 10000*2)
        count1 = 0
        count2 = 0
        while flagy:
            z = random.rand()
            count1 += 1
            if z > 0.99:
                f = z * y * random.rand()
                flagy = False
                flag = False
        while flagz: 
            w = random.rand()
            count2 += 1
            if w > 0.999:
                g = count2 * y * z * random.rand()
                product_str = str(f * g)
                count = 0
                ix = 0
                while count < 8:
                    if product_str[ix] == ".":
                        ix += 1
                    else:
                        count += 1
                        print(product_str[ix], end='')
                    ix += 1  # Move to the next character in the string
                flagz = False

