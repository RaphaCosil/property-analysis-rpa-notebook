import time
import random
from BrowserManager import BrowserManager
from DataScraper import DataScraper
from DataProcessor import DataProcessor

class ZapImoveisScraper:
    def __init__(self):
        self.browser = BrowserManager()
    
    def scrape_location(self, location):
        try:
            print(f"\nIniciando scraping para: {location}")
            
            url = f"https://www.zapimoveis.com.br/venda/imoveis/{location}/"
            html_content = self.browser.get_page(url)
            
            if not html_content:
                print("Falha ao obter conteúdo da página")
                return None
            
            scraper = DataScraper(html_content)
            properties = scraper.extract_properties()
            
            if not properties:
                print("Nenhum imóvel encontrado para a localização especificada")
                return None
            
            processor = DataProcessor(properties)
            clean_df = processor.clean_data()
            
            if clean_df.empty:
                print("Nenhum dado válido após processamento")
                return None
            
            return clean_df
            
        except Exception as e:
            print(f"Erro durante o scraping: {e}")
            return None
        finally:
            self.browser.close()
            time.sleep(random.uniform(3, 7))