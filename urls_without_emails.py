
import csv
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



