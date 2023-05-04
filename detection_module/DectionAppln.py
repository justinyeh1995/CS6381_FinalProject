import time
import json
import traceback
import subprocess
import logging

from ZookeeperAPI import ZookeeperAPI

import grpc
import detection_pb2
import detection_pb2_grpc
from detection_client import DetectionClient

from scapy.all import *
import argparse # for argument parsing
import configparser # for configuration parsing

import paramiko

class DetectionAppln ():
    def __init__(self, logger):
        self.node = None
        self.zk_api = ZookeeperAPI(logger)
        self.detection_client = DetectionClient('192.168.2.209','50051')
        self.ssh_client = None
        self.sftp = None

    def configure (self, args):
        self.zk_api.configure()
        self.zk_api.start ()
        self.zk_api.dump ()
        self.node = args.node
        # Get SSH client
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect('192.168.2.209', username='cc', key_filename='/home/cc/.ssh/id_rsa')
        self.sftp = self.ssh_client.open_sftp()

    def init_znode (self, node):
        path = self.zk_api.detection_root_path + "/" + node
        if not self.zk_api.zk.exists(path):
            value = "0" + ":" + json.dumps([])
            self.zk_api.zk.create(path, value.encode('utf-8'), makepath=True, ephemeral=True)

    def detection_watch (self):
        for node in self.zk_api.nodes:
            # Initialize the znode
            self.init_znode(node)
            # Watch the node for any changes
            @self.zk_api.zk.DataWatch(self.zk_api.detection_root_path + "/" + node)
            def watch_node (data, stat, event):
                try:
                    print ("Watcher called")
                    print ("Watch Node: " + node)
                    print ("Event Watcher: " + str(event))
                    print ("Data Watcher: " + data.decode("utf-8"))
                    print ("Stat Watcher: " + str(stat))
                    # Parse the data to get the source IP
                    flag, ips = self.parse_data(data)
                    # Call the detection service
                    for ip in ips:
                        if self.detect(ip):
                            self.set_quarantine_signal(node, ip)
                except Exception as e:
                    traceback.print_exc()
                    raise e

    def parse_data (self, data):
        flag, history = data.decode("utf-8").split(":")
        ips = json.loads(history)
        return flag, ips

    def detect (self, ip): 
        # Call the detection service
        response = self.detection_client.run(ip)
        return response
    
    def set_quarantine_signal (self, node, ip):
        # Get the data from the znode
        data, stat = self.zk_api.zk.get (self.zk_api.mitigation_root_path + "/" + node)
        # Parse the data to get the source IP
        flag, ips = self.parse_data(data)
        # Add the new IP to the list
        ips.append(ip)
        ips = list(set(ips))
        # Update the znode
        path = self.zk_api.mitigation_root_path + "/" + node
        value = "1" + ":" + json.dumps(ips)
        self.zk_api.zk.set (path, value.encode('utf-8'))

    def write_to_db (self, ip):
        # Read the data from the file
        with self.sftp.open('/home/cc/Team10/CS6381_FinalProject/services/blocklist_db.json', 'r') as f:
            # Parse the JSON data
            data = json.load(f)
            latest_id = data[-1]['id']
            # Modify the parsed data to add a new record
            new_record = {'id': latest_id+1, 'ip': ip}
            data.append(new_record)
        # Write the modified data back to the file
        with self.sftp.open('/home/cc/Team10/CS6381_FinalProject/services/blocklist_db.json', 'w') as f:
            json.dump(data, f, indent=4)

        self.sftp.close()
        self.ssh_client.close()
    
    
    def event_loop (self):
        print ("Event loop started")
        print ("Waiting for an Attack") 
        def packet_callback(packet):
            if packet.haslayer(IP):
                # white list master node
                if packet[IP].src == "192.168.2.209":
                    return
                if self.detect(packet[IP].src):
                    print("Attack from C&C server")
                    print ((packet[IP].src, packet[IP].dst))
                    self.set_quarantine_signal(self.node, packet[IP].src)
                    # to-do: send the IP of this machine to the db server
                    self.write_to_db(packet[IP].dst) 
                #else:
                #    print("Normal traffic from " + packet[IP].src)

        sniff(prn=packet_callback, filter="tcp", iface="ens3")

    def __del__ (self):
        self.zk_api.shutdown()
        self.ssh_client.close()



def parseCmdLineArgs ():
    # instantiate a ArgumentParser object
    parser = argparse.ArgumentParser (description="Publisher Application")
    
    # Now specify all the optional arguments we support
    # At a minimum, you will need a way to specify the IP and port of the lookup
    # service, the role we are playing, what dissemination approach are we
    # using, what is our endpoint (i.e., port where we are going to bind at the
    # ZMQ level)
    
    parser.add_argument ("-n", "--node", default="host1", help="Some host name, host1/host2/host3")
    return parser.parse_args()


if __name__ == "__main__":
    # set underlying default logging capabilities
    logging.basicConfig (level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger (__name__)
    args = parseCmdLineArgs ()
    detection_appln = DetectionAppln(logger)
    detection_appln.configure(args)
    #detection_appln.detection_watch()
    detection_appln.event_loop() 


