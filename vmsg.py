import time
import calendar
import copy
import quopri


def parse_val(holder, line):
    line = line.split(':', 1)
    if line[0] == 'TEL':
        holder['address'] = line[1]
    elif line[0] == 'X-BOX':
        if line[1] == 'INBOX':
            holder['type'] = '1'
        else:
            holder['type'] = '2'
    elif line[0] == 'X-READ':
        if line[1] == 'READ':
            holder['read'] = '1'
        else:
            holder['read'] = '0'
    elif line[0] == 'X-LOCKED':
        if line[1] == 'UNLOCKED':
            holder['locked'] = '0'
        else:
            holder['locked'] = '1'
    elif line[0] == 'Date':
        date_time = time.strptime(line[1], '%Y/%m/%d %H:%M:%S')
        holder['date'] = str(calendar.timegm(date_time))
        date_time = time.localtime(calendar.timegm(date_time))
        holder['readable_date'] = time.strftime('%b %d, %Y %H:%M:%S %p',date_time)
    elif line[0][:8] == 'Subject;':
        holder['body'] = line[1]


def parse_vmsg(input_file):
    msgs = []
    holder = {
        'address': None,
        'type': None,
        'read': None,
        'locked': None,
        'date': None,
        'readable_date': None,
        'body': None,
        'protocol': '0',
        'subject': 'null',
        'toa': 'null',
        'sc_toa': 'null',
        'service_center': 'null',
        'status': '-1',
        'date_sent': '0'
        }

    in_msg = False
    try:
        with open(input_file, 'r') as temp_f:
            for line in temp_f.readlines():
                line = line.strip()
                if not in_msg and line == 'BEGIN:VMSG':
                    in_msg = True
                elif line == 'END:VMSG':
                    msgs.append(copy.deepcopy(holder))
                    in_msg = False
                else:
                    parse_val(holder, line)
        return msgs
    except IOError:
        return None


def convert(input_file, out_file):
    msgs = parse_vmsg(input_file)
    header = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n """
    header += """ <?xml-stylesheet type="text/xsl" href="sms.xsl"?>\n<smses count=" """
    header += str(len(msgs))
    header += """" backup_date="none">\n"""

    with open(out_file, 'w') as temp_f:
        temp_f.write(header)
        for item in msgs:
            body = quopri.decodestring(item['body'])
            readable_date = time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.strptime(item['readable_date'], '%b %d, %Y %H:%M:%S %p'))
            app_line = '  <sms protocol="0" address="'\
                + item['address'] + '" date="' + item['date']\
                + '" type="1" subject="null" body="'\
                + body\
                + '" toa="null" sc_toa="null" service_center="null" read="1" status="-1"'\
                + ' locked="0" date_sent="'\
                + item['date_sent']\
                + '" readable_date="'\
                + readable_date + '" />\n'
            temp_f.write(app_line)
        temp_f.write('</smses>')


if __name__ == '__main__':
    convert('sms.vmsg', 'sms.xml')