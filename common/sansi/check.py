def gen_crc(buffer, buffer_length):
    """
    CRC校验
    :param buffer:
    :param buffer_length:
    :return:2字节的校验码
    """
    c, treat, bcrc = 0, 0, 0
    wcrc = 0
    for i in range(buffer_length):
        c = buffer[i]
        for j in range(8):
            treat = c & 0x80
            c <<= 1
            bcrc = (wcrc >> 8) & 0x80
            wcrc <<= 1
            if treat != bcrc:
                wcrc ^= 0x1021
    return wcrc


def transferred_meaning(byte_data: bytes):
    """
    0x02 转换为 0x1B, 0xE7
    0x03 转换为 0x1B, 0xE8
    0x1B 转换为 0x1B, 0x00
    :param byte_data:
    :return:
    """
    new_byte_data = bytearray()

    i = 0
    while i < len(byte_data):
        by_val = byte_data[i]
        if by_val == 0x02:
            new_byte_data.append(0x1b)
            new_byte_data.append(0xe7)
            i += 1
        elif by_val == 0x03:
            new_byte_data.append(0x1b)
            new_byte_data.append(0xe8)
            i += 1
        elif by_val == 0x00:
            new_byte_data.append(0x1b)
            new_byte_data.append(0x00)
            i += 1
        else:
            new_byte_data.append(by_val)
            i += 1

    return new_byte_data


def un_transferred_meaning(byte_data):
    """
    0x1B, 0xE7 → 0x02
    0x1B, 0xE8 → 0x03
    0x1B, 0x00 → 0x1B
    :param byte_data:
    :return:new_byte_data
    """
    new_byte_data = bytearray()

    i = 0
    while i < len(byte_data):
        by_val = byte_data[i]
        if i + 1 < len(byte_data):
            by_next_val = byte_data[i + 1]
            if by_val == 0x1b and by_next_val == 0xe7:
                new_byte_data.append(0x02)
                i += 2
            elif by_val == 0x1b and by_next_val == 0xe8:
                new_byte_data.append(0x03)
                i += 2
            elif by_val == 0x1b and by_next_val == 0x00:
                new_byte_data.append(0x1b)
                i += 2
            else:
                new_byte_data.append(by_val)
                i += 1
        else:
            new_byte_data.append(by_val)
            i += 1

    return new_byte_data
