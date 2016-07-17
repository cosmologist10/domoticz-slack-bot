from datetime import datetime

from commands import commands
from slack.slack_helper import generate_table_attachment, generate_attachment, datetime_to_ts


def get_domoticz_status(data):
    attachments = generate_table_attachment('Device Status', 'neutral', data, 'Device Status Update')
    return attachments


def get_device_status(domo, name):
    devices = filter(lambda k: name.lower() in k['Name'].lower(), domo.device_list)
    if len(devices) == 0:
        return

    idx = devices[0]['idx']
    data = domo.get_device_data(idx=idx)
    data = data[0]
    ts = datetime_to_ts(datetime.strptime(data['LastUpdate'], '%Y-%m-%d %H:%M:%S'))
    attachment = generate_attachment(data['Name'], 'neutral', data['Data'], ts)
    return attachment


def process(domo, cmd, command_grp):
    if cmd in commands[command_grp]:
        data = domo.get_device_status_many(cmd)
        return get_domoticz_status(data)
    else:
        return get_device_status(domo, cmd)
