from bs4 import BeautifulSoup
# from schrodinger.structure import StructureReader, StructureWriter
import requests
import urllib3
import time
import re
import sys
from tqdm import tqdm

urllib3.disable_warnings()

# FUCK YOU: https://go.drugbank.com/unearth/q?utf8=%E2%9C%93&query=aspirin&searcher=drugs
#                                                                  ^^^^^^^

def get_data(ID):
    url = "https://go.drugbank.com/drugs/%s" % ID
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    try:
        title, description = soup.find_all(name='meta', attrs={'name': ['dc.title', 'description']})
        atc = soup.find_all(name="a", attrs={'href': re.compile(r'/atc/')})
        categories = soup.find_all("a", {'href': re.compile(r'/categories/')})
        
        atc = '; '.join(set(code.text for code in atc))
        categories = '; '.join(cat.text for cat in categories)
        title = title.attrs['content']
        description = description.attrs['content']
    except ValueError:
        title, description, atc, categories = ['not found'] * 4

    return title, description, atc, categories


def main():
    # sts = StructureReader(infile)
    # writer = StructureWriter(outfile)
    with open(sys.argv[1], 'r') as inp:
        with open(sys.argv[2], 'w') as out:
            out.write('s_sd_supplier\_code\ts_u_drug_name\ts_u_drug_description\ts_u_drug_ATC_code\ts_u_drug_categories\n')
            for line in tqdm(inp.readlines()):
                dbcode = line.strip()
                title, descr, atc, cat = get_data(dbcode)
                out.write(f'{dbcode}\t{title}\t{descr}\t{atc}\t{cat}\n')


if __name__ == "__main__":
    main()
