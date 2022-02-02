
from Read_Filesize import ReadFile as rf

readFilesize=rf()
class Msg_Modelling():
    def __init__(self ):


        self.read_schema_msgs= readFilesize.read_schema_msgs()
        self.read_transactional_msgs=readFilesize.read_transactional_msgs()
        self.get_config_RDM_LP=readFilesize.get_config_RDM_LP()
        self.get_config_device_info=readFilesize.get_config_device_info()
        self.get_config_degree_srg=readFilesize.get_config_degree_srg()
        self.edit_config_RDM_Connection=readFilesize.edit_config_RDM_Connection()
        self.edit_config_service_creation=readFilesize.edit_config_service_creation()
        self.get_config_conn_monitoring=readFilesize.get_config_conn_monitoring()
        self.get_config_device_info_Xpdr=readFilesize.get_config_device_info_Xpdr()
        self.edit_config_xpdr_LPCreate=readFilesize.edit_config_xpdr_LPCreate()
        self.get_edit_create_service_xpdrs=readFilesize.get_edit_create_service_xpdrs()
        self.get_config_RDM_NonLP =readFilesize.get_config_RDM_NonLP()
        self.get_config_RDM_Info_Service=readFilesize.get_config_RDM_Info_Service()


    def model_get_schema(self, devices):
        # For every connection, there will be a get schema message requested to all connected devices.
        # Hence schema msgs = (rpc_msg + rpc_reply)xMxN where M = no. of devices and N = no. of Connections
        message_size, reply_size = self.read_schema_msgs
        print(message_size)
        print(reply_size)
        get_schema_msgs = (message_size + reply_size) * devices

        get_schema_msg_total = (get_schema_msgs) / (1024*1024)  # get schema traffic in MB
        return get_schema_msg_total

    def model_edit_config_rdm(self, devices):
        # For every connection, there will be device data requested. However it is different for devices in the light path and not in the light path.
        # M(total) = [{M(LockRPC)}*(candidate + running) + M(devicedataRPC) + M(CommitRPC) + {M(UnlockRPC)}*(candidate + running)]*D
        # where D = no. of devices and M(devicedataRPC) can be a get-config r edit-config message
        # Each RPC above consists of an RPC get/edit-config message and a corresponding reply
        # For example, M(LOCKRPC)= rpc_msg +rpc_reply
        # We consider {M(LockRPC) + M(Lock Reply)}*(candidate + running), M(CommitRPC) + M(CommitReply) + {M(UnlockRPC) + M(Unock Reply)}*(candidate + running) as a bundle of transactional messages
        # These transactional messages bundle will be queried for every get and edit-config messages
        # For connection creation internally n the roadm, for every ROADM in the LP,
        # get_config = (transactional bundle + rpc + rpc_reply)* no.of get_config_requests
        # edit_config = (transactional bundle + rpc + rpc_reply)* no.of edit_config_requests
        # total_connection_creation_msgs= get_config + edit_config (for 1 device)

        edit_config_rpc = self.edit_config_RDM_Connection

        return (edit_config_rpc*devices) / (1024*1024)

    def model_connection_nodes_nonLP(self, devices):
        get_config_rpc=self.get_config_RDM_NonLP *devices
        return get_config_rpc/(1024*1024)
    def service_create_rdms(self, devices):
        get_config_servie = self.get_config_RDM_Info_Service
        edit_config_service = self.edit_config_service_creation
        service_create_msgs = (get_config_servie + edit_config_service) * devices
        return service_create_msgs / (1024*1024)

    def connection_validate(self, devices):
        conn_validate_rdm = (self.get_config_conn_monitoring) * devices
        return conn_validate_rdm / (1024*1024)
    def get_xpdrs_info(self,xpdrs):
        get_config_rpc=self.get_config_device_info_Xpdr * xpdrs
        return get_config_rpc / (1024*1024)

    def connect_xdrs(self, xpdrs):
        edit_config_rpc = self.edit_config_xpdr_LPCreate * xpdrs
        return edit_config_rpc / (1024*1024)

    def service_create_xpdrs(self, xpdrs):
        edit_service_rpc = self.get_edit_create_service_xpdrs * xpdrs

        return edit_service_rpc / (1024*1024)

    def model_roadmdegree_traffic(self,degree):
        get_rdm_deg_rpc = self.get_config_degree_srg * degree
        return get_rdm_deg_rpc

    def model_roadm_traffic(self, degree):
        get_rdm_rpc = self.get_config_device_info + self.model_roadmdegree_traffic(degree)
        return (get_rdm_rpc)/(1024*1024)

    def model_roadm_device_info(self, devices):
        get_device_data= self.get_config_device_info * devices
        return (get_device_data)/(1024*1024)





