from Read_Filesize import ReadFile as rf

readFilesize = rf()


class Msg_Modelling():
    def __init__(self):
        self.read_schema_msgs = readFilesize.read_schema_msgs()
        self.read_transactional_msgs = readFilesize.read_transactional_msgs()
        self.get_config_RDM_LP = readFilesize.get_config_RDM_LP()
        self.get_config_device_info = readFilesize.get_config_device_info()
        self.get_config_degree_srg = readFilesize.get_config_degree_srg()
        self.edit_config_RDM_Connection = readFilesize.edit_config_RDM_Connection()
        self.edit_config_service_creation = readFilesize.edit_config_service_creation()
        self.get_config_conn_monitoring = readFilesize.get_config_conn_monitoring()
        self.get_config_device_info_Xpdr = readFilesize.get_config_device_info_Xpdr()
        self.edit_config_xpdr_LPCreate = readFilesize.edit_config_xpdr_LPCreate()
        self.get_edit_create_service_xpdrs = readFilesize.get_edit_create_service_xpdrs()
        self.get_config_RDM_NonLP = readFilesize.get_config_RDM_NonLP()
        self.get_config_RDM_Info_Service = readFilesize.get_config_RDM_Info_Service()
        self.lp_terminate_rdm=readFilesize.lp_terminate_rdm()
        self.lp_terminate_xpdr=readFilesize.lp_terminate_xpdr()

    def model_get_schema(self, devices):
        # For every connection, there will be a get schema message requested to all connected devices.
        # Hence schema msgs = (rpc_msg + rpc_reply)xMxN where M = no. of devices and N = no. of Connections
        message_size, reply_size = self.read_schema_msgs
        print(message_size)
        print(reply_size)
        get_schema_msgs = (message_size + reply_size) * devices

        get_schema_msg_total = (get_schema_msgs) / (1024 * 1024)  # get schema traffic in MB
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

        total_edit_config = (self.edit_config_RDM_Connection[0] * devices) / (1024 * 1024)
        edit_config_rpc = (self.edit_config_RDM_Connection[1] * devices) / (1024 * 1024)
        edit_config_reply = (self.edit_config_RDM_Connection[2] * devices) / (1024 * 1024)

        return total_edit_config, edit_config_rpc, edit_config_reply

    def model_connection_nodes_nonLP(self, devices):
        total_get_config_rpc = (self.get_config_RDM_NonLP[0] * devices) / (1024 * 1024)
        get_config_rpc = (self.get_config_RDM_NonLP[1] * devices) / (1024 * 1024)
        get_config_reply = (self.get_config_RDM_NonLP[2] * devices) / (1024 * 1024)
        return total_get_config_rpc, get_config_rpc, get_config_reply

    def service_create_rdms(self, devices):
        get_config_service = self.get_config_RDM_Info_Service
        edit_config_service = self.edit_config_service_creation
        total_service_create_msgs = ((get_config_service[0] + edit_config_service[0]) * devices)/ (1024 * 1024)
        service_create_rpc=((get_config_service[1] + edit_config_service[1]) * devices)/ (1024 * 1024)
        service_create_reply=((get_config_service[2] + edit_config_service[2]) * devices)/ (1024 * 1024)
        return total_service_create_msgs, service_create_rpc, service_create_reply

    def connection_validate(self, devices):
        total_conn_validate_rdm = (self.get_config_conn_monitoring[0] * devices)/ (1024 * 1024)
        conn_validate_rpc=(self.get_config_conn_monitoring[1] * devices)/ (1024 * 1024)
        conn_validate_reply=(self.get_config_conn_monitoring[2] * devices)/ (1024 * 1024)

        return total_conn_validate_rdm, conn_validate_rpc,conn_validate_reply

    def get_xpdrs_info(self, xpdrs):
        total_get_config_rpc = (self.get_config_device_info_Xpdr[0] * xpdrs)/ (1024 * 1024)
        get_config_rpc=(self.get_config_device_info_Xpdr[1] * xpdrs)/ (1024 * 1024)
        get_config_reply=(self.get_config_device_info_Xpdr[2] * xpdrs)/ (1024 * 1024)
        return total_get_config_rpc, get_config_rpc, get_config_reply

    def connect_xdrs(self, xpdrs):
        total_edit_config_rpc = (self.edit_config_xpdr_LPCreate[0] * xpdrs)/ (1024 * 1024)
        edit_config_rpc= (self.edit_config_xpdr_LPCreate[1] * xpdrs)/ (1024 * 1024)
        edit_config_reply=  (self.edit_config_xpdr_LPCreate[2] * xpdrs)/ (1024 * 1024)
        return total_edit_config_rpc, edit_config_rpc, edit_config_reply

    def service_create_xpdrs(self, xpdrs):
        total_edit_service_rpc = (self.get_edit_create_service_xpdrs[0] * xpdrs)/ (1024 * 1024)
        edit_service_rpc=(self.get_edit_create_service_xpdrs[1] * xpdrs)/ (1024 * 1024)
        edit_service_reply=(self.get_edit_create_service_xpdrs[2] * xpdrs)/ (1024 * 1024)

        return total_edit_service_rpc, edit_service_rpc, edit_service_reply

    def model_roadmdegree_traffic(self, degree):
        total_get_rdm_deg_rpc = self.get_config_degree_srg[0] * degree
        get_rdm_deg_rpc=self.get_config_degree_srg[1] * degree
        get_rdm_deg_reply=self.get_config_degree_srg[0] * degree
        return total_get_rdm_deg_rpc, get_rdm_deg_rpc, get_rdm_deg_reply

    def model_roadm_traffic(self, degree):
        model_roadmdegree_traffic=self.model_roadmdegree_traffic(degree)
        total_get_rdm_rpc = (self.get_config_device_info[0] + model_roadmdegree_traffic[0]) / (1024 * 1024)
        get_rdm_rpc= (self.get_config_device_info[1] + model_roadmdegree_traffic[1]) / (1024 * 1024)
        get_rdm_reply= (self.get_config_device_info[2] + model_roadmdegree_traffic[2]) / (1024 * 1024)
        return total_get_rdm_rpc, get_rdm_rpc, get_rdm_reply

    def model_roadm_device_info(self, devices):
        total_get_device_data = (self.get_config_device_info[0] * devices)/ (1024 * 1024)
        get_device_rpc=(self.get_config_device_info[1] * devices)/ (1024 * 1024)
        get_device_reply=(self.get_config_device_info[2] * devices)/ (1024 * 1024)
        return total_get_device_data, get_device_rpc, get_device_reply

    def model_lp_termination_rdm(self, devices):
        total_termination_data=(self.lp_terminate_rdm[0]*devices)/(1024 * 1024)
        termination_rpc=(self.lp_terminate_rdm[1]*devices)/(1024 * 1024)
        termination_reply=((self.lp_terminate_rdm[2]*devices)/(1024 * 1024))
        return  total_termination_data, termination_rpc, termination_reply

    def model_lp_termination_xpdr(self, devices):
        total_termination_data=(self.lp_terminate_xpdr[0]*devices)/(1024 * 1024)
        termination_rpc=(self.lp_terminate_xpdr[1]*devices)/(1024 * 1024)
        termination_reply=((self.lp_terminate_xpdr[2]*devices)/(1024 * 1024))
        return  total_termination_data, termination_rpc, termination_reply
