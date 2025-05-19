# Stock_Analysis.py
# Script para análisis de acciones e ingresos de Tesla y GameStop

import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Función para guardar capturas de pantalla (simulada, requiere navegador para exportar)
def save_screenshot(fig, filename):
    # Guardar gráfico como HTML y PNG
    fig.write_html(f"screenshots/{filename}.html")
    # Nota: Para guardar como PNG, necesitas kaleido: pip install kaleido
    try:
        fig.write_image(f"screenshots/{filename}.png")
    except Exception as e:
        print(f"No se pudo guardar {filename}.png: {e}. HTML guardado en su lugar.")

# Pregunta 1: Extracción de datos de acciones de Tesla utilizando yfinance
def get_tesla_stock_data():
    tesla = yf.Ticker("TSLA")
    tesla_data = tesla.history(period="max")
    tesla_data.reset_index(inplace=True)
    tesla_data = tesla_data[['Date', 'Close']]
    tesla_data['Date'] = pd.to_datetime(tesla_data['Date'])
    return tesla_data

# Pregunta 2: Extracción de datos de ingresos de Tesla utilizando Webscraping
def get_tesla_revenue():
    url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all('table', class_='historical_data_table')
    revenue_table = tables[1]  # Tabla de ingresos trimestrales
    rows = revenue_table.find_all('tr')[1:]
    
    dates = []
    revenues = []
    
    for row in rows:
        cols = row.find_all('td')
        date = cols[0].text.strip()
        revenue = cols[1].text.strip().replace('$', '').replace(',', '')
        try:
            revenue = float(revenue)
            dates.append(date)
            revenues.append(revenue)
        except ValueError:
            continue
    
    tesla_revenue = pd.DataFrame({'Date': dates, 'Revenue': revenues})
    tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])
    return tesla_revenue

# Pregunta 3: Extracción de datos de acciones de GameStop utilizando yfinance
def get_gamestop_stock_data():
    gamestop = yf.Ticker("GME")
    gme_data = gamestop.history(period="max")
    gme_data.reset_index(inplace=True)
    gme_data = gme_data[['Date', 'Close']]
    gme_data['Date'] = pd.to_datetime(gme_data['Date'])
    return gme_data

# Pregunta 4: Extracción de datos de ingresos de GameStop utilizando Webscraping
def get_gamestop_revenue():
    url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all('table', class_='historical_data_table')
    revenue_table = tables[1]  # Tabla de ingresos trimestrales
    rows = revenue_table.find_all('tr')[1:]
    
    dates = []
    revenues = []
    
    for row in rows:
        cols = row.find_all('td')
        date = cols[0].text.strip()
        revenue = cols[1].text.strip().replace('$', '').replace(',', '')
        try:
            revenue = float(revenue)
            dates.append(date)
            revenues.append(revenue)
        except ValueError:
            continue
    
    gme_revenue = pd.DataFrame({'Date': dates, 'Revenue': revenues})
    gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])
    return gme_revenue

# Pregunta 5 y 6: Función make_graph para graficar acciones e ingresos
def make_graph(stock_data, revenue_data, title, company):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name="Precio de Acción (USD)", line=dict(color='blue' if company == "Tesla" else 'red')),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=revenue_data['Date'], y=revenue_data['Revenue'], name="Ingresos (Millones USD)", line=dict(color='green' if company == "Tesla" else 'purple')),
        secondary_y=True,
    )
    
    fig.update_layout(
        title_text=title,
        xaxis_title="Fecha",
        legend_title="Métricas",
    )
    
    fig.update_yaxes(title_text="Precio de Acción (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Ingresos (Millones USD)", secondary_y=True)
    
    fig.show()
    save_screenshot(fig, f"{company.lower()}_dashboard")

# Pregunta 7: Ejecutar el análisis y generar resultados
def main():
    # Crear directorio para capturas si no existe
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    # Pregunta 1: Obtener y mostrar datos de Tesla
    print("Extrayendo datos de acciones de Tesla...")
    tesla_data = get_tesla_stock_data()
    print("\nPrimeras cinco filas de tesla_data:")
    print(tesla_data.head())
    tesla_data.to_csv("screenshots/tesla_stock.csv", index=False)
    
    # Pregunta 2: Obtener y mostrar ingresos de Tesla
    print("\nExtrayendo datos de ingresos de Tesla...")
    tesla_revenue = get_tesla_revenue()
    print("\nÚltimas cinco filas de tesla_revenue:")
    print(tesla_revenue.tail())
    tesla_revenue.to_csv("screenshots/tesla_revenue.csv", index=False)
    
    # Pregunta 3: Obtener y mostrar datos de GameStop
    print("\nExtrayendo datos de acciones de GameStop...")
    gme_data = get_gamestop_stock_data()
    print("\nPrimeras cinco filas de gme_data:")
    print(gme_data.head())
    gme_data.to_csv("screenshots/gamestop_stock.csv", index=False)
    
    # Pregunta 4: Obtener y mostrar ingresos de GameStop
    print("\nExtrayendo datos de ingresos de GameStop...")
    gme_revenue = get_gamestop_revenue()
    print("\nÚltimas cinco filas de gme_revenue:")
    print(gme_revenue.tail())
    gme_revenue.to_csv("screenshots/gamestop_revenue.csv", index=False)
    
    # Pregunta 5: Dashboard de Tesla
    print("\nGenerando dashboard de Tesla...")
    make_graph(tesla_data, tesla_revenue, "Tesla: Precio de Acción vs Ingresos", "Tesla")
    
    # Pregunta 6: Dashboard de GameStop
    print("\nGenerando dashboard de GameStop...")
    make_graph(gme_data, gme_revenue, "GameStop: Precio de Acción vs Ingresos", "GameStop")
    
    print("\nAnálisis completado. Revisa la carpeta 'screenshots' para los resultados.")

if __name__ == "__main__":
    main()