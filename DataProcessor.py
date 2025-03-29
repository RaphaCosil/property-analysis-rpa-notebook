import re
import pandas as pd

class DataProcessor:
    def __init__(self, raw_data):
        self.df = pd.DataFrame(raw_data) if raw_data else pd.DataFrame()
    
    def clean_data(self):
        if self.df.empty:
            return self.df
            
        try:
            self.df['preco_num'] = self.df['preco'].apply(self._convert_price)
            
            self.df[['condominio', 'iptu']] = self.df['condominio_iptu'].apply(self._extract_condominio_iptu)
            
            self.df['area_num'] = self.df['area'].str.extract(r'(\d+)').astype(float)
            
            self.df.fillna({
                'preco_num': 0,
                'condominio': 0,
                'iptu': 0,
                'area_num': 0,
                'quartos': 0,
                'banheiros': 0,
                'vagas': 0
            }, inplace=True)
            
            return self.df
        except Exception as e:
            print(f"Erro ao limpar dados: {e}")
            return self.df
    
    def _convert_price(self, price_str):
        """Converte string de preço para float"""
        if not price_str or price_str == 'Não informado':
            return 0.0
        try:
            clean_str = re.sub(r'[^\d,]', '', price_str).replace(',', '.')
            return float(clean_str)
        except:
            return 0.0
    
    def _extract_condominio_iptu(self, text):
        if not text or text == 'Não informado':
            return pd.Series([0, 0])
        
        cond = iptu = 0
        try:
            matches = re.findall(r'R\$ (\d+)', text)
            if len(matches) >= 1:
                cond = float(matches[0])
            if len(matches) >= 2:
                iptu = float(matches[1])
        except:
            pass
            
        return pd.Series([cond, iptu])

    def filter_high_value(self, min_price=500000):
        return self.df[self.df['preco_num'] > min_price].copy() if not self.df.empty else pd.DataFrame()