# SalesForce AI – Topic 7
## AI in Sales Performance Management

### Included files
- app.py – interactive Streamlit application
- requirements.txt – required Python libraries
- sample_sales_data.csv – five illustrative sales executive records
- README.md – installation and usage instructions

### Run on a Windows laptop
1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. During installation, select **Add Python to PATH**.
3. Extract this ZIP folder.
4. Open the extracted `SalesForceAI_Topic7` folder.
5. Click the folder address bar, type `cmd`, and press Enter.
6. Install the libraries:
   `python -m pip install -r requirements.txt`
7. Start the application:
   `python -m streamlit run app.py`
8. It opens in a browser, usually at http://localhost:8501.

### Required columns for uploaded CSV/Excel
Executive, Territory, Target, Actual_Sales, Total_Calls, Productive_Calls, Planned_Outlets, Outlets_Visited, Orders, Previous_Sales, Variable_Cost, Territory_Expenses

Use numeric values only in numeric columns (no ₹ symbol or comma separators).

### Academic note
The included data is synthetic and only for demonstration. Incentive slabs and score weights are illustrative assumptions, not actual company policy. This version uses transparent rule-based scoring and coaching recommendations; it is not a trained AI/ML model. A genuine predictive model requires historical records, a defined outcome, time-based validation and model evaluation.
