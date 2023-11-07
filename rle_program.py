from console_gfx import ConsoleGfx

def to_hex_string(data):  # [3, 15, 6, 4] to '3f64'
    # translates data to hexadecimal string
    res = ''
    for value in data:
        if value >= 10:
            value = chr(value+87)
        res += str(value)
    return res


def count_runs(flat_data):  # [15, 15, 15, 4, 4, 4, 4, 4, 4] to 2
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


def encode_rle(flat_data):  # [15, 15, 15, 4, 4, 4, 4, 4, 4] to [3, 15, 6, 4]
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


def get_decoded_length(rle_data):  # [3, 15, 6, 4] to 9
    # returns decompressed size RLE data
    # used to generate flat data from RLE encoding (counterpart to 2)
    sum = 0
    for index, item in enumerate(rle_data):
        if index % 2 == 0:
            sum += item
    return sum


def decode_rle(rle_data):  # [3, 15, 6, 4] to [15, 15, 15, 4, 4, 4, 4, 4, 4]
    # returns the decoded data set from RLE encoded data
    # decompresses RLE data for use (inverse of 3)
    res = []
    count = 0
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


def string_to_data(data_string):  # '3f64' to [3, 15, 6, 4]
    # translates a string in hexadecimal format into byte data
    # inverse of 1
    res = []
    for value in data_string[0:]:
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
        else:
            res.append(int(value))
    return res


def to_rle_string(rle_data):  # [15, 15, 6, 4] to '15f:64'
    # translates RLE data into a human-readable representation
    # displays in decimal then hexadecimal and :
    res = ''
    count = len(rle_data) - 1
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
        if index % 2 == 1 and index < count:
            res += ':'
        # rle_data = [15, 15, 6, 4, 1, 10, 14, 11]

    return res

def string_to_rle(rle_string):  # '15f:64' to [15, 15, 6, 4]
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


if __name__ =='__main__':
    # set up welcome messages
    print('Welcome to the RLE image encoder!')
    print('')
    print('Displaying Spectrum Image:')
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
    # change color scheme of mac

    # ConsoleGfx.display_image(ConsoleGfx.test_image)

    image_data = None
    cont = True
    while cont:
        # prompt for the user input for menu choice
        print('\nRLE Menu')
        print('-' * 8)
        print('0. Exit')
        print('1. Load File')
        print('2. Load Test Image')
        print('3. Read RLE String')
        print('4. Read RLE Hex String')
        print('5. Read Data Hex String')
        print('6. Display Image')
        print('7. Display RLE String')
        print('8. Display Hex RLE Data')
        print('9. Display Hex Flat Data')
        print('')
        option = int(input("Select a Menu Option: "))
        if option == 0:
            cont = False
        elif option == 1:  # load image data from file
            # read the image data from file
            filename = str(input('Enter name of file to load: '))
            image_data = ConsoleGfx.load_file(filename)  # file name is user input testfiles/fsu.gfx
            # store the image data in the image_data variable
        elif option == 2:  # load image data from test_image
            # assign ConsoleGfx.test_image to image_data
            # image_data = ConsoleGfx.test_image
            image_data = ConsoleGfx.test_image
            print('Test image data loaded.')
        elif option == 3:
            # read RLE String
            # 28:10:6B:10
            rle_str = input('Enter an RLE string to be decoded: ')
            rle_byte = string_to_rle(rle_str)
            flat_byte = decode_rle(rle_byte)

        elif option == 4:
            # read RLE Hex String
            # 28106B10AB
            hex_rle = input('Enter the hex string holding RLE data: ')
            rle_byte = string_to_data(hex_rle)
            flat_byte = decode_rle(rle_byte)

        elif option == 5:
            # read Data Hex String
            # 880bbbbbb0
            hex_data = input('Enter the hex string holding flat data: ')
            flat_byte = string_to_data(hex_data)

        elif option == 6:
            # display the image
            print('Displaying image...')
            ConsoleGfx.display_image(image_data)
        elif option == 7:
            # Display RLE String
            # 28:10:6b:10:10b
            rle_byte = encode_rle(flat_byte)
            rle_string = to_rle_string(rle_byte)
            print('RLE representation:', rle_string)

        elif option == 8:
            # Display Hex RLE Data
            # 28106b10ab
            rle_byte = encode_rle(flat_byte)
            rle_hex = to_hex_string(rle_byte)
            print('RLE hex values:', rle_hex)

        elif option == 9:
            # Display Hex Flat Data
            # 880bbbbb0
            flat_str = to_hex_string(flat_byte)
            print('Flat hex values:', flat_str)
