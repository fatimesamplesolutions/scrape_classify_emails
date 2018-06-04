import pandas as pd
import csv

csv_data = pd.read_csv('emails.csv', index_col=False, header=0)

general_words_list = ['info','contact','HELLO','sales','mail','webmaster','secretariaat','support','secretariat','office','infos','baf','job-psabelux','admin','hallo','direction','Directie','voorbeeld','welcome','verkoop','E-mailinfo','bestuur','service','kantoor','information','immo','shop','welkom','administratie','studio','naam','web','post','voorzitter','license','informatie','Emailinfo','accueil','notaris','bureau','administration','antwerpen','reservation','postmaster','info.be','email','atelier','resto','verzekeringen','jobs','info.antwerpen','architect','secretaris','website','restaurant','team','onthaal','kbc.helpdesk','brussels','brugge','president','help','etude','communication','advocaten','advocaat','verhuur','reservations','IRTeam','klantenservice','directeur','assurances','press','webshop','yannick','vynckier','redactie','exemple','helpdesk','expertisecenter.north-west','reservatie','toerisme','jeugd','info-be','hi','customerservice','berichtinfo','courrier','planning','vragen','marketing','gent','cultuur','commercial','brussel','bestellingen','antwerp','praktijk','pbe.office','traiteur','internetbank','orders','management','garage','bonjour','boekhouding','presse','winkel','ocmw','optiek','mailinfo','name','order','fotografie','drukkerij','secretaire','receptie','reception','secretary','zakenkantoor','notaire','media','kontakt','design','go','expert','dispatching','dokter','hr','infor-etudes','groepsleiding','finance','comptabilite','advocatenkantoor','architecten','accounting','contacts','commandes','Business']

general_emails = []
personal_emails = []
website = []

def main():

    # Read csv file, delete duplicates and write it.
    with open('log.csv', 'r',newline='') as inputfile:
        with open('testout.csv', 'w', newline='') as outputfile:
            duplicatereader = csv.DictReader(inputfile, delimiter=',')
            uniquewrite = csv.DictWriter(outputfile, fieldnames=['no', 'company', 'website'], delimiter=',')
            uniquewrite.writeheader()
            keysread = []
            for row in duplicatereader:
               key = (row['company'])
               if key not in keysread:
                   print(row)
                   keysread.append(key)
                   uniquewrite.writerow(row)

"""Execute this when run the script first time only"""
if __name__ == '__main__':
    main()


def classify_emails():
    for row in csv_data.itertuples():
        # print(row[2:4])

        get_email = row.email
        get_email_lower = get_email.lower()

        for i in general_words_list:

            try:
                if len(row) == 0:
                    continue
                else:
                    if -1 != get_email_lower.find(i):
                        general_emails.append(get_email_lower)

            except ValueError:
                print('No result')
                continue
        if get_email_lower not in general_emails:
            pass

            # website.append(*row[2:3]) # unpacking tuples
            # personal_emails.append(get_email_lower)

    classified_csv()


def classified_csv():

    df1 = pd.DataFrame(general_emails, columns=['General'])
    # df2 = pd.DataFrame(personal_emails, website, columns=['company, website'])
    # df1.reset_index(drop=False)
    # df2.reset_index(drop=False)
    # df = pd.concat([df1, df2], axis=1)
    # df.dropna()
    df1.drop_duplicates(inplace=True)
    # df2.index = df2.index + 1
    df1.to_csv('classified_emails_scrapy.csv', index=False)
    return df1


classify_emails()
