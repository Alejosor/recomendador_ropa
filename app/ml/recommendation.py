from .models import PopularityRecommender, PersonalizedRecommender
from app.models.user import User
import logging

# Configura el logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('recommendations.log'), logging.StreamHandler()]
)
logger = logging.getLogger('recommendation_system')

popularity_model = None
personalized_model = None

def initialize_models():
    global popularity_model, personalized_model
    if popularity_model is None:
        popularity_model = PopularityRecommender().fit()
    if personalized_model is None:
        personalized_model = PersonalizedRecommender().fit()
def get_recommendations(n=30, debug=False):
    if debug:
        recommendations_df = debug_popularity_recommendations(n)
    else:
        initialize_models()
        recommendations_df = popularity_model.recommend(n_recommendations=n)
    
    recommendations = []
    for _, row in recommendations_df.iterrows():
        recommendations.append({
            "id": int(row['id']),
            "nombre": row['nombre'],
            "categoria": row['categoria'],
            "precio": float(row['precio']),
            "popularidad": int(row['cant_ventas'])
        })
    return recommendations
def get_personalized_recommendations(username, n=30, debug=False):
    if debug:
        recommendations_df = debug_personalized_recommendations(username, n)
    else:
        initialize_models()
        user = User.query.filter_by(nombre=username).first()
        if not user:
            return get_recommendations(n)
        recommendations_df = personalized_model.recommend_for_user(user.id, n_recommendations=n)
    
    recommendations = []
    for _, row in recommendations_df.iterrows():
        recommendations.append({
            "id": int(row['id']),
            "nombre": row['nombre'],
            "categoria": row['categoria'],
            "precio": float(row['precio']),
            "popularidad": int(row['cant_ventas'])
        })
    return recommendations

def debug_popularity_recommendations(n=20):
    """Función para depurar las recomendaciones basadas en popularidad."""
    initialize_models()
    
    # Obtener todos los productos y ordenarlos por ventas para verificar
    all_products = popularity_model.products_df.sort_values(
        by='cant_ventas', ascending=False
    )
    
    logger.debug(f"TOP 10 PRODUCTOS POR VENTAS:")
    for i, (_, row) in enumerate(all_products.head(10).iterrows()):
        logger.debug(f"{i+1}. {row['nombre']} - {row['categoria']} - Ventas: {row['cant_ventas']}")
    
    # Obtener las recomendaciones reales
    recommendations_df = popularity_model.recommend(n_recommendations=n)
    
    logger.debug(f"\nRECOMENDACIONES REALES (TOP 10):")
    for i, (_, row) in enumerate(recommendations_df.head(10).iterrows()):
        logger.debug(f"{i+1}. {row['nombre']} - {row['categoria']} - Ventas: {row['cant_ventas']}")
    
    return recommendations_df

def debug_personalized_recommendations(username, n=10):
    """Función para depurar las recomendaciones personalizadas."""
    initialize_models()
    
    user = User.query.filter_by(nombre=username).first()
    if not user:
        logger.warning(f"Usuario '{username}' no encontrado")
        return get_recommendations(n)
    
    logger.debug(f"Depurando recomendaciones para usuario: {username} (ID: {user.id})")
    
    # Analizar historial de compras
    from .data_loader import get_user_purchase_history
    user_history = get_user_purchase_history(user.id)
    
    if user_history.empty:
        logger.warning(f"El usuario {username} no tiene historial de compras")
    else:
        # Contar productos comprados por categoría
        from .data_loader import get_products_data
        all_products = get_products_data()
        
        purchased_products = []
        for pid in user_history['id_product'].unique():
            product = all_products[all_products['id'] == pid]
            if not product.empty:
                purchased_products.append({
                    'id': int(pid),
                    'nombre': product['nombre'].values[0],
                    'categoria': product['categoria'].values[0],
                    'cant': user_history[user_history['id_product'] == pid]['cant'].sum()
                })
        
        logger.debug(f"HISTORIAL DE COMPRAS:")
        for i, item in enumerate(purchased_products):
            logger.debug(f"{i+1}. {item['nombre']} ({item['categoria']}) - Cantidad: {item['cant']}")
    
    # Obtener y mostrar recomendaciones
    recommendations_df = personalized_model.recommend_for_user(user.id, n_recommendations=n)
    
    logger.debug(f"\nRECOMENDACIONES PERSONALIZADAS:")
    for i, (_, row) in enumerate(recommendations_df.head(10).iterrows()):
        # Si existe la columna similarity_score, mostrarla
        if 'similarity_score' in row:
            logger.debug(f"{i+1}. {row['nombre']} - {row['categoria']} - "
                        f"Similitud: {row['similarity_score']:.2f} - Ventas: {row['cant_ventas']}")
        else:
            logger.debug(f"{i+1}. {row['nombre']} - {row['categoria']} - Ventas: {row['cant_ventas']}")
    
    return recommendations_df
