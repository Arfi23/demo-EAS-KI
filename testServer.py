import socket
import pickle
from des import encrypt, string_to_int, int_to_string
from rsa import createPublicKey, createPrivateKey, dec, dec_to_hex

p = 61
q = 89
# p = 7
# q = 13
n = p * q
e, tn = createPublicKey(p, q)

d = createPrivateKey(e, tn)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # membuat objek socket, AF-INET : protokol IPv4, SOCK_STREAM : socket tipe stream untuk TCP
server_address = ('localhost', 10235)
server_socket.bind(server_address)
server_socket.listen(1)
print("Server mendengarkan di", server_address)

client_socket, client_address = server_socket.accept() # hasil return berupa objek socket baru (client) dan alamat client
print("Terhubung ke", client_address)
print("=======================================================")

# Mengirim e, tn, n ke client
data_to_send = {'e': e, 'tn': tn, 'n': n}
serialized_data = pickle.dumps(data_to_send)
client_socket.sendall(serialized_data)

# Menerima pesan terenkripsi dari client
received_data = client_socket.recv(4096)
data_dict = pickle.loads(received_data)

# Proses dekripsi menggunakan private key dan assign ke variable kunci
rec_e_enc = data_dict['e_enc']
d_dec = dec(rec_e_enc, d, n)
kunci_string = dec_to_hex(d_dec)
kunci = int(kunci_string, 16)

# test
# print("Nilai private key d:", d)
# print("Private key berhasil dibuat!")
# print("menerima pesan terenkripsi rec_e_enc: ", rec_e_enc)
# print("isi hasil dekripsi d_dec: ", d_dec)
# print("kunci berupa string hexadecimal:", kunci_string)
# print("kunci yang digunakan (versi integer):", kunci)
# print("=======================================================")


print(f" ~ percakapan ini terenkripsi dengan key: {kunci_string} yang dikirim oleh client ~")
print("==================================================================================")

# Percakapan terenkripsi
while True:
    # Menerima pesan terenkripsi dari klien
    data_received = client_socket.recv(1024)
    print("Pesan terenkripsi dari client: ", data_received.decode('utf-8')) ###
    if not data_received:
        print("Koneksi ditutup oleh klien.")
        break  # Koneksi ditutup oleh klien

# Jika pesan yang diterima dari client berupa "exit123", koneksi diputus
    if data_received.decode('utf-8').lower() == "koneksi ditutup oleh client":
        print("Koneksi ditutup oleh client.")
        break  # Koneksi ditutup oleh client

    # Dekripsi pesan
    decrypted_message = int_to_string(encrypt(int(data_received), kunci, True))
    print("<-- Client (Decrypted):", str(decrypted_message))

    # Mengetikkan pesan untuk dikirim ke klien
    message_to_send = input("--> Server: ")
    
    # Jika server mengirimkan "exit123", server menutup koneksi
    if message_to_send.lower() == "exit123":
        print("Server meminta penutupan koneksi.")
        message_to_send = "koneksi ditutup oleh server"
        # encrypted_message = encrypt(string_to_int(message_to_send), kunci)
        client_socket.sendall(str(message_to_send).encode('utf-8'))
        break  # Koneksi ditutup oleh server
    
    # Mengirim pesan terenkripsi ke klien
    encrypted_message = encrypt(string_to_int(message_to_send), kunci)
    print("Pesan terenkripsi yang dikirim: ", str(encrypted_message)) #
    client_socket.sendall(str(encrypted_message).encode('utf-8'))

client_socket.close()
server_socket.close()
