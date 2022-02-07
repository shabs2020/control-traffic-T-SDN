import re
import os
import shutil

messages = {}

def extract_rpc_message(text):
    # regex = r"<rpc message-id=.*?\n\t*\<\/rpc>" = r"(RemoteDevice\{.{0,8}(?=\}).:)(?:.*?)(\<rpc message-id=[\s\S]*?\<\/rpc>)"
    regex = r"(RemoteDevice\{.{0,8}(?=\}).:)(?:.*?)(\<rpc message-id=[\s\S]*?\<\/rpc>)"
    regex_extraction(regex, text, 'rpc-message-')




def extract_rpc_reply(text):
    # regex = r"<rpc-reply xmlns.*?\n\t*\<\/rpc-reply."
    regex = r"(RemoteDevice\{.{0,8}(?=\}).:)(?:.*?)(\<rpc-reply xmlns[\s\S]*?\<\/rpc-reply>)"
    regex_extraction(regex, text, 'rpc-reply-')


def regex_extraction(regex, text, file_name):

    # matches = re.finditer(regex, text, re.DOTALL | re.MULTILINE)
    matches = re.finditer(regex, text)
    for matchNum, match in enumerate(matches, start=1):

        # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
        #                                                                         end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):

            groupNum = groupNum + 1
            xml_body = match.group(groupNum)
            # print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
            #                                                                 start=match.start(groupNum),
            #                                                                 end=match.end(groupNum),
            #                                                                 group=xml_body))
            if 'RemoteDevice' in xml_body:
                device = _get_device_name(xml_body)
            else:
                # print("Found xml {}".format(xml_body))
                find_msg_id = xml_body.split('"')[1::2]
                substring_in_list = [string for string in find_msg_id if "m-" in string]

                # print("message_id {}".format(substring_in_list[0]))
                # rpc_write_to_file('NetconfMessagesSuccess/' + file_name + substring_in_list[0], xml_body)
                message = xml_body
        if ('XPDR-C1' in device) & ('m-135' in message):
            print("Culprit Found".format(match.group()))

        rpc_write_to_file(create_device_dir(device) + '/' + file_name + substring_in_list[0],
                                  message)
        # messages[device +'-'+ substring_in_list[0]] = message
    # return messages

def _get_device_name(text_body):

    if text_body.count('_value='):
        result = re.search('RemoteDevice{Uri{_value=(.*)}', text_body)

        device_name = result.group(1)
        print("device name is condition1 {}: ".format(result.group(1)))
    else:
        device_name = text_body.split('{', 1)[1].split('}')[0]
        print("device name is condition2 {}: ".format(device_name))
    return device_name

def _get_rpc_body(xml_body,device_name, file_name):
    find_msg_id = xml_body.split('"')[1::2]
    substring_in_list = [string for string in find_msg_id if "m-" in string]

    print("message_id {}".format(substring_in_list[0]))
    # rpc_write_to_file('NetconfMessagesSuccess/' + file_name + substring_in_list[0], xml_body)
    rpc_write_to_file(create_device_dir(device_name) + '/' + file_name + substring_in_list[0],
                      xml_body)

def create_device_dir(device_name):
    path = 'NetconfMessagesService2/' + device_name
    # path = 'NetconfMessagesFailure/' + device_name

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    return path


def rpc_write_to_file(filename, body):
    counter = 1
    while(os.path.exists(filename)):
        old_file= open(filename, 'r')
        text= old_file.read()
        if text != body:
            filename = filename + '_' + str(counter)
            counter += 1
        else:
            break
    with open(filename, 'w') as f:
        f.write(body)
    f.close()







def del_all_files(directory):
    print("Deleting Files")
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
        print("All files deleted")


def del_dir(directory):
    for f in os.listdir(directory):
        sub_dir = os.path.join(directory, f)
        for g in os.listdir(sub_dir):
            os.remove(os.path.join(sub_dir, g))
            print("All files deleted")
        os.rmdir(os.path.join(directory, f))
        print("All device directories deleted")


def enter_timestamp(file):
    global device
    regex = r"(?<=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}))(?:.*?)(RemoteDevice\{.+?(?=\}).)(?:.*?)(\<rpc message-id=.*?\n\t*\<\/rpc>)"
    logfile= open(file, 'r')
    logs = logfile.read()
    matches = re.finditer(regex, logs, re.MULTILINE | re.DOTALL)
    message_dict ={}
    group_list = []
    counter = 0
    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):

            groupNum = groupNum + 1
            group_list.append(match.group(groupNum))

            # print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
            #                                                                 start=match.start(groupNum),
            #                                                                 end=match.end(groupNum),
            #                                                                 group=match.group(groupNum)))

        timestamp = group_list[0]
        device = _get_device_name(group_list[1])
        find_msg_id = group_list[2].split('"')[1::2]
        substring_in_list = [string for string in find_msg_id if "m-" in string]
        xml_body = group_list[2]

       # print("message_id {}".format(substring_in_list[0]))

        keyname = device + substring_in_list[0]
        # while (device + substring_in_list[0] in message_dict.keys()):
        #     old_value = message_dict[device + substring_in_list[0]]
        #
        #     if old_value != xml_body:
        #         keyname = device + substring_in_list[0] + '_' + str(counter)
        #         counter += 1
        #     else:
        #         break
        #print(group_list)

        message_dict[counter] = [timestamp,device,substring_in_list[0],xml_body]
        counter += 1
        group_list.clear()

    return message_dict

def isAscending(xs):
    for n in range(len(xs) - 1):
        if xs[n] > xs[n+1]:
            return False
    return True

def validate_timestamp(file,dev):

    messages= enter_timestamp(file)
    print(messages)
    for n in range(0,len(messages) - 1):

        if dev in messages[n][1].lower():
            print ("Message {} created in timestamp {} for device {}".format(messages[n][2], messages[n][0], messages[n][1]))




    #shutil.rmtree(directory)
# #
# log_file = open('Logs/20211122T114342Z_trpce_netconf.log', 'r')
log_file = open('Logs/20220104T142053Z_trpce_netconf.log', 'r')
logs = log_file.read()
extract_rpc_message(logs)
extract_rpc_reply(logs)
# messages=extract_rpc_message(logs)
# # extract_rpc_reply(logs)
# x = [value for key, value in messages.items() if 'XPDR-C1' in key]
#
# for items in x:
#     if "m-137" in items:
#         print(items)



#del_dir('NetconfMessagesService2/')
# log_fi
#validate_timestamp('Logs/20211105T085125Z_trpce_netconf_success.log','roadm-a1')
#del_dir('NetconfMessagesSuccess/')
#del_dir('NetconfMessagesFailure/')
# del_all_files('NetconfMessagesService2/')
