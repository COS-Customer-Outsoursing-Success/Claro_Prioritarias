
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# === 1. Cargar datos ===
df = pd.read_csv(r"C:\Users\Emerson.Aguilar\Documents\git_hub\Pruebas DataMining\datos_sociodemograficos.csv")  # Ajusta la ruta si es necesario

# === 2. Separar variables ===
X = df.drop("efectividad", axis=1)
y = df["efectividad"]

# Columnas categóricas y numéricas
categorical_cols = ["genero", "nivel_educativo", "ciudad"]
numeric_cols = ["edad", "estrato"]

# === 3. Preprocesamiento ===
preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(drop="first", sparse_output=False), categorical_cols)
], remainder="passthrough")

# === 4. Pipeline con Random Forest ===
model = RandomForestClassifier(n_estimators=100, random_state=42)

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", model)
])

# === 5. Split de datos ===
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# === 6. Entrenar modelo ===
pipeline.fit(X_train, y_train)

# === 7. Métricas ===
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

# Mostrar métricas
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("AUC:", round(auc, 4))

# === 8. Gráfico de métricas ===
metricas = {
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "AUC": auc
}

plt.figure(figsize=(8, 5))
bars = plt.bar(metricas.keys(), metricas.values(), color='skyblue')
plt.ylim(0, 1)
plt.title("Métricas del Modelo")
plt.ylabel("Valor")

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f"{yval:.2f}", ha='center')

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# === 9. Importancia de variables ===
# Recuperar columnas codificadas
ohe = pipeline.named_steps["preprocessing"].transformers_[0][1]
ohe_features = ohe.get_feature_names_out(categorical_cols)
all_features = list(ohe_features) + numeric_cols

# Importancia
importancias = pipeline.named_steps["classifier"].feature_importances_

# Crear dataframe y graficar
df_importancia = pd.DataFrame({
    "Variable": all_features,
    "Importancia": importancias
}).sort_values(by="Importancia", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(df_importancia["Variable"], df_importancia["Importancia"], color="lightgreen")
plt.title("Importancia de Variables")
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
