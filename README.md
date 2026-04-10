# LaunchGuard-AI-Multi-Agent-Product-Decision-System
## SETUP INSTRUCTIONS
### 1. clone the repository
```git clone https://github.com/acrobyte007/LaunchGuard-AI-Multi-Agent-Product-Decision-System
```
### 2. create a virtual environment and activate it
```python -m venv venv
```
### 3.install requirements
```pip install -r requirements.txt
```
### 4. create a .env file with the following variables

```
MISTRAL_API_KEY=mistral_api_key
```
### 5. run the main.py file from the root directory
```python main.py
```
### 6.An output folder will be created in the root directory containing the results of the analysis
There will 5 json files containing the results of the analysis for each agent
final_decision.json contains the final decision of the system
