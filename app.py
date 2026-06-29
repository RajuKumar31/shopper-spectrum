import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
.stApp { background: #f5f4ff !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
    width: 100%; background: #1e1b4b;
    padding: 0 40px; height: 68px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 3px solid #4f46e5;
}
.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-logo {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.topbar-name { font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; }
.topbar-name span { color: #a5b4fc; }
.topbar-tagline { font-size: 12px; color: #6366f1; font-weight: 500; margin-top: 1px; }
.topbar-right { display: flex; align-items: center; gap: 10px; }
.topbar-pill {
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc; font-size: 11px; font-weight: 600;
    padding: 5px 14px; border-radius: 20px; letter-spacing: 0.04em;
}
.topbar-pill.green { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.3); color: #6ee7b7; }

/* ── NAV TABS ── */
.nav-bar {
    background: #ffffff; border-bottom: 1px solid #e5e7eb;
    padding: 0 40px; display: flex; gap: 4px; align-items: center; height: 52px;
}
.nav-tab {
    padding: 8px 20px; border-radius: 8px;
    font-size: 13px; font-weight: 600; cursor: pointer;
    color: #6b7280; transition: all 0.15s; border: none; background: none;
    text-decoration: none; display: inline-flex; align-items: center; gap: 7px;
}
.nav-tab.active { background: #eef2ff; color: #4f46e5; }
.nav-tab:hover { background: #f9fafb; color: #374151; }

/* ── STATS ROW ── */
.stats-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 18px; padding: 28px 40px 0; }
.scard {
    background: #ffffff; border: 1px solid #ebe8ff; border-radius: 16px;
    padding: 22px 24px; display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 8px rgba(79,70,229,0.08);
}
.scard-icon { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
.si1 { background: #eef2ff; } .si2 { background: #ecfdf5; } .si3 { background: #fff7ed; } .si4 { background: #fdf4ff; }
.scard-val { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 600; color: #111827; line-height: 1; }
.scard-key { font-size: 12px; color: #6b7280; margin-top: 4px; font-weight: 500; }

/* ── PAGE CONTENT ── */
.page-wrap { padding: 28px 40px 48px; }
.page-title { font-size: 22px; font-weight: 800; color: #111827; letter-spacing: -0.02em; margin-bottom: 4px; }
.page-sub { font-size: 13px; color: #9ca3af; margin-bottom: 24px; }

/* ── CARDS ── */
.card {
    background: #ffffff; border: 1px solid #e8eaf0;
    border-radius: 16px; padding: 28px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.card-title { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.card-sub { font-size: 12px; color: #9ca3af; margin-bottom: 20px; }

/* ── WIDGETS ── */
.stSelectbox label, .stNumberInput label {
    color: #374151 !important; font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 0.07em !important; text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: #f9fafb !important; border: 1.5px solid #e5e7eb !important;
    border-radius: 10px !important; color: #111827 !important;
}
.stSelectbox > div > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important; }
.stNumberInput > div > div > input {
    background: #f9fafb !important; border: 1.5px solid #e5e7eb !important;
    border-radius: 10px !important; color: #111827 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 16px !important; font-weight: 500 !important;
}
.stNumberInput > div > div > input:focus { border-color: #10b981 !important; box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important; }

/* ── BUTTONS ── */
.stButton > button {
    width: 100% !important; border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; padding: 14px 24px !important; border: none !important;
    font-family: 'Outfit', sans-serif !important; transition: all 0.2s ease !important;
}
.btn-indigo .stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important; }
.btn-indigo .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(79,70,229,0.4) !important; }
.btn-emerald .stButton > button { background: linear-gradient(135deg, #059669, #10b981) !important; color: white !important; box-shadow: 0 4px 15px rgba(5,150,105,0.3) !important; }
.btn-emerald .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(5,150,105,0.4) !important; }

/* ── REC CARDS ── */
.rec-tag { font-size: 11px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 12px; }
.rec-card {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 16px; border-radius: 12px;
    background: #fafbff; border: 1px solid #e8eaf0; margin-bottom: 10px; transition: all 0.15s;
}
.rec-card:hover { background: #eef2ff; border-color: #c7d2fe; transform: translateX(3px); }
.rec-rank {
    width: 32px; height: 32px; border-radius: 9px; background: #4f46e5; color: white;
    font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.rec-info { flex: 1; }
.rec-name { font-size: 13px; font-weight: 600; color: #1f2937; }
.rec-bar { height: 4px; border-radius: 2px; background: #e5e7eb; margin-top: 6px; overflow: hidden; }
.rec-bar-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #4f46e5, #7c3aed); }
.rec-score { background: #eef2ff; color: #4f46e5; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 8px; flex-shrink: 0; }

/* ── SEGMENT RESULT ── */
.seg-result { border-radius: 16px; padding: 28px; border: 2px solid; }
.seg-high    { background: #f0fdf4; border-color: #4ade80; }
.seg-regular { background: #eff6ff; border-color: #60a5fa; }
.seg-occ     { background: #fffbeb; border-color: #fbbf24; }
.seg-risk    { background: #fef2f2; border-color: #f87171; }
.seg-toprow { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.seg-emoji { font-size: 40px; }
.seg-chip { font-size: 11px; font-weight: 800; padding: 5px 14px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.08em; }
.chip-high    { background: #15803d; color: #f0fdf4; }
.chip-regular { background: #1d4ed8; color: #eff6ff; }
.chip-occ     { background: #b45309; color: #fffbeb; }
.chip-risk    { background: #b91c1c; color: #fef2f2; }
.seg-heading { font-size: 24px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 8px; }
.seg-high .seg-heading    { color: #166534; }
.seg-regular .seg-heading { color: #1e40af; }
.seg-occ .seg-heading     { color: #92400e; }
.seg-risk .seg-heading    { color: #991b1b; }
.seg-desc { font-size: 13px; color: #4b5563; line-height: 1.65; margin-bottom: 16px; }
.seg-action { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; padding: 9px 16px; border-radius: 10px; margin-bottom: 20px; }
.abox-high    { background: #dcfce7; color: #15803d; }
.abox-regular { background: #dbeafe; color: #1e40af; }
.abox-occ     { background: #fef3c7; color: #92400e; }
.abox-risk    { background: #fee2e2; color: #991b1b; }
.seg-metrics { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.seg-mbox { background: rgba(255,255,255,0.8); border-radius: 12px; padding: 14px; text-align: center; border: 1px solid rgba(0,0,0,0.05); }
.seg-mval { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 600; color: #111827; }
.seg-mkey { font-size: 10px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 4px; }

/* ── EMPTY ── */
.empty-state { text-align: center; padding: 52px 20px; }
.empty-icon { font-size: 44px; margin-bottom: 14px; opacity: 0.35; }
.empty-text { font-size: 13px; color: #9ca3af; line-height: 1.6; }

/* ── CHART GRID ── */
.chart-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.chart-card { background: #ffffff; border: 1px solid #ebe8ff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 8px rgba(79,70,229,0.08); }
.chart-label { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.chart-sublabel { font-size: 12px; color: #9ca3af; margin-bottom: 16px; }

/* ── INSIGHT BOX ── */
.insight {
    background: #f8faff; border-left: 4px solid #6366f1;
    border-radius: 0 10px 10px 0; padding: 12px 16px;
    font-size: 12px; color: #4b5563; line-height: 1.6; margin-top: 12px;
}
.insight strong { color: #4f46e5; }
</style>
""", unsafe_allow_html=True)


# ── Load Assets ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    with open('kmeans_model.pkl', 'rb') as f:
        kmeans = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('product_list.pkl', 'rb') as f:
        product_list = pickle.load(f)
    product_similarity_df = pd.read_csv('product_similarity.csv', index_col=0)
    return kmeans, scaler, product_list, product_similarity_df

@st.cache_data
def load_data():
    df = pd.read_csv('online_retail.csv', encoding='latin1')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df.dropna(subset=['CustomerID'])
    df = df.drop_duplicates()
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df['CustomerID'] = df['CustomerID'].astype(int)
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    return df

kmeans, scaler, product_list, product_similarity_df = load_assets()
df = load_data()

cluster_labels = {2: 'High-Value', 3: 'Regular', 0: 'Occasional', 1: 'At-Risk'}
segment_config = {
    'High-Value': { 'card': 'seg-high', 'chip': 'chip-high', 'abox': 'abox-high', 'emoji': '💎', 'action': '🎁 Reward with VIP perks & early access', 'desc': 'Top-tier customer. Buys frequently, spends big, and purchased very recently. Prioritise these relationships above everyone else.' },
    'Regular':    { 'card': 'seg-regular', 'chip': 'chip-regular', 'abox': 'abox-regular', 'emoji': '⭐', 'action': '📦 Offer product bundles & loyalty points', 'desc': 'Steady and reliable buyer. Nurture with targeted bundles and personalised offers to push average order value higher.' },
    'Occasional': { 'card': 'seg-occ', 'chip': 'chip-occ', 'abox': 'abox-occ', 'emoji': '🔔', 'action': '⏰ Send limited-time deals & reminders', 'desc': 'Buys infrequently but shows some engagement. Time-sensitive promotions can convert this customer into a Regular.' },
    'At-Risk':    { 'card': 'seg-risk', 'chip': 'chip-risk', 'abox': 'abox-risk', 'emoji': '⚠️', 'action': '📧 Launch win-back campaign immediately', 'desc': "Hasn't purchased in a long time with low engagement. Needs an immediate win-back discount or personalised outreach." }
}

# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-logo">🛒</div>
        <div>
            <div class="topbar-name">Shopper <span>Spectrum</span></div>
            <div class="topbar-tagline">E-Commerce Customer Intelligence Platform</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="topbar-pill">KMeans Clustering</div>
        <div class="topbar-pill">Collaborative Filtering</div>
        <div class="topbar-pill green">✓ Model Active</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── NAVIGATION ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stRadio > div {
    flex-direction: row !important; gap: 8px !important;
    background: transparent; padding: 16px 40px;
    border-bottom: 1px solid #e5e7eb; margin: 0;
}
.stRadio label {
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 10px !important; padding: 9px 22px !important;
    font-size: 13px !important; font-weight: 600 !important;
    color: #6b7280 !important; cursor: pointer !important;
    transition: all 0.15s !important;
}
.stRadio label:hover {
    background: #eef2ff !important;
    color: #4f46e5 !important;
    border-color: #c7d2fe !important;
}
div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked),
.stRadio div[data-baseweb="radio"]:has(input:checked) label {
    background: #4f46e5 !important;
    color: #ffffff !important;
    border-color: #4f46e5 !important;
    box-shadow: 0 4px 12px rgba(79,70,229,0.35) !important;
}
.stRadio > div > label > div:first-child { display: none !important; }
</style>
""", unsafe_allow_html=True)

nav = st.radio("nav", ["📊  Dashboard", "👤  Clustering", "🎯  Recommendations"],
               horizontal=True, label_visibility="collapsed")
page = nav.split("  ")[1]

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

# ── STATS ROW (always visible) ────────────────────────────────────────────────
st.markdown("""
<div class="stats-grid">
    <div class="scard"><div class="scard-icon si1">👥</div><div><div class="scard-val">4,338</div><div class="scard-key">Unique Customers</div></div></div>
    <div class="scard"><div class="scard-icon si2">🛍️</div><div><div class="scard-val">3,877</div><div class="scard-key">Products Indexed</div></div></div>
    <div class="scard"><div class="scard-icon si3">🏷️</div><div><div class="scard-val">4</div><div class="scard-key">Customer Segments</div></div></div>
    <div class="scard"><div class="scard-icon si4">📊</div><div><div class="scard-val">392K</div><div class="scard-key">Transactions</div></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == 'Dashboard':
    st.markdown("""
    <div class="page-wrap" style="padding-bottom:0;">
        <div class="page-title">📊 Analytics Dashboard</div>
        <div class="page-sub">Exploratory analysis of the Online Retail dataset · Dec 2022 – Dec 2023</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 40px 48px;">', unsafe_allow_html=True)

        # Row 1: Top Countries + Top Products
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            st.markdown('<div class="chart-card"><div class="chart-label">🌍 Top 10 Countries by Transactions</div><div class="chart-sublabel">United Kingdom dominates — shown separately for scale</div>', unsafe_allow_html=True)
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            fig.patch.set_facecolor('white')
            top_countries = df['Country'].value_counts().head(10)
            top_ex_uk = df[df['Country'] != 'United Kingdom']['Country'].value_counts().head(9)
            for ax, data, title, color in [
                (axes[0], top_countries, 'All Countries', 'Blues_r'),
                (axes[1], top_ex_uk, 'Excl. UK', 'Purples_r')
            ]:
                ax.set_facecolor('white')
                bars = ax.barh(data.index, data.values, color=plt.cm.get_cmap(color)(np.linspace(0.3, 0.9, len(data))))
                for bar, val in zip(bars, data.values):
                    ax.text(val * 1.01, bar.get_y() + bar.get_height()/2, f'{val:,}', va='center', fontsize=7, color='#374151', fontweight='600')
                ax.set_title(title, fontsize=10, fontweight='bold', color='#111827', pad=8)
                ax.set_xlabel('Transactions', fontsize=8, color='#6b7280')
                ax.tick_params(labelsize=7, colors='#374151')
                ax.spines[['top','right','left']].set_visible(False)
                ax.set_xlim(0, data.values.max() * 1.2)
                ax.grid(axis='x', alpha=0.3, linewidth=0.5)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('<div class="insight"><strong>Insight:</strong> UK accounts for ~89% of all transactions (349,203). Germany and France are the next biggest markets at ~9K and ~8K respectively.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-card"><div class="chart-label">🛍️ Top 10 Best-Selling Products</div><div class="chart-sublabel">By total quantity sold across all orders</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 4.8))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
            colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_products)))[::-1]
            bars = ax.barh(top_products.index, top_products.values, color=colors)
            for bar, val in zip(bars, top_products.values):
                ax.text(val * 1.01, bar.get_y() + bar.get_height()/2, f'{val:,}', va='center', fontsize=8, color='#374151', fontweight='600')
            ax.set_xlabel('Total Quantity Sold', fontsize=9, color='#6b7280')
            ax.tick_params(labelsize=8, colors='#374151')
            ax.spines[['top','right','left']].set_visible(False)
            ax.set_xlim(0, top_products.values.max() * 1.2)
            ax.grid(axis='x', alpha=0.3, linewidth=0.5)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('<div class="insight"><strong>Insight:</strong> PAPER CRAFT LITTLE BIRDIE leads with 80,995 units. Top products are predominantly home décor and gift items — typical of a UK wholesale retailer.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

        # Row 2: Monthly Trend + Revenue Distribution
        c3, c4 = st.columns(2, gap="medium")

        with c3:
            st.markdown('<div class="chart-card"><div class="chart-label">📈 Monthly Purchase Trend</div><div class="chart-sublabel">Total quantity sold per month · Dec 2022 – Dec 2023</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            monthly = df.groupby('YearMonth')['Quantity'].sum().reset_index()
            ax.plot(monthly['YearMonth'], monthly['Quantity'], marker='o', color='#4f46e5', linewidth=2.5, markersize=6, markerfacecolor='white', markeredgewidth=2)
            ax.fill_between(range(len(monthly)), monthly['Quantity'], alpha=0.08, color='#4f46e5')
            for i, row in monthly.iterrows():
                ax.text(i, row['Quantity'] + 8000, f"{row['Quantity']/1000:.0f}K", ha='center', fontsize=7.5, color='#4f46e5', fontweight='600')
            ax.set_xticks(range(len(monthly)))
            ax.set_xticklabels(monthly['YearMonth'], rotation=45, ha='right', fontsize=8, color='#374151')
            ax.tick_params(axis='y', labelsize=8, colors='#6b7280')
            ax.spines[['top','right']].set_visible(False)
            ax.spines[['left','bottom']].set_color('#e5e7eb')
            ax.grid(axis='y', alpha=0.3, linewidth=0.5)
            ax.set_ylabel('Quantity Sold', fontsize=9, color='#6b7280')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('<div class="insight"><strong>Insight:</strong> Sales dip in Feb 2023 (265K) — post-holiday slowdown. Strong Nov 2023 peak (665K) is the pre-Christmas surge. Dec drops as data ends on 9th Dec.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-card"><div class="chart-label">💰 Revenue Distribution per Transaction</div><div class="chart-sublabel">Excluding top 1% outliers for better visibility</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            txn_rev = df.groupby('InvoiceNo')['TotalPrice'].sum()
            txn_filtered = txn_rev[txn_rev < txn_rev.quantile(0.99)]
            ax.hist(txn_filtered, bins=50, color='#6366f1', alpha=0.75, edgecolor='white', linewidth=0.5)
            ax.axvline(txn_rev.median(), color='#10b981', linewidth=2, linestyle='--', label=f'Median: £{txn_rev.median():.0f}')
            ax.axvline(txn_rev.mean(), color='#f59e0b', linewidth=2, linestyle='--', label=f'Mean: £{txn_rev.mean():.0f}')
            ax.legend(fontsize=9, framealpha=0.9)
            ax.set_xlabel('Transaction Revenue (£)', fontsize=9, color='#6b7280')
            ax.set_ylabel('Number of Transactions', fontsize=9, color='#6b7280')
            ax.tick_params(labelsize=8, colors='#374151')
            ax.spines[['top','right']].set_visible(False)
            ax.spines[['left','bottom']].set_color('#e5e7eb')
            ax.grid(axis='y', alpha=0.3, linewidth=0.5)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('<div class="insight"><strong>Insight:</strong> Median transaction is £303 but mean is £480 — a small number of very large bulk orders are pulling the average up. Classic right-skewed B2B pattern.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

        # Row 3: Top Customers (full width)
        st.markdown('<div class="chart-card"><div class="chart-label">🏆 Top 10 Customers by Total Revenue</div><div class="chart-sublabel">Based on total spend across all transactions</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(14, 4))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        top_customers = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
        colors = plt.cm.RdPu(np.linspace(0.4, 0.85, len(top_customers)))
        bars = ax.bar([str(c) for c in top_customers.index], top_customers.values, color=colors, width=0.6, edgecolor='white')
        for bar, val in zip(bars, top_customers.values):
            ax.text(bar.get_x() + bar.get_width()/2, val + 2000, f'£{val/1000:.0f}K', ha='center', fontsize=9, color='#374151', fontweight='700')
        ax.set_xlabel('Customer ID', fontsize=10, color='#6b7280')
        ax.set_ylabel('Total Revenue (£)', fontsize=10, color='#6b7280')
        ax.tick_params(labelsize=9, colors='#374151')
        ax.spines[['top','right']].set_visible(False)
        ax.spines[['left','bottom']].set_color('#e5e7eb')
        ax.grid(axis='y', alpha=0.3, linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown(f'<div class="insight"><strong>Insight:</strong> Top customer (ID: {top_customers.index[0]}) spent £{top_customers.values[0]/1000:.0f}K — significantly more than the rest. These whale customers represent a small group driving disproportionate revenue.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: CLUSTERING
# ════════════════════════════════════════════════════════════════════════════
elif page == 'Clustering':
    st.markdown("""
    <div class="page-wrap" style="padding-bottom:0;">
        <div class="page-title">👤 Customer Segmentation</div>
        <div class="page-sub">Enter RFM values to predict a customer's segment using KMeans clustering</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 40px 48px;">', unsafe_allow_html=True)

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown('<div class="card"><div class="card-title">Enter Customer RFM Values</div><div class="card-sub">Recency · Frequency · Monetary</div>', unsafe_allow_html=True)

            r_col, f_col = st.columns(2)
            with r_col:
                recency = st.number_input("Recency (Days)", min_value=0, max_value=1000, value=30)
            with f_col:
                frequency = st.number_input("Frequency", min_value=1, max_value=500, value=5)

            monetary = st.number_input("Monetary — Total Spend (£)", min_value=0.0, max_value=500000.0, value=1000.0, step=100.0)

            st.markdown('<div class="btn-emerald">', unsafe_allow_html=True)
            predict = st.button("Predict Customer Segment →", use_container_width=True, key="seg_btn")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Segment guide
            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="card">
                <div class="card-title">Segment Reference Guide</div>
                <div class="card-sub">How each cluster is defined</div>
                <div style="display:flex;flex-direction:column;gap:10px;margin-top:4px;">
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#f0fdf4;border-radius:10px;border:1px solid #bbf7d0;">
                        <span style="font-size:20px;">💎</span>
                        <div><div style="font-size:13px;font-weight:700;color:#166534;">High-Value</div><div style="font-size:11px;color:#4b5563;">Low recency · High frequency · High spend</div></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#eff6ff;border-radius:10px;border:1px solid #bfdbfe;">
                        <span style="font-size:20px;">⭐</span>
                        <div><div style="font-size:13px;font-weight:700;color:#1e40af;">Regular</div><div style="font-size:11px;color:#4b5563;">Low recency · Medium frequency · Medium spend</div></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#fffbeb;border-radius:10px;border:1px solid #fde68a;">
                        <span style="font-size:20px;">🔔</span>
                        <div><div style="font-size:13px;font-weight:700;color:#92400e;">Occasional</div><div style="font-size:11px;color:#4b5563;">Medium recency · Low frequency · Low spend</div></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#fef2f2;border-radius:10px;border:1px solid #fecaca;">
                        <span style="font-size:20px;">⚠️</span>
                        <div><div style="font-size:13px;font-weight:700;color:#991b1b;">At-Risk</div><div style="font-size:11px;color:#4b5563;">High recency · Very low frequency · Low spend</div></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            if predict:
                input_scaled = scaler.transform(np.array([[recency, frequency, monetary]]))
                cluster = kmeans.predict(input_scaled)[0]
                segment = cluster_labels[cluster]
                cfg = segment_config[segment]
                st.markdown(f"""
                <div class="seg-result {cfg['card']}">
                    <div class="seg-toprow">
                        <div class="seg-emoji">{cfg['emoji']}</div>
                        <div class="seg-chip {cfg['chip']}">{segment}</div>
                    </div>
                    <div class="seg-heading">{segment} Customer</div>
                    <div class="seg-desc">{cfg['desc']}</div>
                    <div class="seg-action {cfg['abox']}">{cfg['action']}</div>
                    <div class="seg-metrics">
                        <div class="seg-mbox"><div class="seg-mval">{recency}d</div><div class="seg-mkey">Recency</div></div>
                        <div class="seg-mbox"><div class="seg-mval">{frequency}</div><div class="seg-mkey">Frequency</div></div>
                        <div class="seg-mbox"><div class="seg-mval">£{monetary:,.0f}</div><div class="seg-mkey">Monetary</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state" style="margin-top:60px;">
                    <div class="empty-icon">👤</div>
                    <div class="empty-text">Enter RFM values on the left<br>and click <strong>Predict Customer Segment</strong></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == 'Recommendations':
    st.markdown("""
    <div class="page-wrap" style="padding-bottom:0;">
        <div class="page-title">🎯 Product Recommendations</div>
        <div class="page-sub">Item-based collaborative filtering using cosine similarity on customer purchase history</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 40px 48px;">', unsafe_allow_html=True)

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown('<div class="card"><div class="card-title">Select a Product</div><div class="card-sub">Choose any product to find 5 similar items</div>', unsafe_allow_html=True)
            product_input = st.selectbox("Product Name", options=["— Choose a product —"] + sorted(product_list), index=0)
            st.markdown('<div class="btn-indigo">', unsafe_allow_html=True)
            get_rec = st.button("Find Similar Products →", use_container_width=True, key="rec_btn")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="card">
                <div class="card-title">How it Works</div>
                <div class="card-sub">Item-based collaborative filtering</div>
                <div style="display:flex;flex-direction:column;gap:12px;margin-top:8px;">
                    <div style="display:flex;gap:12px;align-items:flex-start;">
                        <div style="width:28px;height:28px;background:#eef2ff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">1</div>
                        <div style="font-size:12px;color:#4b5563;line-height:1.5;">A <strong>Customer × Product matrix</strong> is built from 392K transactions — rows are customers, columns are products, values are quantities.</div>
                    </div>
                    <div style="display:flex;gap:12px;align-items:flex-start;">
                        <div style="width:28px;height:28px;background:#eef2ff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">2</div>
                        <div style="font-size:12px;color:#4b5563;line-height:1.5;"><strong>Cosine similarity</strong> is calculated between every pair of products based on which customers bought them together.</div>
                    </div>
                    <div style="display:flex;gap:12px;align-items:flex-start;">
                        <div style="width:28px;height:28px;background:#eef2ff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">3</div>
                        <div style="font-size:12px;color:#4b5563;line-height:1.5;">The <strong>top 5 most similar products</strong> are returned, ranked by similarity score (1.0 = identical purchase pattern).</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            if get_rec:
                if product_input == "— Choose a product —":
                    st.warning("Please select a product first.")
                elif product_input not in product_similarity_df.index:
                    st.error("Product not found in the database.")
                else:
                    recs = product_similarity_df[product_input].sort_values(ascending=False)[1:6]
                    label = product_input[:55] + ("..." if len(product_input) > 55 else "")
                    st.markdown(f'<div style="margin-bottom:14px;"><div class="rec-tag">📌 Showing results for:</div><div style="font-size:14px;font-weight:700;color:#111827;">{label}</div></div>', unsafe_allow_html=True)
                    for i, (prod, score) in enumerate(recs.items(), 1):
                        bar_w = int(score * 100)
                        st.markdown(f"""
                        <div class="rec-card">
                            <div class="rec-rank">{i}</div>
                            <div class="rec-info">
                                <div class="rec-name">{prod}</div>
                                <div class="rec-bar"><div class="rec-bar-fill" style="width:{bar_w}%;"></div></div>
                            </div>
                            <div class="rec-score">{score:.3f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("""
                    <div class="insight" style="margin-top:16px;">
                        <strong>Score guide:</strong> 1.000 = identical purchase pattern · 0.700+ = strong similarity · 0.400–0.700 = moderate similarity
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state" style="margin-top:60px;">
                    <div class="empty-icon">🔍</div>
                    <div class="empty-text">Select a product on the left<br>and click <strong>Find Similar Products</strong></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #f3f4f6;padding:18px 40px;display:flex;justify-content:space-between;align-items:center;">
    <div style="font-size:12px;color:#9ca3af;font-weight:500;">🛒 Shopper Spectrum · Built with KMeans Clustering & Collaborative Filtering</div>
    <div style="font-size:12px;color:#9ca3af;">Online Retail Dataset · Dec 2022 – Dec 2023 · 392K Transactions</div>
</div>
""", unsafe_allow_html=True)