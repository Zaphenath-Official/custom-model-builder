import sys
import requests
import os
import requests
import tkinter as tk
from tkinter import filedialog

BASE_URL = "http://127.0.0.1:5000"
session_state = {"user_id": None, "token": None}

def main_menu():
    print("\n=== 🚗 CUSTOM AUTOMATED ML PROTO ENGINE CLI ===")
    print("1. Create New Account (Register)")
    print("2. Log In to Session")
    print("3. Profile CSV Layout & Train Automated Model Arena")
    print("4. View All My Trained Models & API Keys")
    print("5. Run Live Prediction on a Trained Model")
    print("6. Exit Engine")
    choice = input("Select operation code (1-6): ").strip()
    
    if choice == "1": register()
    elif choice == "2": login()
    elif choice == "3": train_model()
    elif choice == "4": list_my_models()
    elif choice == "5": run_live_prediction()
    elif choice == "6": sys.exit("Terminating diagnostic session tracker.")
    else: print("Invalid choice configuration option selected.")

def register():
    email = input("Enter registration email: ").strip()
    password = input("Enter password: ").strip()
    res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    print(res.text)

def login():
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if res.status_code == 200:
        data = res.json()
        session_state["user_id"] = data["user_id"]
        session_state["token"] = data["access_token"]
        print(f"\n✅ Session authenticated! Welcome back.")
    else:
        print(f"Authentication failed: {res.text}")

def train_model():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return
    file_path = input("Enter data file path (e.g., C:/data/insurance.csv): ").strip()
    model_name = input("Assign a unique name to this model deployment: ").strip()
    target = input("Input exact target column (e.g., charges): ").strip()
    features_list = input("Input space-separated features list (e.g., age bmi smoker): ").strip().split()

    try:
        with open(file_path, 'rb') as f:
            payload_files = {'file': f}
            payload_form = {
                'user_id': session_state["user_id"],
                'model_name': model_name,
                'targets': [target],
                'features': features_list
            }
            print("⚡ Transmission streaming sequence engaged... Training tournament live...")
            res = requests.post(f"{BASE_URL}/targets-features-train", files=payload_files, data=payload_form)
            print(res.text)
    except Exception as e:
        print(f"Error opening file: {e}")

def list_my_models():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return
    
    # 1. Fetch the array from your backend server
    res = requests.get(f"{BASE_URL}/developer/models", params={"user_id": session_state["user_id"]})
    
    if res.status_code == 200:
        data = res.json()
        print("\n📊 --- YOUR TRAINED CUSTOM ENGINES ---")
        
        # 2. Store the array of models in a cache list
        models_cache = data["models"] 
        
        for idx, model in enumerate(models_cache):
            download_status_tag = "✅ [ALREADY DOWNLOADED]" if model['has_been_downloaded'] else "🆕 [NOT YET DOWNLOADED]"
            print(f"\n[{idx + 1}] Model Name: {model['model_name'].upper()} (Version: v{model['model_version']})")
            print(f"    Status: {download_status_tag}")
            print(f"    Database ID Ref: {model['id']}")
            print(f"    🔑 API Key: {model['api_key']}")
            
        print("\n------------------------------------")
        action = input("Do you want to download one of these models locally? (y/n): ").strip().lower()
        
        if action == 'y':
            # 3. Convert user input string (e.g. "1") into an integer list index (0)
            item_num = int(input("Enter index number integer choice to pull down: ").strip()) - 1
            
            # 4. Check if the index is valid within our cache array bounds
            if 0 <= item_num < len(models_cache):
                
                # 🚨 HERE IS WHERE IT PASSES: 
                # We extract the single model dictionary and pass it straight down!
                target_model = models_cache[item_num]
                download_model_action(model_metadata=target_model)
                
            else:
                print("Invalid list selection index choice.")
    else:
        print(f"Could not retrieve model list: {res.text}")


