import time
import json
import traceback
import subprocess
import logging
from ZookeeperAPI import ZookeeperAPI

class MitigationAppln ():
    def __init__ (self, logger):
        self.zk_api = ZookeeperAPI(logger)
        self.qurantined_hosts = set()

    def configure (self):
        self.zk_api.configure()
        self.zk_api.start ()
        self.zk_api.dump ()

    def init_znode (self, node):
        path = self.zk_api.mitigation_root_path + "/" + node
        if not self.zk_api.zk.exists(path):
            value = "0" + ":" + json.dumps([])
            self.zk_api.zk.create(path, value.encode('utf-8'), makepath=True, ephemeral=True)

    def quarantine_watch (self):
        for node in self.zk_api.nodes:
            # Initialize the znode
            self.init_znode(node)
            # Watch the node for any changes
            @self.zk_api.zk.DataWatch(self.zk_api.mitigation_root_path + "/" + node)
            def watch_node (data, stat, event):
                try:
                    print ("Watcher called")
                    print ("Watch Node: " + node)
                    print("Event Watcher: " + str(event))
                    print("Data Watcher: " + data.decode("utf-8"))
                    print("Stat Watcher: " + str(stat))
                    # Parse the data to get the source IP
                    flag, ips = self.parse_data(data)
                    for ip in ips:
                        if flag == "1" and ip not in self.qurantined_hosts:
                            self.quarantine(ip)
                        elif flag == "0" and ip in self.qurantined_hosts:
                            self.unquarantine(ip)
                        else:
                            pass
                except Exception as e:
                    traceback.print_exc()
                    raise e

    def parse_data (self, data):
        flag, history = data.decode("utf-8").split(":")
        ips = json.loads(history)
        return flag, ips

    def quarantine (self, ip):
        subprocess.call(["sudo", "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"])
        subprocess.call(["sudo", "iptables", "-I", "OUTPUT", "-d", ip, "-j", "DROP"])
        self.qurantined_hosts.add(ip)
        print ("IP Address " + ip + " is blocked")

    def unquarantine (self):
        for ip in self.qurantined_hosts:
            subprocess.call(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
            subprocess.call(["sudo", "iptables", "-D", "OUTPUT", "-d", ip, "-j", "DROP"])
    
    def event_loop (self):
        print ("Event loop started")
        while True:
            time.sleep(1)

    def __del__ (self):
        self.zk_api.shutdown()
        self.unquarantine()


if __name__ == "__main__":
    # set underlying default logging capabilities
    logging.basicConfig (level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger (__name__)
    mitigation_appln = MitigationAppln(logger)
    mitigation_appln.configure()
    mitigation_appln.quarantine_watch()
    mitigation_appln.event_loop() 

