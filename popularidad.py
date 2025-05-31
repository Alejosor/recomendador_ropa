import pandas as pd

def obtener_top_productos(n=5):
    df = pd.read_csv('productos.csv')
    df_ordenado = df.sort_values(by='ventas', ascending=False)
    return df_ordenado.head(n).to_dict(orient='records')

def obtener_producto_por_id(producto_id):
    df = pd.read_csv('productos.csv')
    producto = df[df['id'] == int(producto_id)]
    if not producto.empty:
        return producto.iloc[0].to_dict()
    return None
