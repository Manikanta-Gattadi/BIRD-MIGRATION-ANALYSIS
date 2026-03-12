# Importing necessary modules and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
sns.set_style("whitegrid")
# Load the dataset
df = pd.read_csv('bird_tracking.csv')

# 1. Handle Missing Values
print(f"Missing values before drop:\n{df.isnull().sum()}")
df = df.dropna()

# 2. Handle Duplicates
df = df.drop_duplicates()

# 3. Prevent Data Leakage
# We drop 'device_info' because it is a unique ID for each bird.
# Identifying a bird by its tag ID is cheating; we want to identify it by its flight behavior.
if 'device_info' in df.columns:
    df = df.drop(columns=['device_info'])

# 4. Feature Extraction (Date & Time)
# Convert string date to datetime object
df['date_time'] = pd.to_datetime(df['date_time'])
# Extract numerical features
df['month'] = df['date_time'].dt.month
df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek
# Drop the original timestamp column
df = df.drop(columns=['date_time'])

# 5. Encode Target Variable
le = LabelEncoder()
df['bird_name_encoded'] = le.fit_transform(df['bird_name'])

print("\nData Cleaned and Preprocessed.")
print(df.head())
# Select only numerical columns for correlation
numeric_df = df.select_dtypes(include=[np.number])

# Compute correlation matrix
corr_matrix = numeric_df.corr()

# Plot Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Feature Correlation Matrix')
plt.show()
print("\nCorrelation with Target (bird_name):\n", corr_matrix['bird_name_encoded'].sort_values(ascending=False))
# Define Inputs (X) and Target (y)
feature_cols = ['latitude', 'longitude', 'altitude', 'speed_2d', 'direction', 'month', 'hour', 'day_of_week']
X = df[feature_cols]
y = df['bird_name_encoded']

# Split data: 80% Training, 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale Features (Standardization)
# This is crucial for KNN and Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training Shape:", X_train_scaled.shape)
print("Testing Shape:", X_test_scaled.shape)
# Initialize models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight='balanced'
    ),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB()
}

results = []

print("Training and Evaluating Models...")
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    results.append({'Model': name, 'Accuracy': acc})
    print(f"{name}: {acc * 100:.2f}%")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

results_df = pd.DataFrame(results)

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(
    data=results_df,
    x='Model',
    y='Accuracy',
    hue='Model',
    palette='viridis',
    legend=False
)
plt.title("Model Accuracy Comparison")
plt.ylabel("Accuracy")
plt.xlabel("Model")
plt.tight_layout()
plt.show()
import joblib

# Select the best-performing model (Decision Tree: 98.45%)
best_model = models["Decision Tree"]

# Save the trained model, scaler, and label encoder to disk
joblib.dump(best_model, "bird_model.pkl")
joblib.dump(scaler,     "bird_scaler.pkl")
joblib.dump(le,         "bird_label_encoder.pkl")

print("Saved:")
print("  bird_model.pkl          — trained Decision Tree classifier")
print("  bird_scaler.pkl         — fitted StandardScaler")
print("  bird_label_encoder.pkl  — fitted LabelEncoder (maps numbers -> bird names)")
print()
print("Bird name classes:", list(le.classes_))
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import joblib
from datetime import datetime

# ===============================
# LOAD TRAINED MODEL & SCALER
# (FIX: load the saved .pkl files so predictions are real, not hardcoded)
# ===============================
try:
    model     = joblib.load("bird_model.pkl")
    scaler    = joblib.load("bird_scaler.pkl")
    le        = joblib.load("bird_label_encoder.pkl")
    model_loaded = True
    print("Model loaded successfully. Bird classes:", list(le.classes_))
except FileNotFoundError as e:
    model_loaded = False
    print(f"WARNING: Could not load model files — {e}")
    print("Run the 'Save Best Model' cell above first, then re-run this cell.")

# ===============================
# ROOT WINDOW
# ===============================
root = tk.Tk()
root.title("WINGS IN MOTION")
root.geometry("1100x650")
root.resizable(False, False)
root.update_idletasks()

# Background image
bg_img   = Image.open("bird_gui_2.jpeg")
bg_img   = bg_img.resize((1100, 650))
bg_photo = ImageTk.PhotoImage(bg_img, master=root)
canvas   = tk.Canvas(root, width=1100, height=650, highlightthickness=0)
canvas.pack(fill="both", expand=True)
root.bg_photo = bg_photo
canvas.create_image(0, 0, image=root.bg_photo, anchor="nw")

# ===============================
# VARIABLES
# ===============================
altitude  = tk.DoubleVar()
latitude  = tk.DoubleVar()
longitude = tk.DoubleVar()
speed     = tk.DoubleVar()

# ===============================
# MAIN BLUE PANEL
# ===============================
main_frame = tk.Frame(root, bg="#2e4053")
main_frame.place(relx=0.5, rely=0.47, anchor="center",
                 width=560, height=330)

for i in range(2):
    main_frame.columnconfigure(i, weight=1)

# Title
tk.Label(
    main_frame,
    text="WINGS IN MOTION",
    font=("Segoe UI", 16, "bold"),
    fg="white",
    bg="#2e4053"
).grid(row=0, column=0, columnspan=2, pady=(15, 10))

# Input fields & ranges
fields = [
    ("Altitude (m):",  altitude,  "(-1010  \u2013  6965 m)"),
    ("Latitude:",      latitude,  "(12.35  \u2013  51.52)"),
    ("Longitude:",     longitude, "(-17.63  \u2013  4.86)"),
    ("Speed (m/s):",   speed,     "(0.0  \u2013  63.5)"),
]

