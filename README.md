# 🚌 School Bus Routing Optimization using Streamlit, OR-Tools & Optuna

This project aims to optimize school bus routes to minimize transportation costs and improve student safety. It uses Google's OR-Tools to solve the Vehicle Routing Problem (VRP) and Optuna for hyperparameter tuning. A simple web interface is provided using Streamlit.

---

## 🚀 Features

- Optimize school bus routes based on total travel distance
- Adjustable parameters: number of buses, capacity, optimization trials
- Real-time web interface using Streamlit
- Location data based on Chennai, India
- Uses OR-Tools for route solving and Optuna for tuning

---

## 🛠 Technologies Used

- **Python 3.x**
- **Streamlit** - for web UI
- **OR-Tools** - for Vehicle Routing Problem (VRP)
- **Optuna** - for optimization trials (hyperparameter tuning)
- **NumPy**, **Pandas**, **FPDF** - utilities for data and export

---

## 🧪 Optimization Techniques

- **Google OR-Tools**:
  - Solves the VRP using local search methods like Tabu Search and Guided Local Search
- **Optuna**:
  - Hyperparameter tuning with Tree-structured Parzen Estimator (TPE)
  - Selects optimal bus counts and capacity to minimize distance

---

## ⚙️ Parameters

You can configure these values using the Streamlit sidebar:

| Parameter             | Range            | Description                              |
|-----------------------|------------------|------------------------------------------|
| Min Buses             | 1 to 5           | Minimum number of buses                  |
| Max Buses             | Up to 8          | Maximum number of buses                  |
| Min Capacity          | 40               | Minimum capacity of each bus             |
| Max Capacity          | 60               | Maximum capacity of each bus             |
| Optimization Trials   | 5 to 100         | Number of Optuna trials for optimization |

---
## 🧩 How It Works

1. Define sample student locations on a map
2. Use Euclidean distance to create a distance matrix
3. Optuna runs trials to test different bus counts and capacities
4. OR-Tools solves the VRP with capacity constraints
5. Return the configuration with the least total distance

---

## 📂 Run Locally

```bash
git clone https://github.com/yourusername/school-bus-routing-opt.git
cd school-bus-routing-opt
pip install -r requirements.txt
streamlit run app.py
