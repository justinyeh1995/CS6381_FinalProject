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

class DetectionAppln ():
    def __init__(self, logger):
        self.zk_api = ZookeeperAPI(logger)
        self.detection_client = DetectionClient('192.168.2.209','50051')

    def configure (self):
        self.zk_api.configure()
        self.zk_api.start ()
        self.zk_api.dump ()

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
                    flag, ip = self.parse_data(data)
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
        response = self.detection_client.detect(ip)
        return response
    
    def set_quarantine_signal (self, node, ip):
        # Get the data from the znode
        data, stat = self.zk_api.zk.get (self.zk_api.mitigation_root_path + "/" + node)
        # Parse the data to get the source IP
        flag, ips = self.parse_data(data)
        # Add the new IP to the list
        ips.append(ip)
        # Update the znode
        path = self.zk_api.mitigation_root_path + "/" + node
        value = "1" + ":" + json.dumps(ips)
        self.zk_api.zk.set (path, value.encode('utf-8'))
    
    def event_loop (self):
        print ("Event loop started")
        while True:
            time.sleep(1)

    def __del__ (self):
        self.zk_api.shutdown()


if __name__ == "__main__":
    # set underlying default logging capabilities
    logging.basicConfig (level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger (__name__)
    detection_appln = MitigationAppln(logger)
    detection_appln.configure()
    detection_appln.detection_watch()
    detection_appln.event_loop() 


