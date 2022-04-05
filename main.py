from httplib2 import Http
from bs4 import BeautifulSoup
from datetime import date
import csv


def crawlastroica(st_date: date, end_date:date):
    res, content = Http().request(uri="https://www.astroica.com/vedic-astrology/nakshatra-calculator.php",
                                  method="POST",
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
                                      'Referer': 'https://www.astroica.com/vedic-astrology/nakshatra-calculator.php',
                                      'Origin': 'https://www.astroica.com',
                                      'Content-type': 'application/x-www-form-urlencoded'
                                  },
                                  body="st_year=" + str(st_date.year)
                                       + "&st_month=" + str(st_date.month)
                                       + "&st_day=" + str(st_date.day)
                                       + "&end_year=" + str(end_date.year)
                                       + "&end_month=" + str(end_date.month)
                                       + "&end_day=" + str(end_date.day)
                                       + "&location=Mumbai&loc=1275339&ayanamsa=1&p=1"
                                  )
    if res.status == 200:
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup.prettify())
        table_tag = soup.table
        rows = table_tag('tr')
        cols = rows[0](["td", "th"])
        table = []
        for row in rows:
            table.append([])
            for col in row(["td", "th"]):
                # print(col)
                table[-1].append(col.text)
        return table


def csv_writer(filename:str, table:list):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(table)


if __name__ == '__main__':
    start_date = date(2022, 11, 1)
    end_date = date(2022, 12, 1)
    csv_writer(str(start_date) + '-' + str(end_date), crawlastroica(start_date, end_date))
    print("CSV file " + str(start_date) + '-' + str(end_date) + " created.")
