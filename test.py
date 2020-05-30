import numpy as np


user_card = []
i = 0
j = 0
while i < 5:
    row_list = []
    while j < 5:
        get_number = int(np.random.rand()*15)+1 +(15 * i)
        if get_number in row_list:
            continue
        else:
            row_list.append(get_number)
        j += 1
    j = 0
    user_card.append(row_list)
    i += 1
user_msg = {}
user_msg['use_name'] = ["user_name"]
user_msg['row_b'] = user_card[0]
user_msg['row_i'] = user_card[1]
user_msg['row_n'] = user_card[2]
user_msg['row_g'] = user_card[3]
user_msg['row_o'] = user_card[4]



print(user_msg)
print(user_msg['row_b'])
print(user_card[0])
