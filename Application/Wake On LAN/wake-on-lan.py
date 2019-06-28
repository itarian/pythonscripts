list1=["EC-B1-A9-2F-1A-3Z","54-0F-CF-34-9z-8A"]##give your MAC addresses here in this format
import socket
import struct

def wake_on_lan(macaddress):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
    
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = '' 

    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))
    

if __name__ == '__main__':
    for i in range(0,len(list1)):
        wake_on_lan(list1[i])
print "System is Powered ON"
