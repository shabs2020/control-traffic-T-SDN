from matplotlib.ticker import FixedFormatter, FixedLocator

import RMSA as rs
import CTModelling
import math
import numpy as np
import matplotlib.pyplot as plot



def plot_create_hist(netconf_traffic_hist, yscale, annotation, imagename):
    # calculate bins for histogram https://datatofish.com/plot-histogram-python/
    # n = number of observations = 100
    # Range = maximum value – minimum value = 91 – 1 = 90
    # # of intervals =  √n = √100 = 10
    # Width of intervals = Range / (  # of intervals) = 90/10 = 9
    no_of_obs = len(netconf_traffic_hist)

    hist_range = max(netconf_traffic_hist) - min(netconf_traffic_hist)
    # print(max(netconf_traffic_hist))
    # print(min(netconf_traffic_hist))
    intervals = math.sqrt(no_of_obs)

    interval_width = math.ceil(hist_range / (intervals))
    # print(interval_width)
    bins = []
    for i in range(0, no_of_obs + 1, int(intervals)):
        bins.append(i)
    # print(bins)
    conn = np.arange(121)
    # print(conn)
    plot.bar(conn, netconf_traffic_hist)
    plot.xlim([-1, 121])
    plot.ylim(yscale)
    # axes = plot.gca()
    # y_min, y_max = axes.get_ylim()
    y_min, y_max = round(min(netconf_traffic_hist), 1), round(max(netconf_traffic_hist), 1)
    # plot.xticks(conn)
    # plot.yticks(netconf_traffic_hist)  # This may be included or excluded as per need
    plot.xlabel('Lightpaths')
    plot.ylabel('Netconf Traffic[MB]')
    s = 'max_traffic = ' + str(y_max) + '\n' + \
        'min_traffic = ' + str(y_min)

    plot.annotate(s, annotation)
    # plot.hist(netconf_traffic_hist, density=True, bins=bins)
    # #plot.axis([1, 121, 0, 5])
    # #axis([xmin,xmax,ymin,ymax])
    # plot.xlabel('Connections')
    # plot.ylabel('Netconf Traffic[MB]')
    # plot.show()
    plot.savefig(imagename + ".png")
    plot.clf()


