import copy
import quopri

def parse_val(holder, line):
    tmp = line.split(';')
    if tmp[0] == 'FN':
        holder['name'] = quopri.decodestring(tmp[2].split(":", 1)[1])
    elif tmp[0] == 'TEL' and tmp[1] != 'CELL':
        holder['phone'] = tmp[1].split(':', 1)[1].replace('-', '')
    elif tmp[0] == 'TEL' and tmp[1] == 'CELL':
        holder['mobile'] = tmp[2].split(':', 1)[1].replace('-', '')


def parse_vcf(input_file, out_file):
    contacts = []

    contact_holder = {
        'name': '',
        'mobile': '',
        'phone': ''
    }

    in_msg = False
    try:
        with open(input_file, 'r') as temp_f:
            for line in temp_f.readlines():
                line = line.strip()
                if not in_msg and line == 'BEGIN:VCARD':
                    in_msg = True
                elif line == 'END:VCARD':
                    contacts.append(copy.deepcopy(contact_holder))
                    contact_holder['name'] = ''
                    contact_holder['mobile'] = ''
                    contact_holder['phone'] = ''
                    in_msg = False
                elif line != 'VERSION:2.1':
                    parse_val(contact_holder, line)
    except IOError:
        print('Error, make sure your vmsg file is named sms.vmsg and is in the same folder.')
    write_cvs(contacts, out_file)


def write_cvs(contacts, out_file):
    with open(out_file, 'w') as temp_f:
        temp_f.write('name,mobile,phone\n')
        for item in contacts:
            temp_f.write(item['name']+','+item['mobile']+','+item['phone']+'\n')


if __name__ == '__main__':
    parse_vcf('contact.vcf', 'contact.cvs')
