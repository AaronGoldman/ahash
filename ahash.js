import { createHash } from 'node:crypto'
import {readFileSync} from 'fs'
import { assert } from 'node:console'


function ahash(content) {
    let digest = createHash('sha256').update(content).digest()
    return [
        digest.readUInt32LE( 0), digest.readUInt32LE( 4),
        digest.readUInt32LE( 8), digest.readUInt32LE(12),
        digest.readUInt32LE(16), digest.readUInt32LE(20),
        digest.readUInt32LE(24), digest.readUInt32LE(28),
    ]
}

function hex_from_ahash(ahash){
    console.log(ahash)
    return Buffer.from(new Uint32Array(ahash).buffer).toString('hex').toUpperCase()
}

function add_ahash(a, b){
    for (var i=0; i<8; i++){
        a[i] = (a[i] + b[i]) % 0x100000000
    }
    return a
}

function ahash_words(words){
    let total = [0,0,0,0, 0,0,0,0]
    for (let word of words){
        const u32_8 = ahash(word)
        total = add_ahash(total, u32_8)
    }
    return hex_from_ahash(total)
}

let cases = [
    ["bip_39", "0D021C91D40FD1D87C3ECECB3DEECA30EA3768F87A6618EDD5E6878F4727D7B2"],
    ["eff_large_wordlist", "339BEABED2F5700BEFF323A75680E5A16D0DA176816665355A67817A73302782"],
    ["eff_short_wordlist_1", "70907533251C0E2B66552827B29A5C4F381F4301C961C194B066C21B005A5A73"],
    ["eff_short_wordlist_2", "618BD4C217340D8EF106048CF3341DDD6C366695F6A914233F22EF16E8E84DD3"],
    ["wordle_words5_big", "F6ED9C0621C12669791A97B71BAB582B05951F7B2827AAB31A6212381E13D769"],
    ["wordle_words5", "11013813008811902644706A2874A0E155BE2ACC17FA6FA953C9406450DF870F"],
]

for (let test of cases) {
    const file_name = test[0]
    const expected = test[1]
    const words = readFileSync(file_name + '.txt').toString().split(" ")
    const result = ahash_words(words)
    assert(result == expected)
    console.log(file_name, result, words.length)
}