for i, (label_text, var, range_text) in enumerate(fields, start=1):
    row_frame = tk.Frame(main_frame, bg="#2e4053")
    row_frame.grid(row=i, column=0, columnspan=2, sticky="ew", padx=20, pady=8)

    tk.Label(
        row_frame, text=label_text,
        bg="#2e4053", fg="white",
        font=("Segoe UI", 11), width=14, anchor="e"
    ).pack(side="left")

    tk.Label(
        row_frame, text=range_text,
        bg="#2e4053", fg="#bdc3c7",
        font=("Segoe UI", 10, "italic")
    ).pack(side="left", padx=(8, 0))

    tk.Entry(
        row_frame, textvariable=var,
        width=22, font=("Segoe UI", 11), justify="left"
    ).pack(side="right")

# ===============================
# RESULT FRAME
# ===============================
result_frame = tk.LabelFrame(
    root,
    text=" Prediction Result ",
    bg="#1abc9c", fg="black",
    font=("Segoe UI", 11, "bold")
)
result_frame.place(relx=0.5, rely=0.85, anchor="center",
                   width=680, height=100)

result_label = tk.Label(
    result_frame,
    text="Result will appear here",
    bg="#ecf0f1", fg="black",
    font=("Segoe UI", 12),
    justify="center"
)
result_label.pack(expand=True, fill="both", padx=15, pady=12)


# ===============================
# FIXED PREDICT FUNCTION
# ===============================
def predict_bird():
    """
    FIX APPLIED HERE:
    Previously this function contained a hardcoded static response:
        result_label.config(text="Bird Behavior: Migratory\nPrediction Confidence: 87%")

    Now it:
      1. Reads the user's numeric inputs
      2. Assembles the 8-feature vector the model was trained on
         (month/hour/day_of_week are auto-filled from the current datetime;
          direction defaults to 0 as it is not collected in the GUI)
      3. Scales the vector with the saved StandardScaler
      4. Calls model.predict() to get the actual predicted bird
      5. Decodes the numeric label back to the bird name via LabelEncoder
      6. Calls model.predict_proba() for a real confidence percentage
    """
    if not model_loaded:
        messagebox.showerror(
            "Model Not Found",
            "Could not load 'bird_model.pkl'.\n"
            "Please run the 'Save Best Model' cell first, then restart this cell."
        )
        return

    try:
        alt = altitude.get()
        lat = latitude.get()
        lon = longitude.get()
        spd = speed.get()

        # Optional range warnings
        if not (-1100 <= alt <= 7000):
            messagebox.showwarning("Unusual Value",
                                   "Altitude is outside the typical tracked range (-1010 to 6965 m).")
        if not (12 <= lat <= 52):
            messagebox.showwarning("Unusual Value",
                                   "Latitude seems outside the recorded region (12.35 to 51.52).")
        if not (-18 <= lon <= 5):
            messagebox.showwarning("Unusual Value",
                                   "Longitude seems outside the recorded region (-17.63 to 4.86).")
        if not (0 <= spd <= 65):
            messagebox.showwarning("Unusual Value",
                                   "Speed is outside the typical tracked range (0.0 to 63.5 m/s).")

        # --- Auto-fill time-based features from current datetime ---
        now         = datetime.now()
        month       = now.month        # 1-12
        hour        = now.hour         # 0-23
        day_of_week = now.weekday()    # 0=Monday ... 6=Sunday
        direction   = 0.0              # direction not collected in GUI; use neutral default

        # Build the feature vector in the EXACT same column order used during training:
        # ['latitude', 'longitude', 'altitude', 'speed_2d', 'direction', 'month', 'hour', 'day_of_week']
        feature_vector = np.array([[lat, lon, alt, spd, direction, month, hour, day_of_week]])

        # Scale using the saved StandardScaler
        feature_scaled = scaler.transform(feature_vector)

        # Predict
        pred_encoded = model.predict(feature_scaled)[0]

        # Decode numeric label -> bird name
        bird_name = le.inverse_transform([pred_encoded])[0]

        # Get real confidence via predict_proba (Decision Tree supports this)
        try:
            proba      = model.predict_proba(feature_scaled)[0]
            confidence = proba[pred_encoded] * 100
            result_label.config(
                text=f"Predicted Bird: {bird_name}\nConfidence: {confidence:.1f}%",
                fg="#2c3e50"
            )
        except AttributeError:
            # Fallback if model doesn't support predict_proba
            result_label.config(
                text=f"Predicted Bird: {bird_name}",
                fg="#2c3e50"
            )

    except tk.TclError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numeric values in all fields."
        )
    except Exception as e:
        messagebox.showerror(
            "Prediction Error",
            f"An unexpected error occurred:\n{e}"
        )


def clear_all():
    altitude.set(0.0)
    latitude.set(0.0)
    longitude.set(0.0)
    speed.set(0.0)
    result_label.config(
        text="Result will appear here",
        fg="black"
    )


# ===============================
# BUTTONS
# ===============================
btn_frame = tk.Frame(main_frame, bg="#2e4053")
btn_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky="ew")

tk.Button(
    btn_frame,
    text="Identify Bird",
    bg="#27ae60", fg="white",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=predict_bird,
    relief="flat",
    activebackground="#1e8449"
).pack(side="left", padx=30, expand=True)

tk.Button(
    btn_frame,
    text="Clear",
    bg="#c0392b", fg="white",
    font=("Segoe UI", 11, "bold"),
    width=15,
    command=clear_all,
    relief="flat",
    activebackground="#a93226"
).pack(side="right", padx=30, expand=True)

# ===============================
# START APPLICATION
# ===============================
root.mainloop()
