import random
import string

def generate_random_id():
    chars = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choices(chars, k=4))
    part2 = ''.join(random.choices(chars, k=3))
    part3 = ''.join(random.choices(chars, k=3))
    part4 = ''.join(random.choices(chars, k=3))
    part5 = ''.join(random.choices(chars, k=4))
    return f"{part1}-{part2}-{part3}-{part4}-{part5}"

print(generate_random_id())
