from .models import PopularityRecommender, PersonalizedRecommender
from app.models.user import User

popularity_model = None
personalized_model = None

def initialize_models():
    global popularity_model, personalized_model
    if popularity_model is None:
        popularity_model = PopularityRecommender().fit()
    if personalized_model is None:
        personalized_model = PersonalizedRecommender().fit()
def get_recommendations(n=10):
    initialize_models()
    recommendations_df = popularity_model.recommend(n_recommendations=n)
    recommendtions = []
    for _, row in recommendations_df.iterrows():
        recommendtions.append({
            "id": int(row['id']),
            "nombre": row['nombre'],
            "categoria": row['categoria'],
            "precio": float(row['precio']),
            "popularidad": int(row['cant_ventas'])
        })
    return recommendtions
def get_personalized_recommendations(username, n=10):
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