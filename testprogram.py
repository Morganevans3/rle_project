


def to_hex_string(data):  # DONEEEEEEEE
    # translates data to hexadecimal string
    res = ''
    for value in data:
        if value >= 10:
            value = chr(value+87)
        res += str(value)
    return res

# print(to_hex_string([3, 15, 6, 4]))


def get_decoded_length(rle_data):  # DONEEEEE
    # returns decompressed size RLE data
    # used to generate flat data from RLE encoding (counterpart to 2)
    sum = 0
    for index, item in enumerate(rle_data):
        if index % 2 == 0:
            sum += item
    return sum

# print(get_decoded_length([3, 15, 6, 4]))



def decode_rle(rle_data):  # DONEEEE
    # returns the decoded data set from RLE encoded data
    # decompresses RLE data for use (inverse of 3)
    res = []
    for index, item in enumerate(rle_data):
        if index % 2 == 0:
            count = item
        else:
            value = item
            i = 1
            while i <= count:
                res.append(value)
                i += 1
    return res

# print(decode_rle([3, 15, 6, 4]))



def encode_rle(flat_data):
    # returns encoding in RLE of the raw data passed in
    # used to generate RLE representation of a data
    current = flat_data[0]
    count = 0
    res = []
    for item in flat_data:
        if current == item:
            count += 1
        elif current != item:
            res.append(count)
            res.append(current)
            current = item
            count = 1
            # encode_rle: append count and current into res
        if count == 15:  # special case, there should be no more than 15 elements in a group
            res.append(count)
            res.append(item)
            count = 0
    res.append(count)
    res.append(current)
    return res

# print(encode_rle([15, 15, 15, 4, 4, 4, 4, 4, 4]))
# print(encode_rle([4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))




def string_to_data(data_string):
    # translates a string in hexadecimal format into byte data
    # inverse of 1
    res = []
    mod = str(data_string)
    for value in mod:
        if value == 'a':
            res.append(10)
        elif value == 'b':
            res.append(11)
        elif value == 'c':
            res.append(12)
        elif value == 'd':
            res.append(13)
        elif value == 'e':
            res.append(14)
        elif value == 'f':
            res.append(15)
        elif value == 1:
            res.append(1)
        elif value == 2:
            res.append(2)
        elif value == 3:
            res.append(3)
        elif value == 4:
            res.append(4)
        elif value == 5:
            res.append(5)
        elif value == 6:
            res.append(6)
        elif value == 7:
            res.append(7)
        elif value == 8:
            res.append(8)
        elif value == 9:
            res.append(9)
    return res


def string_to_dat(data_string):
    # translates a string in hexadecimal format into byte data
    # inverse of 1
    res = []
    for value in data_string:
        if value == 'a':
            res.append(10)
        elif value == 'b':
            res.append(11)
        elif value == 'c':
            res.append(12)
        elif value == 'd':
            res.append(13)
        elif value == 'e':
            res.append(14)
        elif value == 'f':
            res.append(15)
        elif value == '1':
            res.append(1)
        elif value == '2':
            res.append(2)
        elif value == '3':
            res.append(3)
        elif value == '4':
            res.append(4)
        elif value == '5':
            res.append(5)
        elif value == '6':
            res.append(6)
        elif value == '7':
            res.append(7)
        elif value == '8':
            res.append(8)
        elif value == '9':
            res.append(9)  # splits 15 up
    return res

# print(string_to_data('3f64'))

# print(string_to_dat('3f64'))


def count_runs(flat_data):  # DONEEEEE
    # returns number of runs of data in an image data set
    # double this result for length of encoded (RLE) list
    current = flat_data[0]
    count = 1
    repeats = 1
    for item in flat_data[1:]:
        if current == item:
            repeats += 1
        elif current != item:  # item = 2, current = 3
            current = item
            count += 1
            repeats = 1
        if repeats == 15:
            count += 1
            repeats = 1
    return count

# print(count_runs([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))


def to_rle_string(rle_data):
    # translates RLE data into a human-readable representation
    # displays in decimal then hexadecimal and :
    # rle_data = [15, 15, 6, 4, 1, 10, 14, 11]
    res = ''
    for index, value in enumerate(rle_data):
        if index % 2 == 0:
            res += str(value)
        elif value == 15:
            res += 'f'
        elif value == 14:
            res += 'e'
        elif value == 13:
            res += 'd'
        elif value == 12:
            res += 'c'
        elif value == 11:
            res += 'b'
        elif value == 10:
            res += 'a'
        else:
            res += str(value)
        if index % 2 == 1 and value != rle_data[-1]:
            res += ':'
            
    return res


# print(to_rle_string([15, 15, 6, 4, 1, 10, 14, 11]))


def string_to_rle(rle_string):
    # translates a string to human-readable RLE format
    res = []
    strings = rle_string.split(':')
    for value in strings:  # iterate through strings
        if len(value) == 2:
            x = slice(0, 2)  # use slicing to separate 15, f, 6, 4, 1, a, 14, b
            sliced = value[x]
            for item in sliced:  # for the strings with 1 digit
                if item == 'f':
                    res.append(15)
                elif item == 'e':
                    res.append(14)
                elif item == 'd':
                    res.append(13)
                elif item == 'c':
                    res.append(12)
                elif item == 'b':
                    res.append(11)
                elif item == 'a':
                    res.append(10)
                else:
                    res.append(int(item))
        elif len(value) == 3:  # for 2 decimals
            x = slice(2, 3)
            y = slice(0, 2)
            hexa = value[x]
            dec = value[y]
            res.append(int(dec))  # int removes ''
            if hexa == 'f':
                res.append(15)
            elif hexa == 'e':
                res.append(14)
            elif hexa == 'd':
                res.append(13)
            elif hexa == 'c':
                res.append(12)
            elif hexa == 'b':
                res.append(11)
            elif hexa == 'a':
                res.append(10)
            else:
                res.append(int(hexa))

    return res


# print(string_to_rle('15f:64'))
# print(string_to_rle('15f:14b'))

initial_str = eefffffffffffffffffffffffffffffffffff2a2ffffff66fff2aa2ffff6666fff2aa22ff6666ffff2aa2fff66ff2222a2a2ffff22a2aaaaa2fff2aaaa2aaaa2f22aaaaaaaaaa22aaaaaaaaaaa2f2a222aa222aa2f2aa2f2a2ff2a2ff22ff2aa2f2aa2
print()

