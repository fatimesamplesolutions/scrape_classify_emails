from pprint import pprint

import urllib.parse


def truncate_url_return_domain():
    with open('urls_of_scraped_emails.csv', 'r') as readfile, open('urls_of_scraped_emails_.csv', 'w') as writefile:
        for line in readfile.readlines():
            parsed_uri_ = urllib.parse.urlparse(line.strip())
            domain = '{uri.scheme}://{uri.netloc}/\n'.format(uri=parsed_uri_)
            writefile.write(domain)
            print(domain)

def compare_two_fucking_csv_files():
    with open('found_url_2_.csv', 'r') as all_urls, open('urls_of_scraped_emails_.csv', 'r') as scraped_urls:
        difference = set(all_urls) - set(scraped_urls)
        print(difference)

        with open('different.csv', 'w') as save_difference:
            for line in difference:
                save_difference.write(line)

# truncate_url_return_domain()
# compare_two_fucking_csv_files()


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
