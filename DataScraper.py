from bs4 import BeautifulSoup

class DataScraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser') if html_content else None
    
    def extract_properties(self):
        if not self.soup:
            return []
            
        cards = self.soup.select('a.ListingCard_result-card__Pumtx')
        properties = []
        
        for card in cards:
            try:
                property_data = {
                    'titulo': self._get_text(card, 'h2 span:first-child'),
                    'localizacao': self._get_attribute(card, 'h2 span:last-child', 'title'),
                    'endereco': self._get_attribute(card, 'p[title]', 'title'),
                    'preco': self._get_text(card, 'p.text-2-25'),
                    'condominio_iptu': self._get_text(card, 'p.text-1-75:not(.flex)'),
                    'area': self._get_detail(card, 0),
                    'quartos': self._get_detail(card, 1),
                    'banheiros': self._get_detail(card, 2),
                    'vagas': self._get_detail(card, 3),
                    'destaque': self._get_text(card, '.l-tag-card__content', default='Normal'),
                    'link': f"https://www.zapimoveis.com.br{card.get('href', '')}"
                }
                properties.append(property_data)
            except Exception as e:
                print(f"Erro ao processar card: {e}")
                continue
        
        return properties
    
    def _get_text(self, element, selector, default='Não informado'):
        found = element.select_one(selector)
        return found.text.strip() if found else default
    
    def _get_attribute(self, element, selector, attr, default='Não informado'):
        found = element.select_one(selector)
        return found.get(attr, default) if found else default
    
    def _get_detail(self, element, index, default='Não informado'):
        details = element.select('ul.flex.flex-row.text-1-75 li')
        return details[index].text.strip() if len(details) > index else default