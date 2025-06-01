import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from .data_loader import get_products_data, get_sales_data, get_sales_details_data, get_user_purchase_history, get_product_categories

class PopularityRecommender:
    def __init__(self):
        self.products_df = None
        self.is_fitted = False
    def fit(self):
        self.products_df = get_products_data()
        self.is_fitted = True
        return self
    def recommend(self, n_recommendations=15):
        if not self.is_fitted:
            self.fit()
        recommend = self.products_df.sort_values(
            by='cant_ventas', ascending=False
        )
        return recommend.head(n_recommendations)
class PersonalizedRecommender:
    def __init__(self):
        self.products_df = None
        self.user_item_matrix = None
        self.product_similarity = None
        self.is_fitted = False
        self.popularity_recommender = PopularityRecommender()
    def fit(self):
        self.products_df = get_products_data()
        sales_df = get_sales_data()
        sales_details_df = get_sales_details_data()
        if len(sales_df) < 5 or len(sales_details_df) < 5:
            self.popularity_recommender.fit()
            self.is_fitted = True
            return self
        merged_data = sales_details_df.merge(sales_df, left_on='id_venta', right_on='id')
        user_product_data = merged_data[['id_user', 'id_product', 'cant']]
        try:
            self.user_item_matrix = user_product_data.pivot_table(
                index='id_user', 
                columns='id_product', 
                values='cant',
                aggfunc='sum',
                fill_value=0
            )
        except:
            self.popularity_recommender.fit()
            self.is_fitted = True
            return self
        self.calculate_product_similarity()
        self.is_fitted = True
        self.popularity_recommender.fit()
        return self
    def calculate_product_similarity(self):
        try:
            # Obtener categorías de productos
            categories_dict = get_product_categories()
            
            # Crear arrays para almacenar IDs y categorías
            product_ids = []
            product_features = []
            
            # Asegurarnos que cada producto tenga un ID y una categoría
            for product_id in self.products_df['id'].values:
                product_ids.append(product_id)
                category = categories_dict.get(product_id, 'unknown')
                product_features.append([category])
                
            # Convertir categorías a vectores numéricos
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoded_features = encoder.fit_transform(product_features)
            
            # Guardar IDs de productos para referencia
            self.product_ids = np.array(product_ids)
            
            # Calcular similitud del coseno entre productos
            self.product_similarity = cosine_similarity(encoded_features)
            
        except Exception as e:
            self.product_similarity = None
    def recommend_for_user(self, user_id, n_recommendations=10):
        if not self.is_fitted:
            self.fit()
        user_history = get_user_purchase_history(user_id)
        if user_history.empty:
            return self.popularity_recommender.recommend(n_recommendations)
        purchased_products = user_history['id_product'].unique()
        if self.product_similarity is None:
            return self.popularity_recommender.recommend(n_recommendations)
        similar_products_scores = {}
        
        for purchased_id in purchased_products:
            try:
                # Encontrar índice del producto en nuestra matriz
                idx = np.where(self.product_ids == purchased_id)[0]
                if len(idx) == 0:
                    continue
                idx = idx[0]
                
                # Recorrer todos los productos
                for i, product_id in enumerate(self.product_ids):
                    if product_id not in similar_products_scores:
                        similar_products_scores[product_id] = 0
                    
                    # Sumar puntaje de similitud
                    similar_products_scores[product_id] += self.product_similarity[idx, i]
                    
            except Exception as e:
                logger.error(f"Error al procesar producto {purchased_id}: {e}")
                continue
        
        similar_df = pd.DataFrame({
            'id_product': list(similar_products_scores.keys()),
            'similarity_score': list(similar_products_scores.values())
        })
        result = similar_df.merge(self.products_df, left_on='id_product', right_on='id')
        result = result.sort_values(by=['similarity_score', 'cant_ventas'], ascending=[False, False])
        result = result[~result["id"].isin(purchased_products)]
        if len(result) < n_recommendations:
            pop_recs = self.popularity_recommender.recommend(n_recommendations)
            pop_recs = pop_recs[~pop_recs["id"].isin(result['id'])]
            result = pd.concat([result, pop_recs]).head(n_recommendations)
        return result.head(n_recommendations)