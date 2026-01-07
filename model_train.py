import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pickle

def train_model():
    print("Loading dataset...")
    # Load the dataset
    try:
        data = pd.read_csv('Housing.csv')
    except FileNotFoundError:
        print("Error: Housing.csv not found.")
        return

    # User Input requirements: Area, Number of bedrooms, Number of bathrooms
    # Selecting only these features for the model
    features = ['area', 'bedrooms', 'bathrooms']
    target = 'price'

    print(f"Selected features: {features}")
    
    # Check if columns exist
    if not all(col in data.columns for col in features + [target]):
        print(f"Error: Dataset missing required columns. Available columns: {data.columns}")
        return

    X = data[features]
    y = data[target]

    # Data Preprocessing
    # 1. Handle missing values (Simple imputation with mean, though Housing.csv is usually clean)
    if X.isnull().sum().any():
        print("Handling missing values...")
        X = X.fillna(X.mean())

    # 2. Split dataset
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Train Model
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 4. Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("----------------------------")
    print(f"Model Performance:")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.2f}")
    print("----------------------------")

    # 5. Save Model
    print("Saving model to model.pkl...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Done.")

if __name__ == "__main__":
    train_model()
