from ZapImoveisScraper import ZapImoveisScraper

if __name__ == "__main__":    
    locais = [
        "sp+sao-paulo+zona-oeste+pinheiros"
    ]
    
    scraper = ZapImoveisScraper()
    
    for local in locais:
        df = scraper.scrape_location(local)
        
        if df is not None and not df.empty:
            nome_arquivo = f"imoveis_{local.replace('+', '_')}.csv"
            df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
            print(f"\nDados salvos em {nome_arquivo}")
        else:
            print(f"\nNenhum dado válido foi obtido para {local}")