import random
import math

# fungsi untuk memeriksa bilangan prima
def is_prime(n):
    # 1 bukan bilangan prima
    if n == 1:
        return False

    i = 2
    # Loop dari 2 sampai int(sqrt(x)) - akar kuadrat dari bilangan yang diperiksa
    while i*i <= n:
        # Periksa apakah i adalah faktor dari n
        if n % i == 0:
            # terdapat faktor antara 2 dan sqrt(n) -> bukan prima
            return False
        i += 1
    # true ketika tidak ada faktor di antara 2 hingga sqrt(n) - 
    # tidak ada pasangan perkalian untuk faktor yang lebih besar dari sqrt(n)
    return True

# fungsi untuk membuat public key e
def createPublicKey(p, q):
    n = p * q
    tn = (p-1) * (q-1)

    pos_e = []

    # loop mencari e
    for i in range(2, tn):
        if (is_prime(i) and n % i != 0 and tn % i != 0):
            pos_e.append(i)

    e = random.choice(pos_e)
    print(pos_e)
    return e, tn

# fungsi untuk membuat private key d - inverse mod
# def createPrivateKey(e, tn):
#     d = pow(e, -1, tn)
#     if(d != e):
#         return d
#     else:
#         return createPrivateKey(e, tn)

# fungsi yang sama dengan yang di atas, dengan penulisan lebih pendek
def createPrivateKey(e, tn):
    d = pow(e, -1, tn)
    return d if (d != e) else createPrivateKey(e, tn)

# catatan : Jika nilai tn tidak boleh dikirim langsung oleh server, melainkan server
#           hanya boleh mengirim nilai n (bukan tn), maka tn harus dicari dengan fungsi 
#           totientOf atau altTotientOf terlebih dahulu, lalu setelah itu dijadikan
#           argumen pemanggilan fungsi createPrivateKey

# fungsi untuk enkripsi pesan
def enc(m, e, n):
    return pow(m, e, n)

# fungsi untuk dekripsi pesan
def dec(m, d, n):
    return pow(m, d, n)

# fungsi untuk mengubah bilangan decimal menjadi string hexadecimal
def dec_to_hex(a):
    hex_string = '0x' + format(a, '016X')
    return hex_string

# fungsi untuk mencarikan nilai totient untuk hasil perkalian p dan q
def totientOf(x):
    coprimes = []
    if(is_prime(x)):
        return x-1
    else:
        for i in range(1, x):
            if (math.gcd(i, x) == 1):
                coprimes.append(i)
        # print("bilangan coprime-nya: ", coprimes)
        return len(coprimes)

# fungsi lain untuk mencarikan nilai totient untuk hasil perkalian p dan q
def altTotientOf(y):
    cop = []
    for i in range (1, y):
        if math.gcd(i, y) == 1:
            cop.append(i)
    # print("bilangan coprime-nya: ", cop)
    return len(cop)

# catatan : kedua fungsi baik totientOf dan altTotientOf tersebut bisa digunakan, jika
#           nilai variabel tn tidak boleh dikirim oleh server ke client (karena tn diasumsikan bersifat rahasia), 
#           hal ini berarti, hanya boleh mengirimkan nilai variabel n saja, setelah itu client melakukan 
#           pembuatan private key dengan terlebih dahulu mencari nilai totient dari n. Setelah 
#           diperoleh tn-nya, maka tn itu bisa digunakan pada fungsi createPrivateKey. Fungsi totientOf dan altTotientOf
#           ini diasumsikan harus rahasia atau tidak diketahui algoritma fungsinya secara publik