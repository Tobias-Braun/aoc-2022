
MAX_NUM_LENGTH = 2

def prettify_num(num: any):
    num = str(num)
    len_diff = MAX_NUM_LENGTH - len(num)
    if len_diff == 0:
        return num
    else:
        return "0" * len_diff + num
