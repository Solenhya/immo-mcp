
from src import dataAccess
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
import joblib
import pathlib
import pandas as pd

def train_model(model_name):
    df = dataAccess.prepare_features(dataAccess.get_data())
    X = df[dataAccess.features]
    y = df[dataAccess.target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print('entrainement du modèle')

    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = ['Type_local']  # Colonne catégorielle
    print('features ok')

    numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())])
    print('numeric_transformer ok')

    categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    print('categorical_transformer ok')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', regressor),
])    
    print('debut entrainement du modele')

    # Exécuter la recherche sur les données d'entraînement
    model.fit(X_train, y_train)
    print('model trained')
    #grid_search.fit(dtrain)

    y_pred = model.predict(X_test)
    print('prediction ok')

    # Calcule le score R²
    r2 = r2_score(y_test, y_pred)
    print('r2 ok')
    print(f"{r2=:.3f}")

    pathlib.Path("models").mkdir(exist_ok=True)

    file_path = "models/" + model_name + ".joblib"
    joblib.dump(model, file_path)
    print('model saved')

    return model



class PredictionModel:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
    
    def predict(self, features: dict) -> float:
        input_df = pd.DataFrame([features], columns=dataAccess.features)
        prediction = self.model.predict(input_df)[0]
        return prediction


if __name__ == "__main__":
    train_model("model")


    

    


        