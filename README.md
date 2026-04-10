#  LaunchGuard AI – Multi-Agent Product Decision System

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/acrobyte007/LaunchGuard-AI-Multi-Agent-Product-Decision-System
cd LaunchGuard-AI-Multi-Agent-Product-Decision-System
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
```

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment Variables File

Create a `.env` file in the root directory and add:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 5. Run the Application
```bash
python main.py
```

### 6. Output

After execution:
- An `output/` folder will be created in the root directory.
- It will contain:
  - **5 JSON files** → Individual agent analysis results
  - **`final_decision.json`** → Final aggregated decision of the system

---

## Notes
- Ensure your API key is valid before running the system.
- The output files provide detailed insights from each agent as well as the final recommendation.