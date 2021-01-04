import socket
import sys


#######################################UDP##############
s_control = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_data = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
########################################
tunnel_conn_req = b'\x06\x10\x02\x05\x00\x1a\x08\x01\xa9\xfe\xe8\xae\xe3\x56\x08\x01\xa9\xfe\xe8\xae\xe3\x57\x04\x04\x80\x00'

busmon_ack = b'\x06\x10\x04\x21\x00\x0a\x04\x09\x00\x00'

busmon_ack_2 = b'\x06\x10\x04\x21\x00\x0a\x04\x09\x01\x00'

byte = b'\x00'
#######################################
ip_router = ('169.254.182.237',3671)

################Since we are using UDP, it does not need a connection###############################################
#s1.connect(('192.168.1.4',5043)) # wifi RPI
#s1.connect(('169.254.44.247',5043)) # ethernet to RPI
#############################################################
s_control.bind(('',58198)) 
s_data.bind(('',58199))
#s_control is the socket for receiving controlling packets on port 58198
#s_data is the socket we use to receive data on port 58199
# assign a port to this socket, do not let the OS assign a random port
# since we need to know our port for later communications with ip router

s_control.sendto(tunnel_conn_req, ip_router)
tunnel_conn_res, address = s_control.recvfrom(1024)
channel = tunnel_conn_res.hex()[12:14] # sth like '09' a string!

busmon_ack = busmon_ack.hex() # now a string
####busmon_ack[14:16] = channel; illegal assignment
busmon_ack = busmon_ack[0:14] + channel + busmon_ack[16:]

busmon_ack_2 = busmon_ack_2.hex()
###busmon_ack_2[14:16] = channel;
busmon_ack_2 = busmon_ack_2[0:14] + channel + busmon_ack_2[16:]

print("now we wait for the telegram to receive")
while(True):
    busmon_ind,address_ind = s_data.recvfrom(1024)
    ###busmon_ack[16:18] = busmon_ind[16:18]
    busmon_ack = busmon_ack[0:16] + busmon_ind.hex()[16:18] + busmon_ack[18:]
    s_data.sendto(byte.fromhex(busmon_ack), ip_router)
    
    busmon_ind_2,address_ind = s_data.recvfrom(1024)
    ###busmon_ack_2[16:18] = busmon_ind_2[16:18]
    busmon_ack_2 = busmon_ack_2[0:16] + busmon_ind_2.hex()[16:18] + busmon_ack_2[18:]
    s_data.sendto(byte.fromhex(busmon_ack_2), ip_router)

    


