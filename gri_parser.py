from bs4 import BeautifulSoup
class gri_parser():
    '''
    parser the search result of https://database.globalreporting.org/search/
    
    '''
    def index_parser(self,content):
        '''
        20201022
        to parser the search result
        Args:
            content (binary or str): the html source of page
        Returns:
            dict: a data dictionary
        '''
        # data container
        data_dict = {'ORG_name':[],'ORG_url':[],'size':[],'sector':[],'country':[], 'region':[], 'reports':[]}
        
        # parse
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table',{'class':'table table-hover dataTable'})
        tablebody = table.tbody
        for tr in tablebody.find_all('tr'):
            tmp_dict = {}
            tds = tr.find_all('td')
            tmp_dict['ORG_name'] = tds[0].get_text().strip()
            tmp_dict['ORG_url'] = tds[0].h4.a['href']
            tmp_dict['size'] = tds[1].get_text()
            tmp_dict['sector'] = tds[2].get_text()
            tmp_dict['country'] = tds[3].img['src']
            tmp_dict['region'] = tds[4].get_text()
            tmp_dict['reports'] = []
            
            for a in tds[5].find_all('a'):
                tmp_report = {}
                tmp_report['report_url'] = a['href']
                tmp_report['report_year'] = a.span.contents[0].replace('-','').strip()
                tmp_report['report_label'] = a.find('span',{'class':'text-slim label label-primary'}).get_text().strip()
                tmp_dict['reports'].append(tmp_report)
            
            for k in data_dict.keys():
                data_dict[k].append(tmp_dict.get(k))
        return data_dict

# if __name__ == '__main__':
with open('database.globalreporting.org_search.html','rb') as f:
    content = f.read()
gp = gri_parser()
data_dict = gp.index_parser(content)
# print(data_dict)
