import traceback 
import logging
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

class ZookeeperAPI():

    #################################################################
    # constructor
    #################################################################
    def __init__ (self, logger):
        """constructor"""
        self.logger = logger
        self.zkIPAddr = "192.168.2.209"  # ZK server IP address
        self.zkPort = 2181 # ZK server port num
        self.zk = None  # session handle to the server
        #---------------------------------------------------
        self.detection_root_path = "/detection"
        self.mitigation_root_path = "/mitigation"
        #---------------------------------------------------
        self.nodes = ["host1", "host2", "host3"]


    # Debugging: Dump the contents
    def dump (self):
        """dump contents"""
        self.logger.debug  ("=================================")
        self.logger.debug (("Server IP: {}, Port: {}; Path = {}".format (self.zkIPAddr, self.zkPort, self.detection_root_path)))
        self.logger.debug  ("=================================")


    # Initialize the driver
    def configure (self):
        """Initialize the client driver program"""
        try:
            # debug output
            self.dump ()

            # instantiate a zookeeper client object
            # right now only one host; it could be the ensemble
            hosts = self.zkIPAddr + ":" + str (self.zkPort)
            self.logger.debug (("ZookeeperAPI::configure -- instantiate zk obj: hosts = {}".format(hosts)))
            self.zk = KazooClient (hosts)
            self.logger.debug (("ZookeeperAPI::configure -- state = {}".format (self.zk.state)))
            
        except Exception as e:
            self.logger.debug ("ZookeeperAPI::configure -- Exception: {}".format (e))
            traceback.print_exc()
            raise
            

    def start (self):
        """Start the client driver program"""
        try:
            # first connect to the zookeeper server
            self.logger.debug  ("ZookeeperAPI::start -- connect with server")
            self.zk.start ()
            self.logger.debug ("ZookeeperAPI::start -- state = {}".format (self.zk.state))

        except Exception as e:
            self.logger.debug ("ZookeeperAPI::start -- Exception: {}".format (e))
            traceback.print_exc()
            raise


    def register_node (self, path, value):
        """Configure the client driver program"""
        try:
            # next, create a znode for the discovery service with initial value of its address
            self.logger.debug  ("ZookeeperAPI::run_driver -- create a znode for discovery service")
            #-------------------------------------------
            if not self.zk.exists (path):
                self.logger.debug (("ZookeeperAPI::configure -- create znode: {}".format (path)))
                self.zk.create (path, value=value.encode('utf-8'), ephemeral=True, makepath=True)
            else:
                self.logger.debug (("ZookeeperAPI::configure -- znode already exists: {}".format (path)))
                self.zk.set (path, value=value.encode('utf-8'))
        
        except Exception as e:
            self.logger.debug ("ZookeeperAPI::configure -- Exception: {}".format (e))
            traceback.print_exc()
            raise

  
    def shutdown (self):    
        """Shutdown the zookeeper adapter"""
        try:
            self.logger.debug  ("ZookeeperAPI::shutdown -- disconnect and close")
            self.zk.stop ()
            self.zk.close ()

            self.logger.debug  ("ZookeeperAPI::shutdown -- Bye Bye")

        except Exception as e: 
            traceback.print_exc()
            raise e

###################################
#
# Main entry point
#
###################################
if __name__ == "__main__":
    try:
        # set underlying default logging capabilities
        logging.basicConfig (level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger = logging.getLogger (__name__)
        zk = ZookeeperAPI (logger)
        zk.configure ()
        zk.start ()
    except Exception as e:
        traceback.print_exc()
        raise e
