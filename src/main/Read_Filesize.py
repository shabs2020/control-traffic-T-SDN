import os

Roadms = ['ROADM-A1', 'ROADM-B1', 'ROADM-C1']
Xpdrs = ['XPDR-C1', 'XPDR-B1', 'XPDR-A1']
Devices = ['ROADM-A1', 'ROADM-B1', 'ROADM-C1', 'XPDR-C1', 'XPDR-B1', 'XPDR-A1']


class ReadFile():
    def __init__(self):
        self.Roadms = Roadms
        self.Xpdrs = Xpdrs
        self.Devices = Devices
        self.total_avg_transactional_bundle = self.read_transactional_msgs()

    def read_schema_msgs(self):
        devices = self.Devices
        rpc_msg = 0.0
        rpc_reply = 0.0
        for d in devices:
            rpc_msg = os.path.getsize(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-0') + rpc_msg
            rpc_reply = os.path.getsize(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-0') + rpc_reply
            print("{} schema get size in  {}".format(d, rpc_msg))
            print("{} schema reply get size in  {}".format(d, rpc_reply))
        print('Avd msg size is {}'.format(rpc_reply / len(devices)))
        return rpc_msg / len(devices), rpc_reply / len(devices)

    def read_transactional_msgs(self):
        devices = self.Devices
        lock_candidate, lock_running, commit_rpc, unlock_candidate, unlock_running = 0.0, 0.0, 0.0, 0.0, 0.0
        lock_candidate_reply, lock_running_reply, commit_rpc_reply, unlock_candidate_reply, unlock_running_reply = 0.0, 0.0, 0.0, 0.0, 0.0
        for d in devices:
            lock_candidate = os.path.getsize(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-0_1') + lock_candidate
            lock_candidate_reply = os.path.getsize(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-0_1') + lock_candidate_reply
            if d == 'ROADM-B1':
                lock_running = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-1_1') + lock_running
                commit_rpc = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-3_1') + commit_rpc
                unlock_candidate = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-4_1') + unlock_candidate
                unlock_running = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-5_1') + unlock_running
                lock_running_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-1_1') + lock_running_reply
                commit_rpc_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-3_1') + commit_rpc_reply
                unlock_candidate_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-4_1') + unlock_candidate_reply
                unlock_running_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-5_1') + unlock_running_reply
            else:
                lock_running = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-1') + lock_running
                commit_rpc = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-3') + commit_rpc
                unlock_candidate = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-4') + unlock_candidate
                unlock_running = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-5') + unlock_running

                lock_running_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-1') + lock_running_reply
                commit_rpc_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-3') + commit_rpc_reply
                unlock_candidate_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-4') + unlock_candidate_reply
                unlock_running_reply = os.path.getsize(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-5') + unlock_running_reply
        total_avg_transactional_messages = (
                                                   lock_candidate + lock_running + commit_rpc + unlock_candidate + unlock_running) / len(
            devices)
        total_avg_transactional_reply = (
                                                lock_running_reply + lock_running_reply + commit_rpc_reply + unlock_candidate_reply + unlock_running_reply) / len(
            devices)
        total_avg_transactional_bundle = total_avg_transactional_messages +total_avg_transactional_reply
        return total_avg_transactional_bundle, total_avg_transactional_messages, total_avg_transactional_reply

    def get_config_RDM_LP(self):
        devices = ['ROADM-A1', 'ROADM-C1']

        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA = self.read_message_file_size(d, 2, 123)
            else:
                rpc_RDMC = self.read_message_file_size(d, 2, 117)
        total_get_config_rpc = (rpc_RDMA[0] + rpc_RDMC[0])/ len(devices)
        gc_request=(rpc_RDMA[1] + rpc_RDMC[1])/ len(devices)
        gc_reply=(rpc_RDMA[2] + rpc_RDMC[2])/ len(devices)

        print("total get config message{} ".format(total_get_config_rpc,))
        return total_get_config_rpc, gc_request, gc_reply
    def get_config_device_info(self):
        # Get device data initially
        get_dev_data_rpc= 0
        get_dev_data_reply= 0

        for r in self.Roadms:
            if r == 'ROADM-B1':
                get_dev_data_rpc = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + r + '/rpc-message-m-2_1').st_size + get_dev_data_rpc
                get_dev_data_reply = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + r + '/rpc-reply-m-2_1').st_size+get_dev_data_reply
                # print("Device data fro RoadmB1- {}, {}".format(get_dev_data_rpc, get_dev_data_reply))
            else:
                get_dev_data_rpc = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + r + '/rpc-message-m-2').st_size + get_dev_data_rpc
                get_dev_data_reply = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + r + '/rpc-reply-m-2').st_size + get_dev_data_reply



        transactional_bundle = self.read_transactional_msgs() * len(self.Roadms)
        total_dev_info= (get_dev_data_rpc + get_dev_data_reply + transactional_bundle[0])/len(self.Roadms)
        dev_info_rpc=(get_dev_data_rpc+transactional_bundle[1])/len(self.Roadms)
        dev_info_reply=(get_dev_data_reply+ transactional_bundle[2])/len(self.Roadms)

        return total_dev_info, dev_info_rpc, dev_info_reply


    def get_config_degree_srg(self):
        # here each roadmA and C has two degrees. Hence we find the avg load per degree and srg of a device
        # considering no. of deg= no. of srg.
        devices = ['ROADM-A1', 'ROADM-C1']

        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA = self.read_message_file_size(d, 8, 123)
            else:
                rpc_RDMC = self.read_message_file_size(d, 2, 117)
        total_get_degree= (rpc_RDMA[0] + rpc_RDMC[0])/2
        deg_rpc=(rpc_RDMA[1] + rpc_RDMC[1])/2
        deg_reply=(rpc_RDMA[2] + rpc_RDMC[2])/2
        return total_get_degree, deg_rpc, deg_reply


    # def get_config_degree_only(self):
    #     # here each roadmA and C has two degrees. Hence we find the avg load per degree of a device
    #     # considering no. of deg= no. of srg.
    #     devices = ['ROADM-A1', 'ROADM-C1']
    #
    #     for d in devices:
    #         if d == 'ROADM-A1':
    #             rpc_RDMA = self.read_message_file_size(d, 8, 123)/2
    #         else:
    #             rpc_RDMC = self.read_message_file_size(d, 2, 117)/2
    #     return (rpc_RDMA + rpc_RDMC)/2



    def get_config_RDM_NonLP(self):
        # Get device data initially
        get_dev_data_rpc = os.path.getsize(
            '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/ROADM-B1/rpc-message-m-2_1')
        get_dev_data_reply = os.path.getsize(
            '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/ROADM-B1/rpc-reply-m-2_1')
        print("Device data fro RoadmB1- {}, {}".format(get_dev_data_rpc, get_dev_data_reply))
        transactional_bundle= self.read_transactional_msgs()
        total_gc_nonLP= get_dev_data_rpc+ get_dev_data_reply+ transactional_bundle[0]
        dev_info_rpc= get_dev_data_rpc+ transactional_bundle[1]
        dev_info_reply= get_dev_data_reply + transactional_bundle[2]
        return total_gc_nonLP, dev_info_rpc, dev_info_reply


    def edit_config_RDM_Connection(self):
        #Create logical points internally and connect them
        devices = ['ROADM-A1', 'ROADM-C1']
        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA= self.read_message_file_size(d, 137, 180)
            else:
                rpc_RDMC= self.read_message_file_size(d, 131, 178)

        total_edit_config_rpc = (rpc_RDMA[0] + rpc_RDMC[0])/ len(devices)
        edit_config_rpc=(rpc_RDMA[1] + rpc_RDMC[1])/ len(devices)
        edit_config_reply=(rpc_RDMA[2] + rpc_RDMC[2])/ len(devices)

        # print("total edit messages {},".format(edit_config_rpc / len(devices)))
        return total_edit_config_rpc, edit_config_rpc, edit_config_reply

    def get_config_RDM_Info_Service(self):
        # get info about created logical connction
        devices = ['ROADM-A1', 'ROADM-C1']
        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA = self.read_message_file_size(d, 185, 198)
            else:
                rpc_RDMC = self.read_message_file_size(d, 179, 192)
        total_get_service_info = (rpc_RDMA[0] + rpc_RDMC[0])/len(devices)
        get_service_rpc=(rpc_RDMA[1] + rpc_RDMC[1])/len(devices)
        get_service_reply=(rpc_RDMA[2] + rpc_RDMC[2])/len(devices)

        return total_get_service_info, get_service_rpc, get_service_reply

    def edit_config_service_creation(self):
        # give power configs to the connection created
        devices = ['ROADM-A1', 'ROADM-C1']
        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA = self.read_message_file_size(d, 203, 228)
            else:
                rpc_RDMC = self.read_message_file_size(d, 197, 222)
        total_edit_service_info =(rpc_RDMA[0] + rpc_RDMC[0])/len(devices)
        edit_service_rpc=(rpc_RDMA[1] + rpc_RDMC[1])/len(devices)
        edit_service_reply=(rpc_RDMA[2] + rpc_RDMC[2])/len(devices)
        return total_edit_service_info, edit_service_rpc, edit_service_reply


    def get_config_conn_monitoring(self):
        #validate the created connection
        devices = ['ROADM-A1', 'ROADM-C1']
        rpc_msg, rpc_reply = 0.0, 0.0
        total_avg_transactional_bundle=self.total_avg_transactional_bundle
        for d in devices:
            if d == 'ROADM-A1':
                i,j=231,235
            else:
                i,j=225, 229
            for k in range(i,j):
                rpc_msg = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-message-m-' + str(
                        k)).st_size + rpc_msg
                rpc_reply = os.stat(
                    '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + d + '/rpc-reply-m-' + str(
                        k)).st_size + rpc_reply
        total_avg_conn_monitor=(rpc_msg +rpc_reply + total_avg_transactional_bundle[0])/len(devices)
        conn_monitor_rpc=(rpc_msg+total_avg_transactional_bundle[1])/len(devices)
        conn_monitor_reply=(rpc_reply+total_avg_transactional_bundle[2])/len(devices)
        return total_avg_conn_monitor,conn_monitor_rpc, conn_monitor_reply

    def get_config_device_info_Xpdr(self):
        #get XPDR data initially
        devices=  self.Xpdrs
        total_rpc=0.0
        rpc_msg =0.0
        rpc_reply=0.0
        for d in devices:
            read_msg_size=self.read_message_file_size(d,2,9)
            total_rpc=(read_msg_size[0]+ total_rpc)/len(devices)
            rpc_msg =  (read_msg_size[1]+ rpc_msg)/len(devices)
            rpc_reply=(read_msg_size[2]+ rpc_reply)/len(devices)
        return total_rpc,rpc_msg, rpc_reply

    def edit_config_xpdr_LPCreate(self):
        #create connection
        devices =  ['XPDR-C1', 'XPDR-A1']
        for d in devices:
            if d == 'XPDR-A1':
                rpc_XPDRA = self.read_message_file_size(d, 23, 54)
            else:
                rpc_XPDRC = self.read_message_file_size(d, 23, 48)
        total_edit_conn_info = (rpc_XPDRA[0] + rpc_XPDRC[0])/len(devices)
        edit_conn_rpc=(rpc_XPDRA[1] + rpc_XPDRC[1])/len(devices)
        edit_conn_reply=(rpc_XPDRA[2] + rpc_XPDRC[2])/len(devices)
        return total_edit_conn_info,  edit_conn_rpc, edit_conn_reply

    def get_edit_create_service_xpdrs(self):
        #get and edit power config to created connection
        devices =  ['XPDR-C1', 'XPDR-A1']
        for d in devices:
            if d == 'XPDR-A1':
                rpc_XPDRA = self.read_message_file_size(d, 59, 90)
            else:
                rpc_XPDRC = self.read_message_file_size(d, 53, 78)
        total_edit_service_info = (rpc_XPDRA[0] + rpc_XPDRC[0])/len(devices)
        edit_service_rpc=(rpc_XPDRA[1] + rpc_XPDRC[1])/len(devices)
        edit_service_reply=(rpc_XPDRA[2] + rpc_XPDRC[2])/len(devices)
        return total_edit_service_info, edit_service_rpc, edit_service_reply

    # NETCONF traffic related to connection termination
    def lp_terminate_rdm(self):
        devices = ['ROADM-A1', 'ROADM-C1']
        for d in devices:
            if d == 'ROADM-A1':
                rpc_RDMA = self.read_message_file_size_II(d, 230, 411)
            else:
                rpc_RDMC = self.read_message_file_size_II(d, 231, 412)
        total_terminate_service=(rpc_RDMA[0]+ rpc_RDMC[0])/len(devices)
        service_terminate_rpc=(rpc_RDMA[1]+ rpc_RDMC[1])/len(devices)
        service_terminate_reply=(rpc_RDMA[2]+ rpc_RDMC[2])/len(devices)
        return  total_terminate_service, service_terminate_rpc, service_terminate_reply

    def lp_terminate_xpdr(self):
        devices = ['XPDR-C1', 'XPDR-A1']
        for d in devices:
            if d == 'XPDR-A1':
                rpc_XPDRA = self.read_message_file_size_II(d, 88, 203)
            else:
                rpc_XPDRC = self.read_message_file_size_II(d, 76, 179)
        total_terminate_service=(rpc_XPDRA[0]+ rpc_XPDRC[0])/len(devices)
        service_terminate_rpc=(rpc_XPDRA[1]+ rpc_XPDRC[1])/len(devices)
        service_terminate_reply=(rpc_XPDRA[2]+ rpc_XPDRC[2])/len(devices)
        return  total_terminate_service, service_terminate_rpc, service_terminate_reply

    def read_message_file_size(self, device, start, end):

        rpc_msg, rpc_reply = 0.0, 0.0
        total_avg_transactional_bundle=self.total_avg_transactional_bundle
        for i in range(start, end, 6):
            rpc_msg = os.stat(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + device + '/rpc-message-m-' + str(
                    i)).st_size + rpc_msg + total_avg_transactional_bundle[1]
            rpc_reply = os.stat(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessagesSuccess-OhneLLDPMitXPDRB/' + device + '/rpc-reply-m-' + str(
                    i)).st_size + rpc_reply + total_avg_transactional_bundle[2]
        total_rpc = rpc_msg + rpc_reply
        return (total_rpc,rpc_msg,rpc_reply)

    def read_message_file_size_II(self, device, start, end):

        rpc_msg, rpc_reply = 0.0, 0.0
        total_avg_transactional_bundle = self.total_avg_transactional_bundle
        for i in range(start, end, 6):
            rpc_msg = os.stat(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessages-ServiceDeletion/' + device + '/rpc-message-m-' + str(
                    i)).st_size + rpc_msg + total_avg_transactional_bundle[1]
            rpc_reply = os.stat(
                '/home/shabnam/PycharmProjects/TransportPCEScripts/NetconfMessages-ServiceDeletion/' + device + '/rpc-reply-m-' + str(
                    i)).st_size + rpc_reply + total_avg_transactional_bundle[2]
        total_rpc = rpc_msg + rpc_reply
        return (total_rpc, rpc_msg, rpc_reply)



# rf = ReadFile()
# rf.read_schema_msgs()
# rf.get_config_RDM_LP()
# rf.read_transactional_msgs()
# rf.get_config_RDM_NonLP()
# rf.edit_config_RDM_Connection()
