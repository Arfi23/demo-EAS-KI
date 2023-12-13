import socket
import pickle
from des import encrypt, string_to_int, int_to_string
from rsa import createPrivateKey, enc, dec_to_hex, totientOf, altTotientOf

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # membuat objek socket, AF-INET : protokol IPv4, SOCK_STREAM : socket tipe stream untuk TCP
server_address = ('localhost', 10235)
client_socket.connect(server_address)
print("Terhubung ke server di", server_address)

# kunci = 0xABCDEF1234567890
# kunci = 0x0000000000000017 # jika p=7, q=13

kunci = 0x0000000000000FFF
dec_num = int('0x0000000000000FFF', 16)
m = dec_num

# Menerima data e, tn, n dari server
received_data = client_socket.recv(4096)
data_dict = pickle.loads(received_data)

# Mendapatkan nilai e dan tn
e = data_dict['e']
tn = data_dict['tn']
n = data_dict['n']

# jika tn tidak boleh dikirim, hanya n saja, maka fungsi totientOf akan digunakan dengan argumen n

# enkripsi pesan sebelum dikirim ke server
e_enc = enc(m, e, n)


data_to_send = {'e_enc': e_enc}
serialized_data = pickle.dumps(data_to_send)
client_socket.sendall(serialized_data)


# test
# print("Nilai e:", e)
# print("Nilai tn:", tn)
# print("Nilai n:", n)

# Percakapan terenkripsi
while True:
    # Meminta pengguna memasukkan pesan untuk dikirim ke server
    message_to_send = input("--> Client: ")
    
    # Jika client mengetik "exit123", client menutup koneksi
    if message_to_send.lower() == "exit123":
        print("Anda meminta penutupan koneksi.")
        message_to_send = "koneksi ditutup oleh client"
        # encrypted_message = encrypt(string_to_int(message_to_send), kunci)
        client_socket.sendall(str(message_to_send).encode('utf-8'))
        break  # Koneksi ditutup oleh client

    # Mengirim pesan terenkripsi ke server
    encrypted_message = encrypt(string_to_int(message_to_send), kunci)
    print("Pesan terenkripsi yang dikirim: ", encrypted_message)
    client_socket.sendall(str(encrypted_message).encode('utf-8'))

    # Menerima pesan terenkripsi dari server
    data_received = client_socket.recv(1024)
    print("Pesan terenkripsi dari server: ", data_received.decode('utf-8')) ###

    if not data_received:
        print("Koneksi ditutup oleh server.")
        break  # Koneksi ditutup oleh server

    if data_received.decode('utf-8').lower() == "koneksi ditutup oleh server":
        print("Koneksi ditutup oleh server.")
        break  # Koneksi ditutup oleh server

    # Dekripsi pesan
    decrypted_message = int_to_string(encrypt(int(data_received), kunci, True))
    print("<-- Server (Decrypted):", str(decrypted_message))

client_socket.close()
