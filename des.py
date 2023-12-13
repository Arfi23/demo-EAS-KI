import random

# Tabel Permutasi dan S-box

# Matriks Permutasi Awal (Initial Permutation)
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
# Matriks Invers Permutasi Awal
IP_INV = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
)
# Matriks PC-1 (untuk keperluan generate internal key)
PC1 = (
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
)
# Matriks PC-2 (untuk keperluan generate internal key)
PC2 = (
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)
# Matriks Ekspansi E (digunakan di dalam fungsi transformasi f pada jaringan Feistel)
E  = (
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)
# Substitution Box (digunakan di dalam fungsi transformasi f, di-XOR bersama hasil ekspansi (A))
Sboxes = {
    0: (
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ),
    1: (
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
        3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
        0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9 
    ),
    2: (
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
        1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 
    ),
    3: (
        7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
        3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ),
    4: (
        2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
        4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ),
    5: (
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
        9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
        4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ),
    6: (
        4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
        1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
        6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ),
    7: (
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
        1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
        7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
        2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    )
}
# Matriks permutasi P (digunakan di dalam fungsi transformasi f untuk permutasi blok hasil s-box (B))
P = (
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11, 4,  25
)
    
def encrypt(msg, key, decrypt=False):
    # 
    assert isinstance(msg, int) and isinstance(key, int)
    assert not msg.bit_length() > 64
    assert not key.bit_length() > 64

    # permutasi menggunakan PC-1
    key = permutation_by_table(key, 64, PC1) # 64bit -> PC1 -> 56bit

    # external key dibagi dua (28-28)
    # untuk membuat 16 round internal key
    C0 = key >> 28
    D0 = key & (2**28-1)
    round_keys = generate_round_keys(C0, D0) # 56bit -> PC2 -> 48bit

    msg_block = permutation_by_table(msg, 64, IP)
    L0 = msg_block >> 32
    R0 = msg_block & (2**32-1)

    # menerapkan jaringan Feistel untuk 16 round
    L_last = L0
    R_last = R0
    for i in range(1,17):
        if decrypt: # untuk decrypt dapat menggunakan round keys dalam urutan terbalik
            i = 17-i
        L_round = R_last # Li = Ri-1
        R_round = L_last ^ round_function(R_last, round_keys[i]) # Ri = Li-1 XOR fungsi f (round function)
        L_last = L_round
        R_last = R_round

    # menggabungkan yang terbalik
    cipher_block = (R_round<<32) + L_round

    # permutasi akhir dengan matriks IP_INV
    cipher_block = permutation_by_table(cipher_block, 64, IP_INV)

    return cipher_block

def round_function(Ri, Ki):
    # melakukan ekspansi pada Ri menggunakan matriks Ekspansi E (32->48)
    Ri = permutation_by_table(Ri, 32, E)

    # xor dengan round key
    Ri ^= Ki # A

    # membagi Ri menjadi 8 kelompok (8 blok) berisikan 6 bit tiap kelompok
    Ri_blocks = [((Ri & (0b111111 << shift_val)) >> shift_val) for shift_val in (42,36,30,24,18,12,6,0)]

    # memetakan setiap blok berisi 6 bit (kelompok bit) untuk setiap s-box
    for i, block in enumerate(Ri_blocks):
        # mengambil bit
        row = ((0b100000 & block) >> 4) + (0b1 & block)
        col = (0b011110 & block) >> 1
        # sbox disimpan sebagai tupel satu dimensi, jadi kita perlu menghitung indeks dengan cara ini
        Ri_blocks[i] = Sboxes[i][16*row+col]

    # blok kembali digabung
    Ri_blocks = zip(Ri_blocks, (28,24,20,16,12,8,4,0))
    Ri = 0
    for block, lshift_val in Ri_blocks:
        Ri += (block << lshift_val)

    # B
    # dari proses sebelumnya, diperoleh 32 bit (6 bit -> 4 bit * 8 kelompok = 32),
    # Permutasi Ri (32 bit) dengan menggunakan matriks P sebelum menjadi output dari fungsi f / round function
    Ri = permutation_by_table(Ri, 32, P)

    return Ri

def permutation_by_table(block, block_len, table):
    # 
    block_str = bin(block)[2:].zfill(block_len)
    perm = []
    for pos in range(len(table)):
        perm.append(block_str[table[pos]-1])
    return int(''.join(perm), 2)

def generate_round_keys(C0, D0):
    # return dict berisi 16 internal key (1 round 1 key)

    round_keys = dict.fromkeys(range(0,17))
    lrot_values = (1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1)

    # fungsi left-rotation
    lrot = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

    # rotasi awal
    C0 = lrot(C0, 0, 28)
    D0 = lrot(D0, 0, 28)
    round_keys[0] = (C0, D0)

    # membuat 16 pasang key berbeda
    for i, rot_val in enumerate(lrot_values):
        i+=1
        Ci = lrot(round_keys[i-1][0], rot_val, 28)
        Di = lrot(round_keys[i-1][1], rot_val, 28)
        round_keys[i] = (Ci, Di)

    # round_keys[1] untuk round satu
    #           [16] untuk round dua
    # tidak lagi membutuhkan round_keys[0], maka dihapus
    del round_keys[0]

    # membuat key dari gabungan CiDi 1<=i<=16 dengan juga menerapkan permutasi PC-2
    for i, (Ci, Di) in round_keys.items():
        Ki = (Ci << 28) + Di
        round_keys[i] = permutation_by_table(Ki, 56, PC2) # 56bit -> 48bit

    return round_keys


# string->byte[e-utf-8]->rep-hex->int
def string_to_int(message):
    return int(message.encode('utf-8').hex(), 16)

# int->rep-hex[2:=remove 0x]->byte[bytes.fromhex]->string[d-utf-8]
def int_to_string(number):
    hex_string = hex(number)[2:]
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    return bytes.fromhex(hex_string).decode('utf-8')



# k = 0xABCDEF1234567890
# # m = 0x2323232323232323
# m = 0x1010101010101010


# def coba():    
#     kunci_heksadesimal = 0x1234567890ABCDEF
#     print(kunci_desimal)

# def test(key, msg):
#     print('key:       {:x}'.format(key))
#     print('message:   {:x}'.format(msg))
#     cipher_text = encrypt(msg, key)
#     print('encrypted: {:x}'.format(cipher_text))
#     plain_text = encrypt(cipher_text, key, decrypt=True)
#     print('decrypted: {:x}'.format(plain_text))

# test(k, m)
# coba()