# --- list comprehensions --- :

# [print("Fizz"*(i%3==0)+"Buzz"*(i%5==0) or i) for i in range(101)]

# [print("Even") if i%2==0 else print("Odd") for i in range(10)]

# (lambda max: [print(f"{i.split(' ')[0]}'s score is {i.split(' ')[1]}") if x <= max-1 else quit() for x, i in enumerate(["toby 100", "jake 200", "gabe 234", "joe 104", "louis 90"])])(2)
# ^ stupid mega function??

# def wrap(string, max_width):
#    return "\n".join([string[i:i+max_width] for i in range(0, len(string), max_width)])

# print(wrap("ABCDEFGHIJ", 4))


# my_list = ["toby 90", "jake 80", "toby 90"]


#  new_list = map(lambda x: x.split(' ')[1], my_list)
# [print(i) for i in new_list]

# print(sorted(my_list, key=lambda x: x.split(' ')[1]))

# print(int(not 1))


# this file is used to experiment with various programming techniques
