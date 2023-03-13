#! python3
from hashlib import sha256
from base64 import b16encode
from random import shuffle
from struct import pack, unpack

# i = lambda b: int.from_bytes(bytes=b , byteorder='little', signed=False)  # u32 from  u8[4]
# ahash_from_bytes = lambda u8_32: [
#         i(u8_32[:4]),    i(u8_32[4:8]),   i(u8_32[8:12]),  i(u8_32[12:16]),
#         i(u8_32[16:20]), i(u8_32[20:24]), i(u8_32[24:28]), i(u8_32[28:32]),
# ]
ahash_from_bytes = lambda buffer: unpack("<IIIIIIII", buffer)

# b = lambda i: i.to_bytes(length=4, byteorder='little', signed=False)  # u8[4] from u32
# bytes_from_ahash = lambda u32_8: \
#         b(u32_8[0]) + b(u32_8[1]) + b(u32_8[2]) + b(u32_8[3]) + \
#         b(u32_8[4]) + b(u32_8[5]) + b(u32_8[6]) + b(u32_8[7])
bytes_from_ahash = lambda ahash: pack("<IIIIIIII", *ahash)

add_u32 = lambda a, b: (a + b) & 0xffffffff  # add u32
add_ahash = lambda a, b: [add_u32(a[i], b[i]) for i in range(8)]

def ahash_words(words):
    total = [0,0,0,0, 0,0,0,0]
    for word in words:
        u32_8 = ahash_from_bytes(sha256(word).digest())
        total = add_ahash(total, u32_8)

    return bytes_from_ahash(total)

cases = [
    ("bip_39", "0D021C91D40FD1D87C3ECECB3DEECA30EA3768F87A6618EDD5E6878F4727D7B2"),
    ("eff_large_wordlist", "339BEABED2F5700BEFF323A75680E5A16D0DA176816665355A67817A73302782"),
    ("eff_short_wordlist_1", "70907533251C0E2B66552827B29A5C4F381F4301C961C194B066C21B005A5A73"),
    ("eff_short_wordlist_2", "618BD4C217340D8EF106048CF3341DDD6C366695F6A914233F22EF16E8E84DD3"),
    ("wordle_words5_big", "F6ED9C0621C12669791A97B71BAB582B05951F7B2827AAB31A6212381E13D769"),
    ("wordle_words5", "11013813008811902644706A2874A0E155BE2ACC17FA6FA953C9406450DF870F"),
]

hex_from_bytes = lambda b: b16encode(b).decode()

for (file_name, expected) in cases:
    words = open(file_name+".txt", 'rb').read().split()
    print(file_name, hex_from_bytes(ahash_words(words)), len(words))
    shuffle(words)
    print(file_name, hex_from_bytes(ahash_words(words)), len(words))
    words.sort()
    print(file_name, hex_from_bytes(ahash_words(words)), len(words))
    assert hex_from_bytes(ahash_words(words)) == expected

# eff_large_wordlist   = open("eff_large_wordlist.txt",   'rb').read().split()
# eff_short_wordlist_1 = open("eff_short_wordlist_1.txt", 'rb').read().split()
# eff_short_wordlist_2 = open("eff_short_wordlist_2.txt", 'rb').read().split()
# wordle_words5_big    = open("wordle_words5_big.txt",    'rb').read().split()
# wordle_words5        = open("wordle_words5.txt",        'rb').read().split()
