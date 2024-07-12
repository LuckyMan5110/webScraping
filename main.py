# python main.py

# all exporting and importing python library on pc
# pip freeze > requirements.txt
# pip install -r requirements.txt

#virtaul env
# virtualenv venv
# cd venv
# cd Scripts
# activate, deactivate

from bs4 import BeautifulSoup
import requests
import csv

def get_urls():
    header = ['name', 'url', 'title', 'city', 'country', 'com_url', 'facebook', 'linkedin', 'twitter', 'instagram']

    url = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/Exhibitors.aspx?Index=All"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")

    div_element = soup.find("div",  class_="listTableBody")
    table = div_element.find("table")
    body = table.find("tbody")
    result = body.find_all("tr")

    with open('url_file.csv', 'w', encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        prefix = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/"
        for tr in result:
            data = tr.find("td", class_="companyName")
            url = data.find_all("a")
            csv_data = [data.text, prefix + url[0]["href"] ]
            writer.writerow(csv_data)
        print(f"********url extraction completed********")

def get_info_from_urls():
    with open('url_file.csv', mode='r', encoding="UTF8") as csv_file:
        with open('info_file.csv', mode='w', newline="", encoding="UTF8") as write_file:
            print(f"******* start company info extraction *******")

            fieldnames = ['name','url','title','city','country','com_url','facebook','linkedin','twitter','instagram']
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)
            writer.writeheader()

            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    print(f"******* wait for a few minutes *******")

                    line_count += 1

                target_url = row['url']
                page = requests.get(target_url)
                soup = BeautifulSoup(page.content, "html.parser")
                container = soup.find(id="eboothContainer")
                panel = container.find("div", class_="panel")
                panel_body = panel.find("div", class_="panel-body")
                title = panel_body.find("h1")
                body = panel_body.find("div", class_="BoothContactInfo pull-left")
                city = panel_body.find("span", class_="BoothContactCity")
                country = panel_body.find("span", class_="BoothContactCountry")
                url = panel_body.find("span", class_="BoothContactUrl")

                socialContainer = panel_body.find(id="ctl00_ContentPlaceHolder1_ctrlCustomField_Logos_dlCustomFieldList")
                socialUrls = socialContainer.find_all("span", class_="spCustomFieldIcon")

                dict = {}
                dict['name'] = row['name']
                dict['url'] = row['url']
                dict['title'] = title.text
                dict['city'] = city.text
                dict['country'] = country.text
                dict['com_url'] = url.text

                for item in socialUrls:
                    social_url = item.find_all("a")
                    if(social_url != []):
                        href = social_url[0]["href"]
                        if (href.count("www.facebook.com") > 0):
                            dict['facebook'] = href

                        if (href.count("www.linkedin.com") > 0):
                            dict['linkedin'] = href

                        if (href.count("www.instagram.com") > 0):
                            dict['instagram'] = href

                        if (href.count("twitter.com") > 0):
                            dict['twitter'] = href

                writer.writerow(dict)

                line_count += 1

            print(f'***Processed {line_count} lines.***')
        
get_urls()
get_info_from_urls()

