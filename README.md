# 🛒 Shopper Spectrum — E-Commerce Customer Intelligence System

An end-to-end data analytics project that analyses 392,000+ online retail transactions to segment customers using RFM analysis and KMeans clustering, and recommend products using item-based collaborative filtering. Built with Python, scikit-learn, and Streamlit.

**🚀 Live Demo:** [shopper-spectrum-4jn3ernyuguqf6le2zrxhi.streamlit.app](https://shopper-spectrum-4jn3ernyuguqf6le2zrxhi.streamlit.app/)

---

## 📌 Project Overview

Most e-commerce businesses have thousands of customers and products but no structured way to understand buying behaviour. This project solves that by:

- Segmenting customers into 4 behavioural groups based on how recently, how often, and how much they buy
- Recommending similar products based on real purchase patterns across all customers
- Presenting everything through a clean, interactive 3-page Streamlit dashboard

---

## 🎯 Business Questions Answered

- Who are the highest-value customers?
- Which customers are at risk of churning?
- Which products are most frequently bought together?
- Which countries and months drive the most sales?
- What should we recommend to a customer who buys product X?

---

## 🗂️ Dataset

**Source:** Online Retail Dataset (UCI Machine Learning Repository)  
**Period:** December 2022 – December 2023  
**Raw records:** 541,909 rows | **After cleaning:** 392,692 rows

| Column | Description |
|--------|-------------|
| InvoiceNo | Unique bill number per transaction |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units purchased |
| InvoiceDate | Date and time of purchase |
| UnitPrice | Price per unit (£) |
| CustomerID | Unique customer identifier |
| Country | Customer's country |

---

## 🔧 Project Pipeline

```
Load Dataset
    ↓
Data Cleaning
(nulls · duplicates · cancellations · invalid qty/price)
    ↓
Exploratory Data Analysis
(5 charts covering countries, products, trends, revenue, customers)
    ↓
RFM Feature Engineering
(Recency · Frequency · Monetary per customer)
    ↓
KMeans Clustering
(Elbow method + Silhouette score → k=4)
    ↓
Customer Segmentation
(High-Value · Regular · Occasional · At-Risk)
    ↓
Collaborative Filtering
(Customer-Product matrix → Cosine similarity)
    ↓
Streamlit Dashboard
(Dashboard · Clustering · Recommendations)
```

---

## 📊 Exploratory Data Analysis

| Chart | Key Finding |
|-------|-------------|
| Top 10 Countries | UK accounts for 89% of transactions (349,203). Germany and France are next at ~9K and ~8K |
| Top 10 Products | PAPER CRAFT LITTLE BIRDIE leads with 80,995 units sold |
| Monthly Trend | Sales peak in November 2023 (665K units) — pre-Christmas surge |
| Revenue Distribution | Median transaction £303, mean £480 — right-skewed due to bulk B2B orders |
| Top Customers | Customer 14646 spent £280K. Top 10 customers contribute £1.53M combined |

---

## 👥 Customer Segments

| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary | Strategy |
|---------|-----------|-------------|---------------|--------------|----------|
| 💎 High-Value | 13 | 7 days | 83 orders | £127,188 | VIP perks & early access |
| ⭐ Regular | 204 | 16 days | 22 orders | £12,691 | Bundles & loyalty points |
| 🔔 Occasional | 3,054 | 44 days | 4 orders | £1,354 | Limited-time promotions |
| ⚠️ At-Risk | 1,067 | 248 days | 2 orders | £479 | Win-back campaigns |

**Model:** KMeans (k=4, Silhouette Score: 0.616)  
**Features:** StandardScaler-normalised Recency, Frequency, Monetary

---

## 🎯 Product Recommendation System

**Method:** Item-based collaborative filtering using cosine similarity

1. Built a 4,338 × 3,877 Customer-Product matrix from all transactions
2. Computed cosine similarity between every pair of products
3. For any product, returns the top 5 most similar items ranked by score

**Example:**
> Input: `WHITE HANGING HEART T-LIGHT HOLDER`  
> Recommendations: GIN + TONIC DIET METAL SIGN (0.750) · RED HANGING HEART T-LIGHT HOLDER (0.659) · WASHROOM METAL SIGN (0.644)

---

## 🖥️ Streamlit App

Three-page interactive dashboard:

**📊 Dashboard** — Live EDA charts rendered from the dataset with business insight callouts for each chart

**👤 Clustering** — Enter any customer's Recency, Frequency, and Monetary values to instantly predict their segment with a tailored engagement strategy

**🎯 Recommendations** — Select any of the 3,877 products to get 5 similar product recommendations with similarity scores and progress bars

---

## 📁 File Structure

```
shopper-spectrum/
│
├── shopper_spectrum.ipynb     # Full analysis notebook
├── app.py                     # Streamlit dashboard
├── online_retail.csv          # Raw dataset
│
├── kmeans_model.pkl           # Trained KMeans model (k=4)
├── scaler.pkl                 # StandardScaler for RFM normalisation
├── rfm_segments.csv           # 4,338 customers with RFM + segment labels
├── product_similarity.csv     # 3,877 × 3,877 cosine similarity matrix
├── product_list.pkl           # Full product name list
│
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/RajuKumar31/shopper-spectrum.git
cd shopper-spectrum
```

**2. Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit
```

**3. Run the Streamlit app**
```bash
streamlit run app.py
```

> Make sure all `.pkl` and `.csv` files are in the same folder as `app.py`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas & NumPy | Data manipulation |
| Matplotlib & Seaborn | EDA visualisations |
| scikit-learn | KMeans clustering, StandardScaler, cosine similarity |
| Streamlit | Interactive web dashboard |
| Jupyter Notebook | Step-by-step analysis |

---

## 👤 Author

**Raju Kumar S**  
Data Analyst Intern @ Labmentix  
[Portfolio](https://rajukumar31.github.io) · [LinkedIn](https://linkedin.com/in/rajukumarsahani) · [GitHub](https://github.com/RajuKumar31)