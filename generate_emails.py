from pprint import pprint

def remove_www_from_domains(input_file):
    domains_with_www = []
    domains_without_www = []
    domains = []

    with open(input_file,'r') as read_file, open('domains.csv', 'w') as write_file:
        for line in read_file.readlines():
            v = line.split("//")[-1].split("/")[0].split('?')[0]
            v = v.lower()
            if -1 == v.find('www.'):
                domains_without_www.append(v)
            elif -1 != v.find('www.'):
                v1 = v.replace('www.','')
                domains_with_www.append(v1.strip())
                pass

            domains = domains_without_www+domains_with_www

        for item in domains:
            write_file.write(item+'\n')

        pprint(len(domains))


def generate_emails(input_file):
    generated_emails = []

    with open(input_file, 'r') as read_file, open('generated_emails.csv','w') as write_file:
        for line in read_file.readlines():
            v = 'info@'+line
            generated_emails.append(v.strip())

        for item in generated_emails:
            write_file.write(item+'\n')

        pprint(generated_emails)