def download_model_action(model_metadata):
    model_id = model_metadata["id"]
    suggested_name = f"{model_metadata['model_name'].replace(' ', '_')}_v{model_metadata['model_version']}.joblib"
    
    if model_metadata['has_been_downloaded']:
        print(f"\n⚠️ Note: You have already downloaded this specific model file previously ({suggested_name}).")
        confirm = input("Are you sure you want to download it again? (y/n): ").strip().lower()
        if confirm != 'y':
            return

    print(f"\n📥 Fetching file streaming response channel...")
    res = requests.get(f"{BASE_URL}/developer/models/download/{model_id}")
    
    if res.status_code == 200:
        # 🚨 THE DESKTOP SAVE-AS FIX:
        # 1. Hide the ugly root Tkinter blank window box from popping up
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True) # Bring the dialog box to the absolute front of the screen
        
        print("🖥️  Opening native file manager window... Please select your destination path.")
        
        # 2. Trigger the OS file explorer layout grid
        selected_file_path = filedialog.asksaveasfilename(
            initialfile=suggested_name,
            defaultextension=".joblib",
            filetypes=[("Joblib Serialized Objects", "*.joblib"), ("All Files", "*.*")],
            title="Choose Local Destination Directory to Store Model"
        )
        
        # 3. Check if the user didn't hit cancel
        if selected_file_path:
            with open(selected_file_path, 'wb') as f:
                f.write(res.content)
            print(f"🎉 Success! Binary artifact package saved locally to disk at:\n   '{selected_file_path}'")
        else:
            print("❌ Download aborted: No destination directory was selected by the user.")
            
        root.destroy() # Completely clean up memory references to window process
    else:
        print(f"Download stream error response context: {res.text}")


def run_live_prediction():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return

    # 1. Fetch user's models so they can pick one
    print("\n📡 Fetching available deployed models...")
    res = requests.get(f"{BASE_URL}/developer/models", params={"user_id": session_state["user_id"]})
    
    if res.status_code != 200:
        print(f"❌ Failed to retrieve models: {res.text}")
        return

    models_cache = res.json()["models"]
    if not models_cache:
        print("⚠️ You don't have any trained models yet. Train a model using Option 3 first.")
        return

    # 2. Display selection list
    print("\n🤖 Select a model to run inference against:")
    for idx, model in enumerate(models_cache):
        print(f"[{idx + 1}] {model['model_name'].upper()} (Version: v{model['model_version']})")

    try:
        selection = int(input("\nEnter selection number: ").strip()) - 1
        if not (0 <= selection < len(models_cache)):
            print("Invalid index choice.")
            return
    except ValueError:
        print("Please enter a valid integer.")
        return

    selected_model = models_cache[selection]
    api_key = selected_model["api_key"]

    # 3. Request a dynamic feature payload from the user
    print(f"\n🧠 Preparing input payload structure for model: {selected_model['model_name'].upper()}")
    print("Please provide the custom data values for inference when prompted.")
    
    payload = {}
    
    # We ask the user to type in comma-separated values or prompt based on known features
    # Since we know the schema structure of our models, let's ask the user to provide 
    # values for the typical tabular features.
    
    # Let's prompt for features based on the column dataset we are currently experimenting with
    features_input = input("\nEnter space-separated features you want to input values for (e.g., age sex bmi smoker): ").strip().split()
    
    if not features_input:
        print("❌ Feature list cannot be empty.")
        return

    for feature in features_input:
        val = input(f"   Enter value for [{feature}]: ").strip()
        
        # Smart casting helper: convert to numeric if possible, otherwise keep as string
        if val.replace('.', '', 1).isdigit():
            payload[feature] = float(val) if '.' in val else int(val)
        else:
            payload[feature] = val

    # 4. Transmit secure prediction request to the server gateway
    print("\n⚡ Transmitting inference payload over secure API gateway...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/predict", json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("\n🎯 --- INFERENCE SUCCESSFUL ---")
            print(f"    Model Used: {result['model_name']}")
            print(f"    Predicted Value Output: {result['prediction']}")
            print("--------------------------------")
        else:
            print(f"\n❌ API Gateway Rejected Request ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ Network dispatch error: {str(e)}")

if __name__ == "__main__":
    while True:
        main_menu()