from collections import deque

MARKER_BUFFER_SIZE = 4
MESSAGE_BUFFER_SIZE = 14

marker_buffer = deque()
message_buffer = deque()
def check_unique(buffer, buffer_size):
    if len(buffer) < buffer_size:
        return False
    else:
        buffer = list(buffer)
        # previous solution for buffer of size 4:
        # first = buffer[0]
        # second = buffer[1]
        # third = buffer[2]
        # fourth = buffer[3]
        # first_unique = first != second and first != third and first != fourth
        # second_unique = second != third and second != fourth
        # third_unique = third != fourth
        # combinatorical decrease of checks

        # Now, we generalize above

        for i in range(buffer_size - 1): # -1 because we don't need to check the last element (combinatorical decrease of checks)
            # check each element with its sucessors
            char = buffer[i]
            if char in buffer[i+1:]:
                return False # duplicate in sucessors detected
        return True # all checked and no duplicate detected. Unique

def add_char_to_buffer(buffer, char, allowed_size):
    buffer.append(char)
    if len(buffer) > allowed_size:
        buffer.popleft()

if __name__ == "__main__":
    stream = None
    with open("input.txt") as input_file:
        stream = input_file.readline().strip("\n")
    num_chars = 0
    marker_found = False
    message_found = False
    for char in stream:
        num_chars += 1
        add_char_to_buffer(marker_buffer, char, MARKER_BUFFER_SIZE)
        add_char_to_buffer(message_buffer, char, MESSAGE_BUFFER_SIZE)

        if not marker_found:
            marker_found = check_unique(marker_buffer, MARKER_BUFFER_SIZE)
            if marker_found:
                print("Part 1:", num_chars)
        if not message_found:
            message_found = check_unique(message_buffer, MESSAGE_BUFFER_SIZE)
            if message_found:
                print("Part 2:", num_chars)
        if marker_found and message_found:
            break # no need to compute further, solutions are found