def plot_create_hist1(netconf_traffic, y_label, yscale1, yscale2, imagename, annotation):
    x1 = []
    x2 = []
    for t in range(0, 50):
        x1.append(netconf_traffic[t][0])
        x2.append(round(netconf_traffic[t][1], 2))

        # x1.append(t[0])
        # x2.append(round(t[1], 3))
    print('x1 {}'.format(x1))
    print('x2 {}'.format(x2))
    conn = np.arange(start=1, stop=51)
    print(conn)
    print(max(x1))
    fig, ax1 = plot.subplots(figsize=(12, 5.3))
    # figsize=(40, 30)
    color = 'tab:blue'
    ax1.set_xlabel('Lightpath ID', fontsize=20)
    ax1.set_ylabel('Netconf traffic volume [MB]', color=color, fontsize=18)
    ax1.bar(conn, x2, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:orange'
    ax2.set_ylabel(y_label, color=color, fontsize=18)  # we already handled the x-label with ax1
    ax2.plot(conn, x1, 's', color=color, linewidth=0.75)

    ax2.tick_params(axis='y', labelcolor=color)

    #  ax1.set_xlim(0, 51)
    ax1.set_ylim(yscale1)
    ax2.set_ylim(yscale2)
    ax1.yaxis.labelpad = 0
    ax2.yaxis.labelpad = 0
    y_min, y_max = round(min(x2), 2), round(max(x2), 2)
    avg = round((sum(x2) / len(x2)), 2)
    s = 'max_traffic_vol. = ' + str(y_max) + '\n' + \
        'min_traffic_vol. = ' + str(y_min) + '\n' + \
        'avg_traffic_vol. = ' + str(avg)
    # ax1.axhline(y=y_max, xmin=-1, xmax=121, linewidth=2, color='b', linestyle='dotted')
    # ax1.axhline(y=y_min, xmin=-1, xmax=121, linewidth=2, color='b',linestyle='dashed')
    plot.annotate(s, annotation, fontsize=18)
    # plot.xticks(np.arange(len(conn)), np.arange(1, len(conn) + 1))
    # plot.xticks(conn)
    # plot.xticks(range(1,50,5))
    x_formatter = FixedFormatter([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    x_locator = FixedLocator([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax2.xaxis.set_major_formatter(x_formatter)
    ax2.xaxis.set_major_locator(x_locator)

    plot.tight_layout()
    plot.savefig(imagename + ".eps", format='eps', dpi=1200, pad_inches=0)
    # bbox_inches='tight'
    plot.clf()
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plot.show()
    x1.clear()
    x2.clear()


def plot_create_hist2(netconf_traffic, imagename):
    x1 = []
    x2 = []
    for t in netconf_traffic:
        x1.append(t[0])
        x2.append(round(t[1], 1))
    print('x2 {}'.format(x2))
    conn = np.arange(121)
    print(max(x1))

    plot.bar(conn, x2, color='g')
    plot.plot(conn, x1, 'o-', color='b')

    plot.show()
    x1.clear()
    x2.clear()


def plot_show_relation_XPDR(xscale, yscale, axisname, imagename, ):
    no_of_obs = xscale

    color = 'tab:blue'
    plot.plot(no_of_obs, yscale, color=color, marker='o')
    plot.xticks(np.arange(0, 18, 2))
    plot.yticks(np.arange(0, 4.5, 0.5))
    plot.xlabel(axisname, fontsize=12)
    plot.ylabel('Netconf Traffic[MB]', fontsize=12)
    # s = 'max_traffic = ' + str(y_max) + '\n' + \
    #     'min_traffic = ' + str(y_min)
    for x, y in zip(no_of_obs, yscale):
        label = "{:.2f}".format(y)

        plot.annotate(label,  # this is the text
                      (x, y),  # these are the coordinates to position the label
                      textcoords="offset points",  # how to position the text
                      xytext=(0, 10),  # distance from text to points (x,y)
                      ha='center')  # horizontal alignment can be left, right or center
    # plot.show()
    plot.tight_layout()
    plot.savefig(imagename + ".eps", format='eps', dpi=1200, pad_inches=0)
    # plot.savefig(imagename + ".png")
    # plot.clf()


def plot_show_relation_RDMS(xscale, yscale, yscale1, axisname, imagename):
    no_of_obs = xscale
    plot.figure(figsize=(9, 4), dpi=80)
    color = 'tab:blue'
    #plot.plot(no_of_obs, yscale, color=color, marker='o', label="Increase in ROADMs, degree=1")
    plot.plot(no_of_obs, yscale, color=color, marker='o', label="Downlink")
    color1 = 'tab:red'
    #plot.plot(no_of_obs, yscale1, color=color1, marker='o', label="Increase in degree, ROADMs=1")
    plot.plot(no_of_obs, yscale1, color=color1, marker='o', label="Uplink")
    plot.xticks(np.arange(1, 6))
    plot.yticks(np.arange(0, 2.5, 0.5))
    plot.xlabel(axisname, fontsize=18)
    plot.ylabel('Netconf Traffic volume [MB]', fontsize=18)
    plot.legend(loc='upper left', fancybox=True, fontsize=16)
    # s = 'max_traffic = ' + str(y_max) + '\n' + \
    #     'min_traffic = ' + str(y_min)
    # for x, y in zip(no_of_obs, yscale):
    #     label = "{:.2f}".format(y)
    #
    #     plot.annotate(label,  # this is the text
    #                   (x, y),  # these are the coordinates to position the label
    #                   textcoords="offset points",  # how to position the text
    #                   xytext=(0, 8.0),  # distance from text to points (x,y)
    #                   ha='center')  # horizontal alignment can be left, right or center
    # for x, y in zip(no_of_obs, yscale1):
    #     label = "{:.2f}".format(y)
    #
    #     plot.annotate(label,  # this is the text
    #                   (x, y),  # these are the coordinates to position the label
    #                   textcoords="offset points",  # how to position the text
    #                   xytext=(0, 8.0),  # distance from text to points (x,y)
    #                   ha='center')  # horizontal alignment can be left, right or center
    # plot.show()
    plot.tight_layout()
    plot.savefig(imagename + ".eps", format='eps', dpi=1200, pad_inches=0)
    plot.savefig(imagename + ".png")
    plot.clf()


def plot_create_hist_directional(netconf_traffic, y_label, yscale1, yscale2, imagename, annotation):
    rdms = []
    xpdrs = []
    rpc = []
    for t in range(0, 50):
        rdms.append(netconf_traffic[t][0])
        xpdrs.append(netconf_traffic[t][1])
        #rpc.append(round(netconf_traffic[t][2], 2))
        rpc.append(round(netconf_traffic[t][3], 2))

        # x1.append(t[0])
        # x2.append(round(t[1], 3))
    print('rdms {}'.format(rdms))
    print('xpdrs {}'.format(xpdrs))
    print('rpc {}'.format(rpc))
    conn = np.arange(start=1, stop=51)
    print(conn)

    fig, ax1 = plot.subplots(figsize=(10, 5.3))
    # figsize=(40, 30)
    color = 'tab:blue'
    ax1.set_xlabel('Lightpath ID', fontsize=20)
    ax1.set_ylabel('Netconf traffic volume [MB]', color=color, fontsize=20)
    ax1.bar(conn, rpc, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:orange'
    color1 = 'tab:green'
    ax2.set_ylabel(y_label, color=color, fontsize=20)  # we already handled the x-label with ax1
    ax2.plot(conn, rdms, 's', color=color, linewidth=0.75, label="ROADMs")
    ax2.plot(conn, xpdrs, 'o', color=color1, linewidth=0.75, label="Transponders")

    ax2.tick_params(axis='y', labelcolor=color)

    #  ax1.set_xlim(0, 51)
    ax1.set_ylim(yscale1)
    ax2.set_ylim(yscale2)
    ax1.yaxis.labelpad = 0
    ax2.yaxis.labelpad = 0
    y_min, y_max = round(min(rpc), 2), round(max(rpc), 2)
    avg = round((sum(rpc) / len(rpc)), 2)
    s = 'max_traffic_vol. = ' + str(y_max) + '\n' + \
        'min_traffic_vol. = ' + str(y_min) + '\n' + \
        'avg_traffic_vol. = ' + str(avg)
    # ax1.axhline(y=y_max, xmin=-1, xmax=121, linewidth=2, color='b', linestyle='dotted')
    # ax1.axhline(y=y_min, xmin=-1, xmax=121, linewidth=2, color='b',linestyle='dashed')
    plot.annotate(s, annotation, fontsize=18)
    plot.legend(loc='best', fontsize=18, prop={'size': 12})
    # plot.xticks(np.arange(len(conn)), np.arange(1, len(conn) + 1))
    # plot.xticks(conn)
    # plot.xticks(range(1,50,5))
    x_formatter = FixedFormatter([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    x_locator = FixedLocator([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax2.xaxis.set_major_formatter(x_formatter)
    ax2.xaxis.set_major_locator(x_locator)

    plot.tight_layout()
    plot.savefig(imagename + ".eps", format='eps', dpi=1200, pad_inches=0)
    plot.savefig(imagename + ".png")
    # bbox_inches='tight'
    plot.clf()
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plot.show()
    rdms.clear()
    xpdrs.clear()
    rpc.clear()


def plot_rdm_uldl_set_terminate(rdm_dl, rdm_ul, rdm_dl_term, rdm_ul_term, axisname, imagename):
    no_of_obs = np.arange(1, 6)
    rdm_dl_obs = []
    rdm_ul_obs = []
    rdm_dl_term_obs = []
    rdm_ul_term_obs = []
    for i in range(1, 6):
        rdm_dl_obs.append(rdm_dl * i)
        rdm_ul_obs.append(rdm_ul * i)
        rdm_dl_term_obs.append(rdm_dl_term * i)
        rdm_ul_term_obs.append(rdm_ul_term * i)

    print("rdm_dl_obs {}".format(rdm_dl_obs))
    print("rdm_ul_obs {}".format(rdm_ul_obs))
    print("rdm_dl_term_obs {}".format(rdm_dl_term_obs))
    print("rdm_ul_term_obs {}".format(rdm_ul_term_obs))
    plot.figure(figsize=(9, 4), dpi=80)
    color = 'tab:blue'
    plot.plot(no_of_obs, rdm_dl_obs, color=color, marker='o', label="Downlink-Lightpath Establishment")
    color1 = 'tab:red'
    plot.plot(no_of_obs, rdm_ul_obs, color=color1, marker='o', label="Uplink-Lightpath Establishment")
    color2 = 'tab:green'
    plot.plot(no_of_obs, rdm_dl_term_obs, color=color2, marker='o', label="Downlink-Lightpath Termination")
    color3 = 'tab:brown'
    plot.plot(no_of_obs, rdm_ul_term_obs, color=color3, marker='o', label="Uplink-Lightpath Termination")
    plot.xticks(np.arange(1, 6))
    plot.yticks(np.arange(0, 3.5, 0.5))
    plot.xlabel(axisname, fontsize=18)
    plot.ylabel('Netconf Traffic Size [MB]', fontsize=16)
    plot.legend(loc='upper left', fancybox=True, fontsize=12)
    # s = 'max_traffic = ' + str(y_max) + '\n' + \
    #     'min_traffic = ' + str(y_min)
    # for x, y in zip(no_of_obs, yscale):
    #     label = "{:.2f}".format(y)
    #
    #     plot.annotate(label,  # this is the text
    #                   (x, y),  # these are the coordinates to position the label
    #                   textcoords="offset points",  # how to position the text
    #                   xytext=(0, 8.0),  # distance from text to points (x,y)
    #                   ha='center')  # horizontal alignment can be left, right or center
    # for x, y in zip(no_of_obs, yscale1):
    #     label = "{:.2f}".format(y)
    #
    #     plot.annotate(label,  # this is the text
    #                   (x, y),  # these are the coordinates to position the label
    #                   textcoords="offset points",  # how to position the text
    #                   xytext=(0, 8.0),  # distance from text to points (x,y)
    #                   ha='center')  # horizontal alignment can be left, right or center
    # plot.show()
    plot.tight_layout()

    plot.savefig(imagename + ".eps", format='eps', dpi=1200, pad_inches=0)
    plot.savefig(imagename + ".png")
    plot.clf()


def model_netconf_traffic_XPDR(accepted_connections, transponders, model_traffic):
    # accepted_connections, blocked_connections, regen, transponders=rmsa.execute_RMSA()
    netconf_traffic_hist = []
    netconf_traffic = []
    for i in accepted_connections:
        get_dev_data = 0
        xpdrs = accepted_connections[i][2]
        xpdrs_nonLP = transponders - xpdrs

        # print("degree of roadms {} is {}".format(r, degree))
        get_dev_data = model_traffic.get_xpdrs_info(xpdrs)[0]
        edit_conn = model_traffic.connect_xdrs(xpdrs)[0]
        create_service_xpdr = model_traffic.service_create_xpdrs(xpdrs)[0]

        total_netconf_traffic_xpdr = get_dev_data + edit_conn + create_service_xpdr
        netconf_traffic_hist.append(total_netconf_traffic_xpdr)
        netconf_traffic.append((xpdrs, total_netconf_traffic_xpdr))

    return netconf_traffic_hist, netconf_traffic


def model_netconf_traffic_RDM(rmsa, model_traffic):
    nodes = []
    accepted_connections, blocked_connections, regen, transponders = rmsa.execute_RMSA()

    netconf_traffic_hist = []
    netconf_traffic = []
    for i in accepted_connections:
        get_dev_data = 0
        roadms = accepted_connections[i][0][0]
        roadm_nonLP = regen - len(roadms)
        for r in roadms:
            if r not in nodes:
                degree = rmsa.topology.graph.degree(r)
                get_dev_data = get_dev_data + model_traffic.model_roadm_traffic(degree)[0]
                nodes.append(r)

        # print("degree of roadms {} is {}".format(r, degree))
        # get_dev_data = get_dev_data + model_traffic.model_roadm_device_info(roadm_nonLP)
        edit_conn = model_traffic.model_edit_config_rdm(len(roadms))[0]
        create_service_rdm = model_traffic.service_create_rdms(len(roadms))[0]
        validation_traffc = model_traffic.connection_validate(len(roadms))[0]
        total_netconf_traffic_rdm = get_dev_data + edit_conn + create_service_rdm + validation_traffc
        netconf_traffic_hist.append(total_netconf_traffic_rdm)
        netconf_traffic.append((len(roadms), total_netconf_traffic_rdm))
    print('netconf_traffic_hist {}'.format(netconf_traffic))
    return netconf_traffic_hist, accepted_connections, transponders, netconf_traffic


def model_netconf_relational_traffic_RDM(model_traffic):
    # increase roadms keep degree constant
    const_degree = 1
    tr_const_degree = []
    trafficfor1Roadm = model_traffic.model_roadm_traffic(const_degree)[0] + model_traffic.model_edit_config_rdm(1)[0] + \
                       model_traffic.service_create_rdms(1)[0] + model_traffic.connection_validate(1)[0]
    for r in range(1, 6):
        tr_const_degree.append(trafficfor1Roadm * r)

    return tr_const_degree

def model_netconf_relational_traffic_degree(model_traffic):
    get_dev_rpc = []
    get_dev_reply = []
    for i in range(1, 6):
        roadm_traffic = model_traffic.model_roadm_traffic(i)
        get_dev_rpc.append(roadm_traffic[1])
        get_dev_reply.append(roadm_traffic[2])

    traffic_remaining_rpc = model_traffic.model_edit_config_rdm(1)[1] + model_traffic.service_create_rdms(1)[1] + \
                        model_traffic.connection_validate(1)[1]
    traffic_remaining_reply = model_traffic.model_edit_config_rdm(1)[2] + model_traffic.service_create_rdms(1)[2] + \
                        model_traffic.connection_validate(1)[2]
    tr_increase_degree_rpc = [x + traffic_remaining_rpc for x in get_dev_rpc]
    tr_increase_degree_reply = [x + traffic_remaining_reply for x in get_dev_reply]
    return tr_increase_degree_rpc, tr_increase_degree_reply

def model_netconf_traffic_RDM_directional(rmsa, model_traffic):
    nodes = []
    accepted_connections, blocked_connections, regen, transponders = rmsa.execute_RMSA()

    netconf_traffic_hist = []
    netconf_traffic = []
    for i in accepted_connections:
        get_device_info_rpc = 0
        get_device_info_reply = 0
        roadms = accepted_connections[i][0][0]
        roadm_nonLP = regen - len(roadms)
        for r in roadms:
            if r not in nodes:
                degree = rmsa.topology.graph.degree(r)
                get_device_info_rpc = get_device_info_rpc + model_traffic.model_roadm_traffic(degree)[1]
                get_device_info_reply = get_device_info_reply + model_traffic.model_roadm_traffic(degree)[1]
                nodes.append(r)

        # print("degree of roadms {} is {}".format(r, degree))
        # get_dev_data = get_dev_data + model_traffic.model_roadm_device_info(roadm_nonLP)
        edit_conn_rpc = model_traffic.model_edit_config_rdm(len(roadms))[1] + \
                        model_traffic.service_create_rdms(len(roadms))[1] + \
                        model_traffic.connection_validate(len(roadms))[1]
        edit_conn_reply = model_traffic.model_edit_config_rdm(len(roadms))[2] + \
                          model_traffic.service_create_rdms(len(roadms))[2] + \
                          model_traffic.connection_validate(len(roadms))[2]
        # calculate uplink and downlink for transponders
        xpdrs = accepted_connections[i][2]
        xpdr_rpc = model_traffic.get_xpdrs_info(xpdrs)[1] + model_traffic.connect_xdrs(xpdrs)[1] + \
                   model_traffic.service_create_xpdrs(xpdrs)[1]
        xpdr_reply = model_traffic.get_xpdrs_info(xpdrs)[2] + model_traffic.connect_xdrs(xpdrs)[2] + \
                     model_traffic.service_create_xpdrs(xpdrs)[2]
        total_rpc = get_device_info_rpc + edit_conn_rpc + xpdr_rpc
        total_reply = get_device_info_reply + edit_conn_reply + xpdr_reply
        netconf_traffic.append((len(roadms), xpdrs, total_rpc, total_reply))
    print('netconf_traffic_hist {}'.format(netconf_traffic))
    return netconf_traffic


def main():
    rmsa = rs.RMSA()
    model_traffic = CTModelling.Msg_Modelling()
    # netconf_traffic_hist_rdm, accepted_connections, transponders, netconf_traffic_rdm = model_netconf_traffic_RDM(rmsa,
    #                                                                                                               model_traffic)
    #
    # # plot_create_hist(netconf_traffic_hist_rdm, [0, 5], (2, 4.5), "NetconfTraffic_RDM")
    # plot_create_hist1(netconf_traffic_rdm, 'Number of ROADMS', [0, 5], [0, 10], "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/NetconfTraffic_RDM1", (1, 8))
    # netconf_traffic_hist_xpdr, netconf_traffic_xpdr = model_netconf_traffic_XPDR(accepted_connections, transponders,
    #                                                                              model_traffic)
    # print(accepted_connections)
    # # plot_create_hist(netconf_traffic_hist_xpdr, [0, 18], (2, 16.5), "NetconfTraffic_XPDR")
    # total_traffic = []
    # for (item1, item2) in zip(netconf_traffic_hist_rdm, netconf_traffic_hist_xpdr):
    #     total_traffic.append(item1 + item2)
    # # plot_create_hist(total_traffic, [0, 25], (2, 23.5), "NetconfTraffic_Total")
    # plot_create_hist1(netconf_traffic_xpdr, 'Number of Transponders', [0, 5], [0, 16], "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/NetconfTraffic_XPDR1", (1, 13))
    # x1 = []
    # x2 = []
    # x3 = []
    # for t in netconf_traffic_rdm:
    #     #x1.append(t[0])
    #     x2.append(round(t[1], 2))
    #
    #
    # for t in netconf_traffic_xpdr:
    #     if (t[0] not in x1) & (t[0]<16):
    #         x1.append(t[0])
    #         x3.append(round(t[1], 2))
    # print(x1,x3)
    # x = np.arange(1,6)
    # #plot_show_relation_XPDR(x1,x3,'Number of Transponders','/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/Relation_xpdrs')
    # const_degree, var_degree= model_netconf_relational_traffic_RDM(model_traffic)
    # plot_show_relation_RDMS(x, const_degree,var_degree, 'Number of ROADMs and degrees', '/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/Relation_RDM')

    # Find uplink and downlink control traffic
    get_dev_info_rpc = model_traffic.model_roadm_traffic(2)[1]
    get_dev_info_reply = model_traffic.model_roadm_traffic(2)[2]
    edit_config_rpc = model_traffic.model_edit_config_rdm(1)[1] + model_traffic.service_create_rdms(1)[1]
    edit_config_reply = model_traffic.model_edit_config_rdm(1)[2] + model_traffic.service_create_rdms(1)[2]
    conn_validate_rpc = model_traffic.connection_validate(1)[1]
    conn_validate_reply = model_traffic.connection_validate(1)[2]
    get_dev_info_rpc_xpdr = model_traffic.get_xpdrs_info(1)[1]
    get_dev_info_reply_xpdr = model_traffic.get_xpdrs_info(1)[2]
    edit_config_rpc_xpdr = model_traffic.connect_xdrs(1)[1] + model_traffic.service_create_xpdrs(1)[1]
    edit_config_reply_xpdr = model_traffic.connect_xdrs(1)[2] + model_traffic.service_create_xpdrs(1)[2]
    total_netconf_traffic_rdm_downlink = get_dev_info_rpc + edit_config_rpc + conn_validate_rpc
    total_netconf_traffic_rdm_uplink = get_dev_info_reply + edit_config_reply + conn_validate_reply
    total_netconf_traffic_xpdr_downlink = get_dev_info_rpc_xpdr + edit_config_rpc_xpdr
    total_netconf_traffic_xpdr_uplink = get_dev_info_reply_xpdr + edit_config_reply_xpdr
    total_netconf_traffic_rdm_ul_terminate = model_traffic.model_lp_termination_rdm(1)[2]
    total_netconf_traffic_rdm_dl_terminate = model_traffic.model_lp_termination_rdm(1)[1]
    total_netconf_traffic_xpdr_ul_terminate = model_traffic.model_lp_termination_xpdr(1)[2]
    total_netconf_traffic_xpdr_dl_terminate = model_traffic.model_lp_termination_xpdr(1)[1]
    print('total_netconf_traffic_rdm_uplink : {}'.format(total_netconf_traffic_rdm_uplink))
    print('total_netconf_traffic_rdm_downlink : {}'.format(total_netconf_traffic_rdm_downlink))
    print('total_netconf_traffic_xpdr_uplink: {}'.format(total_netconf_traffic_xpdr_uplink))
    print('total_netconf_traffic_xpdr_downlink: {}'.format(total_netconf_traffic_xpdr_downlink))
    print('total_netconf_traffic_rdm_ul_terminate : {}'.format(total_netconf_traffic_rdm_ul_terminate))
    print('total_netconf_traffic_rdm_dl_terminate : {}'.format(total_netconf_traffic_rdm_dl_terminate))
    print('total_netconf_traffic_xpdr_ul_terminate: {}'.format(total_netconf_traffic_xpdr_ul_terminate))
    print('total_netconf_traffic_xpdr_dl_terminate: {}'.format(total_netconf_traffic_xpdr_dl_terminate))
    netconf_traffic = model_netconf_traffic_RDM_directional(rmsa, model_traffic)
    plot_create_hist_directional(netconf_traffic,'Number of devices', [0, 5], [0, 16], "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/NetconfTraffic_Uplink", (1, 13))
    plot_rdm_uldl_set_terminate(total_netconf_traffic_rdm_downlink, total_netconf_traffic_rdm_uplink,
                                total_netconf_traffic_rdm_dl_terminate, total_netconf_traffic_rdm_ul_terminate,
                                "Number of ROADMs",
                                "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/NetconfTraffic_RDMNew")
    plot_rdm_uldl_set_terminate(total_netconf_traffic_xpdr_downlink, total_netconf_traffic_xpdr_uplink,
                                total_netconf_traffic_xpdr_dl_terminate, total_netconf_traffic_xpdr_ul_terminate,
                                "Number of Transponders",
                                "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/NetconfTraffic_XPDRNew")
    tr_increase_degree_rpc, tr_increase_degree_reply=model_netconf_relational_traffic_degree(model_traffic)
    plot_show_relation_RDMS(np.arange(1, 6),tr_increase_degree_rpc,tr_increase_degree_reply,"Number of ROADM Degrees", "/home/shabnam/PycharmProjects/Doktorarbeit/FNSS/Images/Relation_degree")



get_schema_load_rdm = 0
get_schema_load_xpdr = 0
get_schema_load_nonLP = 0
conn_rdm_load = 0
conn_xpdr_load = 0
create_service_load_rdm = 0
create_service_load_xpdr = 0
conn_rdm_data_nonLP = 0
conn_xpdr_data_nonLP = 0
validation_load = 0

get_dev_data = 0

# #'get schema messages'
# get_schema_load_rdm= model_traffic.model_get_schema(roadms)
# get_schema_load_xpdr= model_traffic.model_get_schema(xpdrs)
# get_schema_load_nonLP= model_traffic.model_get_schema(roadm_nonLP+xpdrs_nonLP)
# #'connection messages'
# conn_rdm_load=conn_rdm_load + model_traffic.model_connection_nodes(roadms)
# conn_xpdr_load= conn_xpdr_load + model_traffic.connect_xdrs(xpdrs)
# conn_rdm_data_nonLP=conn_rdm_data_nonLP+model_traffic.model_connection_nodes_nonLP(roadm_nonLP)
# conn_xpdr_data_nonLP=conn_xpdr_data_nonLP+model_traffic.connect_xpdrs_nonlp(xpdrs_nonLP)
# # service create messages
# create_service_load_rdm=create_service_load_rdm + model_traffic.service_create_rdms(roadms)
# create_service_load_xpdr=create_service_load_xpdr+ model_traffic.service_create_xpdrs(xpdrs)
# # validate conn
# validation_load =validation_load + model_traffic.connection_validate(roadms)

total_nonLP_traffic = conn_rdm_data_nonLP + conn_xpdr_data_nonLP

# print("get_schema_load RDM{}:".format(get_schema_load_rdm))
# print("get_schema_load_xpdr {}".format(get_schema_load_xpdr))
# print("get_schema_load_nonLP {}".format(get_schema_load_nonLP))
# print("conn_rdm_load: {}".format(conn_rdm_load))
# print("conn_xpdr_load : {}".format(conn_xpdr_load))
# print("create_service_load_rdm: {}".format(create_service_load_rdm))
# print("create_service_load_xpdr : {}".format(create_service_load_xpdr))
# print("validation_load: {}".format(validation_load))
# print("conn_rdm_data_nonLP: {}".format(conn_rdm_data_nonLP))
# print("conn_xpdr_data_nonLP: {}".format(conn_xpdr_data_nonLP))
# print("total_nonLP_traffic {}".format(total_nonLP_traffic))


if __name__ == "__main__":
    main()
