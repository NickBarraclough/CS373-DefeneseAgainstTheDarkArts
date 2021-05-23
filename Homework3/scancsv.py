from CSVPacket import Packet, CSVPackets
import sys

def stats():

    print "\n\nSTATS\n"
    print str(sys.argv[1]) + "\n\n"
    
    TCPports = [0 for i in range(1025)]
    UDPports = [0 for i in range(1025)]

    IPProtos = [0 for x in range(256)]
    numBytes = 0
    numPackets = 0

    csvfile = open(sys.argv[1],'r')

    for pkt in CSVPackets(csvfile):
        # pkt.__str__ is defined...
        #print pkt
        numBytes += pkt.length
        numPackets += 1
        proto = pkt.proto & 0xff
        IPProtos[proto] += 1

    print "numPackets:%u numBytes:%u" % (numPackets,numBytes)
    for i in range(256):
        if IPProtos[i] != 0:
            print "%3u: %9u" % (i, IPProtos[i])
    
    # Close and reopen file to reset buffer
    csvfile.close()
    csvfile = open(sys.argv[1], 'r')
    
    ## SHOW TCP/UDP packet counts for ports 1-1024
    for pkt in CSVPackets(csvfile):

        proto = pkt.proto & 0xff

        if proto == 6 and pkt.tcpdport <= 1024:
            TCPports[pkt.tcpdport] += 1
        if proto == 17 and pkt.udpdport <= 1024:
            UDPports[pkt.udpdport] += 1
    
    for idx,amt in enumerate(TCPports):
        if amt > 0:
            print "TCP packets going to port %d:\t%d" % (idx, amt)
    for idx,amt in enumerate(UDPports):
        if amt > 0:
            print "UDP packets going to port %d:\t%d" % (idx, amt)
    
def countip():
    
    print "\n\nCOUNTIP\n"
    print str(sys.argv[1]) + "\n\n"
    
    IPs = []
    IPProtos = [0 for x in range(256)]
    numBytes = 0
    numPackets = 0
    
    csvfile = open(sys.argv[1], 'r')
    
    for pkt in CSVPackets(csvfile):
        # pkt.__str__ is defined...
        #print pkt
        numBytes += pkt.length
        numPackets += 1
        proto = pkt.proto & 0xff
        IPProtos[proto] += 1

    print "numPackets:%u numBytes:%u" % (numPackets,numBytes)
    for i in range(256):
        if IPProtos[i] != 0:
            print "%3u: %9u" % (i, IPProtos[i])
    
    # Close and reopen file to reset buffer
    csvfile.close()
    csvfile = open(sys.argv[1], 'r')
    
    if len(sys.argv) < 4:
        for pkt in CSVPackets(csvfile):
            IPs.append(pkt.ipsrc)
            IPs.append(pkt.ipdst)
    elif len(sys.argv) == 4:
        if sys.argv[3] == '-GRE':
            print "---[ Searching for unique IP with GRE ..."
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 47:
                    IPs.append(pkt.ipsrc)
                    IPs.append(pkt.ipdst)
        elif sys.argv[3] == '-IPSEC':
            print "---[ Searching for unique IP with IPSEC ..."
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 50 or pkt.proto == 51:
                    IPs.append(pkt.ipsrc)
                    IPs.append(pkt.ipdst)
        elif sys.argv[3] == '-OSPF':
            print "---[ Searching for unique IP with OSPF ..."
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 89:
                    IPs.append(pkt.ipsrc)
                    IPs.append(pkt.ipdst)
        
    uniqueIPs = { x : IPs.count(x) for x in set(IPs) }
    sortedIPs = sorted(uniqueIPs.items(), key=lambda kv: kv[1], reverse=True)
    
    print "\n([IP address], [count])\n"
    for x in sortedIPs:
        print x
        
def connto():
    
    print "\n\nCONNTO\n"
    print str(sys.argv[1]) + "\n\n"
    
    destIPs = {}
    IPProtos = [0 for x in range(256)]
    numBytes = 0
    numPackets = 0
    
    csvfile = open(sys.argv[1], 'r')
    
    for pkt in CSVPackets(csvfile):
        # pkt.__str__ is defined...
        #print pkt
        numBytes += pkt.length
        numPackets += 1
        proto = pkt.proto & 0xff
        IPProtos[proto] += 1

    print "numPackets:%u numBytes:%u" % (numPackets,numBytes)
    for i in range(256):
        if IPProtos[i] != 0:
            print "%3u: %9u" % (i, IPProtos[i])
    
    # Close and reopen file to reset buffer
    csvfile.close()
    csvfile = open(sys.argv[1], 'r')
    for pkt in CSVPackets(csvfile):
        check = False
        if pkt.proto == 6:
            if pkt.tcpdport <= 1024:
                protoPort = "tcp/" + str(pkt.tcpdport)
                check = True
        elif pkt.proto == 17:
            if pkt.udpdport <= 1024:
                protoPort = "udp/" + str(pkt.udpdport)
                check = True
        
        if check == True:
            if pkt.ipdst in destIPs:
                destIPs[pkt.ipdst][0].add(pkt.ipsrc)
                destIPs[pkt.ipdst][1].add(protoPort)
            else:
                destIPs[pkt.ipdst] = [set([pkt.ipsrc]), set([protoPort])]
                
    i = 0
    for j,k in sorted(destIPs.items(), key=lambda (j, k): (len(k[0]), j), reverse=True):
        i += 1
        print "ipdst %s has %d distinct ipsrc on ports: %s" % (j,len(k[0]), ', '.join(k[1]))
        if i > 20:
            break
            
            
if __name__ == "__main__":

    if len(sys.argv) < 3:
        pass
    elif sys.argv[2] == '-stats':
        stats()
    elif sys.argv[2] == '-countip':
        countip()
    elif sys.argv[2] == '-connto':
        connto()
    

    
