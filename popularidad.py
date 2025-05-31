import pandas as pd

def obtener_top_productos(n=5):
    df = pd.read_csv('productos.csv')
    df_ordenado = df.sort_values(by='ventas', ascending=False)
    return df_ordenado.head(n).to_dict(orient='records')
