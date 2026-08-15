# 💸 Cash Flow Minimizer

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![NetworkX](https://img.shields.io/badge/NetworkX-000000?style=flat-square&logo=networkx&logoColor=white)](https://networkx.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=python&logoColor=white)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

*An intelligent, algorithmic cash flow minimization system designed to simplify multi-party debt networks, minimize total transaction count, generate visual debt graph analytics, and dispatch automated PDF settlement reports.*

</div>

---

## 📖 Table of Contents
- [🚀 Overview](#-overview)
- [🌟 Key Features](#-key-features)
- [🗺️ System Architecture](#️-system-architecture)
- [⚙️ How the Algorithms Work](#️-how-the-algorithms-work)
  - [1. Greedy Algorithm](#1-greedy-algorithm)
  - [2. Graph Flow Algorithm (Min-Cost Flow)](#2-graph-flow-algorithm-min-cost-flow)
- [📁 Folder Structure](#-folder-structure)
- [🛠️ Tech Stack & Dependencies](#️-tech-stack--dependencies)
- [📥 Installation & Setup](#-installation--setup)
- [💻 Usage Guide](#-usage-guide)
  - [Option A: Streamlit Web UI (Recommended)](#option-a-streamlit-web-ui-recommended)
  - [Option B: Command Line Interface (CLI)](#option-b-command-line-interface-cli)
- [📄 License & Authors](#-license--authors)

---

## 🚀 Overview

In group trips, shared apartments, or team projects, tracking and settling mutual expenses often leads to an entangled web of bidirectional debts. If Person A owes Person B, Person B owes Person C, and Person C owes Person A, paying each debt individually causes unnecessary banking friction and redundant transactions.

**Cash Flow Minimizer** models the entire group's financial relationships as a directed flow network and calculates the minimum number of transactions required to completely balance all net debts.

> [!NOTE]
> The total net balance of each individual remains invariant—everyone receives or pays their exact required net amount, while reducing the number of money transfers by up to 70-80%.

---

## 🌟 Key Features

- **👥 Group & Member Management**: Quickly register members with names and email addresses.
- **💳 Advanced Expense Logging**: Support for split modes:
  - **Equally**: Divides the total bill equally across participants.
  - **Exact Amounts**: Allows custom, unequal contributions per person.
- **⚙️ Dual Optimization Solvers**:
  - **Greedy Minimizer**: Optimal matching algorithm pairing the largest debtor with the largest creditor iteratively.
  - **Graph Flow Minimizer**: Constructs a flow network and computes the Minimum Cost Flow using **Network Simplex**.
- **📊 Debt Network Visualizations**: Interactive graph plotting (Original Debts vs. Optimized Settlements) rendered with **NetworkX** and **Matplotlib**.
- **📄 PDF Settlement Reports**: Automatically generates structured, professional PDF invoices featuring group summaries, expense logs, and debt settlement tables.
- **📧 Automated Email Dispatcher**: Sends the generated PDF settlement report directly to all group members' inbox via SMTP.

---

## 🗺️ System Architecture

```mermaid
graph TD
    A[Add Group Members] --> B[Log Expense Details]
    B --> C{Choose Split Mode}
    C -->|Equally| D[Compute Equal Share]
    C -->|Exact Amounts| E[Specify Custom Amounts]
    D --> F[Compile Debt Network]
    E --> F
    F --> G{Select Solver}
    G -->|Greedy Algorithm| H[Sort Debtors & Creditors <br/> Settle Greedy Maximums]
    G -->|Graph Flow Algorithm| I[Build Min-Cost Flow Network <br/> Network Simplex Solver]
    H --> J[Generate Visual Matplotlib Graphs]
    I --> J
    J --> K[Compile PDF Settlement Report]
    K --> L[Send automated email to members via SMTP]
```

---

## ⚙️ How the Algorithms Work

### 1. Greedy Algorithm
This approach simplifies debts by balancing individual nets (credits minus debits):
1. Calculates the net balance of each group member:
   $$\text{Net Balance}_i = \sum \text{Receivables}_i - \sum \text{Payables}_i$$
2. Partitions members into **Debtors** ($\text{Net} < 0$) and **Creditors** ($\text{Net} > 0$).
3. Sorts debtors in ascending order (greatest debt first) and creditors in descending order (greatest credit first).
4. Greedily pairs the largest debtor with the largest creditor, resolving $\min(|\text{Debt}|, \text{Credit})$.
5. Updates net balances and repeats until all balances reach zero.

### 2. Graph Flow Algorithm (Min-Cost Flow)
A network flow representation using NetworkX's **Network Simplex** algorithm:
1. Constructs a directed graph where nodes represent participants and directed edges represent debt pathways.
2. A virtual `__SOURCE__` node is connected to all Creditors ($\text{capacity} = \text{credit balance}, \text{cost} = 0$).
3. A virtual `__SINK__` node is connected to all Debtors ($\text{capacity} = |\text{debt balance}|, \text{cost} = 0$).
4. Participants are interconnected with directed edges ($\text{cost} = 1$).
5. The algorithm executes Minimum Cost Flow to determine the minimal-weight transaction route satisfying all supplies and demands.

---

## 📁 Folder Structure

```text
├── main.py                     # Cash Flow CLI Entry Point & Report Generator
├── streamlit_app.py            # Streamlit Interactive Web Application
├── greedy_algorithm.py         # Greedy Debt Minimizer Algorithm
├── graph_flow_algorithm.py     # Network Simplex Min-Cost Flow Algorithm
├── generate_pdf_report         # PDF Generation Utilities (FPDF2)
├── config.py                   # SMTP Email Configuration
├── cash_flow.db                # SQLite Application Database
├── requirements.txt            # Python Dependencies
├── templates/                  # Web Templates
│   └── index.html
└── static/                     # Assets & Generated Graph Images
    └── graphs/
```

---

## 🛠️ Tech Stack & Dependencies

| Tool / Library | Category | Description |
| :--- | :--- | :--- |
| **Python 3.8+** | Core Language | Application logic & data structures |
| **Streamlit** | Frontend / GUI | Modern, interactive web UI dashboard |
| **NetworkX** | Graph Algorithms | Graph modeling & Network Simplex solver |
| **Matplotlib** | Data Visualization | Renders directed debt graphs |
| **fpdf2** | Reporting | Compiles structured PDF invoices & reports |
| **Pandas & NumPy** | Data Wrangling | Manages balances and matrix calculations |
| **SQLite** | Database | Local persistence for groups, members, and expenses |
| **smtplib** | Email Service | Automated email dispatch with PDF attachments |

---

## 📥 Installation & Setup

### Prerequisites
- Python 3.8 or above installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/Lokeshwar-09/Cash-Flow-Minimizer.git
cd Cash-Flow-Minimizer
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure SMTP Email Dispatcher (Optional)
If you wish to send PDF settlement reports directly via Gmail SMTP, update `config.py` with your Google App Password:
```python
GMAIL_USER = "your-email@gmail.com"
GMAIL_PASSWORD = "your-app-password"  # Generate at https://myaccount.google.com/apppasswords
```

---

## 💻 Usage Guide

### Option A: Streamlit Web UI (Recommended)
Launch the rich interactive web application:
```bash
streamlit run streamlit_app.py
```
Open your browser and navigate to `http://localhost:8501`.

### Option B: Command Line Interface (CLI)
Run the interactive console application:
```bash
python main.py
```

---

## 📄 License & Authors

- **License**: This project is licensed under the [MIT License](LICENSE).
- **Authors**:
  - **N. Lokeshwar** (24020)
  - **M. Gowtham** (24018)
