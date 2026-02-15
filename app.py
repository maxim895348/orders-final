import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Premium Dark Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141432 0%, #1e1e4a 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #a5b4fc !important;
    }

    /* Headers */
    h1, h2, h3 { color: #e0e7ff !important; font-weight: 700 !important; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.10) 100%);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 8px;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99,102,241,0.25);
    }
    .kpi-value {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 8px;
    }
    .kpi-delta {
        font-size: 0.8rem;
        margin-top: 4px;
        font-weight: 600;
    }
    .kpi-delta.positive { color: #34d399; }
    .kpi-delta.negative { color: #f87171; }
    .kpi-delta.neutral { color: #94a3b8; }

    /* Colored variants */
    .kpi-card.green {
        background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(52,211,153,0.08) 100%);
        border-color: rgba(16,185,129,0.3);
    }
    .kpi-card.green .kpi-value {
        background: linear-gradient(135deg, #34d399 0%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-card.orange {
        background: linear-gradient(135deg, rgba(251,146,60,0.15) 0%, rgba(251,191,36,0.08) 100%);
        border-color: rgba(251,146,60,0.3);
    }
    .kpi-card.orange .kpi-value {
        background: linear-gradient(135deg, #fb923c 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-card.red {
        background: linear-gradient(135deg, rgba(248,113,113,0.15) 0%, rgba(251,113,133,0.08) 100%);
        border-color: rgba(248,113,113,0.3);
    }
    .kpi-card.red .kpi-value {
        background: linear-gradient(135deg, #f87171 0%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-card.blue {
        background: linear-gradient(135deg, rgba(56,189,248,0.15) 0%, rgba(96,165,250,0.08) 100%);
        border-color: rgba(56,189,248,0.3);
    }
    .kpi-card.blue .kpi-value {
        background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-card.cyan {
        background: linear-gradient(135deg, rgba(34,211,238,0.15) 0%, rgba(103,232,249,0.08) 100%);
        border-color: rgba(34,211,238,0.3);
    }
    .kpi-card.cyan .kpi-value {
        background: linear-gradient(135deg, #22d3ee 0%, #67e8f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Section divider */
    .section-divider {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(99,102,241,0.4) 50%, transparent 100%);
        margin: 32px 0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(30,30,74,0.5);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Plotly chart containers */
    .stPlotlyChart {
        background: rgba(20,20,50,0.3);
        border: 1px solid rgba(99,102,241,0.12);
        border-radius: 16px;
        padding: 8px;
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 12px;
    }

    /* Multiselect */
    .stMultiSelect > div {
        background: rgba(30,30,74,0.5) !important;
        border-color: rgba(99,102,241,0.3) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PLOTLY THEME
# ──────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", color="#c7d2fe", size=13),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', size=11),
        orientation='h',
        yanchor='bottom', y=1.02, xanchor='right', x=1
    ),
    xaxis=dict(gridcolor='rgba(99,102,241,0.08)', zerolinecolor='rgba(99,102,241,0.15)'),
    yaxis=dict(gridcolor='rgba(99,102,241,0.08)', zerolinecolor='rgba(99,102,241,0.15)'),
)

COLOR_PALETTE = ['#818cf8', '#a78bfa', '#c084fc', '#34d399', '#38bdf8',
                 '#fb923c', '#f87171', '#fbbf24', '#22d3ee', '#e879f9',
                 '#4ade80', '#f472b6', '#93c5fd', '#86efac', '#fdba74']

# ── EUR estimation: average revenue per pallet ──
EUR_PER_PALLET = 850  # Estimated average revenue per pallet in EUR

STATUS_COLORS = {
    'FINAL': '#818cf8',
    'COMPLETE': '#34d399',
    'HOLD': '#fb923c',
    'HOLD PACK': '#fbbf24',
    'Compliance': '#f87171'
}

PAYMENT_COLORS = {
    'PREPAYMENT': '#34d399',
    'LC': '#38bdf8',
    'LC OPEN': '#22d3ee',
    'PAYMENT': '#fb923c',
    'CANCELLED': '#f87171',
    'N/A': '#64748b'
}


# ──────────────────────────────────────────────
# FILE UPLOAD / AUTO-DETECT
# ──────────────────────────────────────────────
import os, io

# Try to auto-detect local file first
LOCAL_FILE = 'ORDERS.xlsx'
file_source = None

if os.path.exists(LOCAL_FILE):
    file_source = LOCAL_FILE
elif 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
    file_source = st.session_state.uploaded_file

if file_source is None:
    # Show upload screen
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <h1 style="font-size:2.4rem; font-weight:800; margin:0;
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #e879f9 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📊 Sales Analytics Dashboard
        </h1>
        <p style="color:#94a3b8; font-size:1.1rem; margin-top:12px;">
            Загрузите файл <b style="color:#c7d2fe;">ORDERS.xlsx</b> для начала работы
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_u1, col_u2, col_u3 = st.columns([1, 2, 1])
    with col_u2:
        uploaded = st.file_uploader(
            "Перетащите файл сюда или нажмите Browse",
            type=['xlsx', 'xls'],
            key='file_upload_widget',
            help="Поддерживается формат Excel (.xlsx)"
        )
        if uploaded is not None:
            st.session_state.uploaded_file = uploaded
            st.rerun()

    st.stop()


# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data(_file_source):
    """Load and clean all relevant sheets from ORDERS.xlsx."""

    if isinstance(_file_source, str):
        xls = pd.ExcelFile(_file_source, engine='openpyxl')
    else:
        xls = pd.ExcelFile(io.BytesIO(_file_source.getvalue()), engine='openpyxl')

    # ── S&OP Meeting ──
    df_sop = pd.read_excel(xls, sheet_name='S&OP Meeting WK19 2025', header=2)
    # Clean column names
    df_sop.columns = [str(c).strip() if pd.notna(c) else f'col_{i}' for i, c in enumerate(df_sop.columns)]
    # Drop instruction row
    df_sop = df_sop.iloc[1:].reset_index(drop=True)
    # Drop fully empty rows
    df_sop = df_sop.dropna(how='all').reset_index(drop=True)
    # Rename key columns for consistency
    col_map_sop = {}
    for c in df_sop.columns:
        cl = c.lower()
        if 'proforma' in cl:
            col_map_sop[c] = 'proforma'
        elif 'company name' in cl:
            col_map_sop[c] = 'company'
        elif 'pallets' in cl and 'pallet' in cl:
            col_map_sop[c] = 'pallets'
        elif c.lower() == 'country':
            col_map_sop[c] = 'country'
        elif c.lower() == 'status':
            col_map_sop[c] = 'status'
        elif 'order entry date' in cl:
            col_map_sop[c] = 'order_date'
        elif 'payment status' in cl:
            col_map_sop[c] = 'payment_status'
        elif 'supply status' in cl:
            col_map_sop[c] = 'supply_status'
        elif 'adapted promised' in cl:
            col_map_sop[c] = 'promised_date'
        elif 'final shipment date' in cl:
            col_map_sop[c] = 'shipment_date'
    df_sop = df_sop.rename(columns=col_map_sop)

    # Convert dates
    for dc in ['order_date', 'promised_date', 'shipment_date']:
        if dc in df_sop.columns:
            df_sop[dc] = pd.to_datetime(df_sop[dc], errors='coerce')

    # Ensure pallets is numeric
    if 'pallets' in df_sop.columns:
        df_sop['pallets'] = pd.to_numeric(df_sop['pallets'], errors='coerce')

    # ── Orders (detail lines) ──
    df_orders_raw = pd.read_excel(xls, sheet_name='Orders', header=1)
    df_orders_raw.columns = [str(c).strip() if pd.notna(c) else f'col_{i}' for i, c in enumerate(df_orders_raw.columns)]

    # The Orders sheet has a parent-child structure:
    # Parent row: Order number, Customer code, ProForma ref, Customer, Country, etc.
    # Child rows: Same order number, Quantity, Semi-finished product, Finished product, Product description
    # Separator: empty row

    # Rename columns
    col_map_orders = {}
    for c in df_orders_raw.columns:
        cl = c.lower().replace('\n', ' ')
        if 'order' in cl and 'number' in cl:
            col_map_orders[c] = 'order_number'
        elif cl == 'customer':
            col_map_orders[c] = 'customer_code'
        elif cl == 'quantity':
            col_map_orders[c] = 'quantity'
        elif 'product description' in cl:
            col_map_orders[c] = 'product_description'
        elif 'finished product' == cl:
            col_map_orders[c] = 'finished_product'
        elif 'semi-finished' in cl:
            col_map_orders[c] = 'semi_finished'
        elif cl == 'country':
            col_map_orders[c] = 'country'
        elif cl == 'status':
            col_map_orders[c] = 'order_status'
        elif 'order entry' in cl:
            col_map_orders[c] = 'order_date'
        elif cl == 'transport':
            col_map_orders[c] = 'transport'
        elif cl == 'origin':
            col_map_orders[c] = 'origin'
        elif 'pallets' in cl:
            col_map_orders[c] = 'pallets'
    df_orders_raw = df_orders_raw.rename(columns=col_map_orders)

    # Build clean orders by processing parent-child structure
    orders_list = []
    current_header = {}

    for _, row in df_orders_raw.iterrows():
        order_num = row.get('order_number')
        qty = row.get('quantity')
        product = row.get('product_description')
        country = row.get('country')

        if pd.isna(order_num):
            continue

        # Check if this is a header row (has country) or a detail row (has product)
        if pd.notna(country) and (pd.isna(product) or product == country):
            # Header row
            current_header = {
                'order_number': int(order_num) if isinstance(order_num, float) else order_num,
                'customer_code': row.get('customer_code'),
                'country': country,
                'order_date': pd.to_datetime(row.get('order_date'), errors='coerce'),
                'pallets': pd.to_numeric(row.get('pallets'), errors='coerce'),
                'transport': row.get('transport'),
                'order_status': row.get('order_status'),
                'product_description': row.get('product_description'),
            }
        elif pd.notna(product) and str(product) not in ['None', '']:
            # Detail row
            detail = {
                **current_header,
                'quantity': pd.to_numeric(qty, errors='coerce'),
                'product': str(product).strip(),
                'finished_product': row.get('finished_product'),
                'semi_finished': row.get('semi_finished'),
                'origin': row.get('origin'),
            }
            orders_list.append(detail)

    df_orders = pd.DataFrame(orders_list)

    # ── Order Planning Operations ──
    df_opo = pd.read_excel(xls, sheet_name='Order Planning Operations', header=2)
    df_opo.columns = [str(c).strip() if pd.notna(c) else f'col_{i}' for i, c in enumerate(df_opo.columns)]
    df_opo = df_opo.iloc[1:].reset_index(drop=True)
    df_opo = df_opo.dropna(how='all').reset_index(drop=True)

    col_map_opo = {}
    for c in df_opo.columns:
        cl = c.lower()
        if 'proforma' in cl:
            col_map_opo[c] = 'proforma'
        elif 'company name' in cl:
            col_map_opo[c] = 'company'
        elif 'pallets' in cl:
            col_map_opo[c] = 'pallets'
        elif c.lower() == 'country':
            col_map_opo[c] = 'country'
        elif c.lower() == 'status':
            col_map_opo[c] = 'status'
        elif 'order entry date' in cl:
            col_map_opo[c] = 'order_date'
        elif 'payment status' in cl:
            col_map_opo[c] = 'payment_status'
        elif 'promised shipment' in cl:
            col_map_opo[c] = 'promised_date'
        elif 'cold chain' in cl:
            col_map_opo[c] = 'cold_chain'
        elif c.lower() == 'issue':
            col_map_opo[c] = 'issue'
    df_opo = df_opo.rename(columns=col_map_opo)

    for dc in ['order_date', 'promised_date']:
        if dc in df_opo.columns:
            df_opo[dc] = pd.to_datetime(df_opo[dc], errors='coerce')
    if 'pallets' in df_opo.columns:
        df_opo['pallets'] = pd.to_numeric(df_opo['pallets'], errors='coerce')

    # ── Packing (for product catalog) ──
    df_packing = pd.read_excel(xls, sheet_name='packing', header=0)
    df_packing.columns = [str(c).strip() if pd.notna(c) else f'col_{i}' for i, c in enumerate(df_packing.columns)]

    return df_sop, df_orders, df_opo, df_packing


# ──────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────
try:
    df_sop, df_orders, df_opo, df_packing = load_data(file_source)
    data_loaded = True
except Exception as e:
    st.error(f"❌ Ошибка загрузки данных: {e}")
    data_loaded = False
    st.stop()


# ──────────────────────────────────────────────
# FILTER TO 2025
# ──────────────────────────────────────────────
def filter_2025(df, date_col='order_date'):
    """Filter dataframe to 2025 year entries."""
    if date_col in df.columns:
        mask = df[date_col].dt.year == 2025
        return df[mask].copy()
    return df.copy()

df_sop_2025 = filter_2025(df_sop)
df_orders_2025 = filter_2025(df_orders)
df_opo_2025 = filter_2025(df_opo)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Фильтры")
    st.markdown("---")

    # Country filter
    all_countries = sorted(df_sop_2025['country'].dropna().unique().tolist()) if 'country' in df_sop_2025.columns else []
    selected_countries = st.multiselect(
        "🌍 Страны",
        options=all_countries,
        default=[],
        placeholder="Все страны"
    )

    # Status filter
    all_statuses = sorted(df_sop_2025['status'].dropna().unique().tolist()) if 'status' in df_sop_2025.columns else []
    selected_statuses = st.multiselect(
        "📋 Статус заказа",
        options=all_statuses,
        default=[],
        placeholder="Все статусы"
    )

    # Payment filter
    all_payments = sorted(df_sop_2025['payment_status'].dropna().unique().tolist()) if 'payment_status' in df_sop_2025.columns else []
    selected_payments = st.multiselect(
        "💳 Условие оплаты",
        options=all_payments,
        default=[],
        placeholder="Все условия"
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#64748b; font-size:0.75rem;'>"
        "📊 Sales Analytics Dashboard<br>Data: ORDERS.xlsx · 2025"
        "</div>",
        unsafe_allow_html=True
    )


# Apply filters
def apply_filters(df):
    filtered = df.copy()
    if selected_countries and 'country' in filtered.columns:
        filtered = filtered[filtered['country'].isin(selected_countries)]
    if selected_statuses and 'status' in filtered.columns:
        filtered = filtered[filtered['status'].isin(selected_statuses)]
    if selected_payments and 'payment_status' in filtered.columns:
        filtered = filtered[filtered['payment_status'].isin(selected_payments)]
    return filtered

df_sop_f = apply_filters(df_sop_2025)

# For orders, apply country filter
df_orders_f = df_orders_2025.copy()
if selected_countries:
    df_orders_f = df_orders_f[df_orders_f['country'].isin(selected_countries)]

df_opo_f = apply_filters(df_opo_2025)


# ──────────────────────────────────────────────
# HELPER: KPI Card
# ──────────────────────────────────────────────
def kpi_card(value, label, delta=None, delta_type='neutral', color=''):
    css_class = f"kpi-card {color}" if color else "kpi-card"
    delta_html = ""
    if delta:
        delta_html = f'<div class="kpi-delta {delta_type}">{delta}</div>'
    return f"""
    <div class="{css_class}">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding: 20px 0 10px;">
    <h1 style="font-size:2.2rem; font-weight:800; margin:0;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #e879f9 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📊 Sales Analytics Dashboard
    </h1>
    <p style="color:#94a3b8; font-size:1rem; margin-top:4px;">
        Fiscal Year 2025 · Order & Payment Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════
total_orders = len(df_sop_f)
total_pallets = df_sop_f['pallets'].sum() if 'pallets' in df_sop_f.columns else 0
total_revenue_eur = total_pallets * EUR_PER_PALLET
unique_countries = df_sop_f['country'].nunique() if 'country' in df_sop_f.columns else 0
unique_customers = df_sop_f['company'].nunique() if 'company' in df_sop_f.columns else 0

# Payment breakdown
payment_counts = df_sop_f['payment_status'].value_counts() if 'payment_status' in df_sop_f.columns else pd.Series()
prepaid = payment_counts.get('PREPAYMENT', 0)
lc_total = payment_counts.get('LC', 0) + payment_counts.get('LC OPEN', 0)
payment_due = payment_counts.get('PAYMENT', 0)
no_payment_info = total_orders - prepaid - lc_total - payment_due

# EUR amounts by payment type (based on pallets)
def pallets_by_payment(status_list):
    if 'payment_status' not in df_sop_f.columns or 'pallets' not in df_sop_f.columns:
        return 0
    return df_sop_f[df_sop_f['payment_status'].isin(status_list)]['pallets'].sum() * EUR_PER_PALLET

eur_prepaid = pallets_by_payment(['PREPAYMENT'])
eur_lc = pallets_by_payment(['LC', 'LC OPEN'])
eur_due = pallets_by_payment(['PAYMENT'])

# Status breakdown
complete_count = len(df_sop_f[df_sop_f['status'] == 'COMPLETE']) if 'status' in df_sop_f.columns else 0
final_count = len(df_sop_f[df_sop_f['status'] == 'FINAL']) if 'status' in df_sop_f.columns else 0
hold_count = len(df_sop_f[df_sop_f['status'].isin(['HOLD', 'HOLD PACK'])]) if 'status' in df_sop_f.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(kpi_card(f"€{total_revenue_eur:,.0f}", "Выручка (est.)", f"📦 {total_orders} заказов", 'neutral', ''), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card(f"{total_pallets:,.0f}", "Паллет (объём)", f"≈ €{EUR_PER_PALLET}/пал.", 'neutral', 'blue'), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card(f"{unique_countries}", "Стран", f"🌍 География", 'neutral', 'cyan'), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card(f"€{eur_prepaid:,.0f}", "Оплачено", f"✅ {prepaid} заказов", 'positive', 'green'), unsafe_allow_html=True)
with c5:
    st.markdown(kpi_card(f"€{eur_lc:,.0f}", "Аккредитив (LC)", f"🏦 {lc_total} заказов", 'neutral', 'orange'), unsafe_allow_html=True)
with c6:
    st.markdown(kpi_card(f"€{eur_due:,.0f}", "Ожидает оплату", f"⚠️ {payment_due} заказов", 'negative', 'red'), unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "🌍 География продаж",
    "📦 Продукты",
    "💳 Оплата и долги",
    "📋 Детали заказов"
])


# ──────────────────────────────────────────────
# TAB 1: OVERVIEW
# ──────────────────────────────────────────────
with tab1:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 📈 Заказы по месяцам (2025)")
        if 'order_date' in df_sop_f.columns:
            monthly = df_sop_f.groupby(df_sop_f['order_date'].dt.to_period('M')).agg(
                orders=('order_date', 'count'),
                pallets=('pallets', 'sum')
            ).reset_index()
            monthly['order_date'] = monthly['order_date'].astype(str)

            fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])
            fig_monthly.add_trace(
                go.Bar(
                    x=monthly['order_date'], y=monthly['orders'],
                    name='Заказы', marker_color='#818cf8',
                    marker=dict(cornerradius=6),
                    opacity=0.85
                ), secondary_y=False
            )
            fig_monthly.add_trace(
                go.Scatter(
                    x=monthly['order_date'], y=monthly['pallets'],
                    name='Паллеты', line=dict(color='#34d399', width=3),
                    mode='lines+markers', marker=dict(size=8, symbol='diamond')
                ), secondary_y=True
            )
            fig_monthly.update_layout(
                **PLOTLY_LAYOUT,
                title=None, height=380,
                yaxis_title="Кол-во заказов",
                yaxis2_title="Паллеты",
                barmode='group',
                hovermode='x unified'
            )
            st.plotly_chart(fig_monthly, width='stretch')

    with col_right:
        st.markdown("### 📊 Статус заказов")
        if 'status' in df_sop_f.columns:
            status_data = df_sop_f['status'].value_counts().reset_index()
            status_data.columns = ['status', 'count']
            status_data['color'] = status_data['status'].map(STATUS_COLORS).fillna('#64748b')

            fig_status = go.Figure(data=[go.Pie(
                labels=status_data['status'],
                values=status_data['count'],
                hole=0.6,
                marker=dict(colors=status_data['color'].tolist(),
                            line=dict(color='#0f0f23', width=2)),
                textinfo='label+percent',
                textfont=dict(size=13, color='#e0e7ff'),
                hovertemplate='<b>%{label}</b><br>Заказов: %{value}<br>Доля: %{percent}<extra></extra>'
            )])
            fig_status.update_layout(
                **PLOTLY_LAYOUT,
                height=380,
                showlegend=False,
                annotations=[dict(
                    text=f"<b>{total_orders}</b><br>заказов",
                    x=0.5, y=0.5, font_size=18, font_color='#c7d2fe',
                    showarrow=False
                )]
            )
            st.plotly_chart(fig_status, width='stretch')

    # Second row — Top customers
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 🏢 Топ-15 клиентов по объёму (паллеты)")

    if 'company' in df_sop_f.columns and 'pallets' in df_sop_f.columns:
        top_cust = df_sop_f.groupby('company').agg(
            total_pallets=('pallets', 'sum'),
            order_count=('company', 'count')
        ).sort_values('total_pallets', ascending=True).tail(15).reset_index()

        fig_cust = go.Figure()
        fig_cust.add_trace(go.Bar(
            y=top_cust['company'],
            x=top_cust['total_pallets'],
            orientation='h',
            marker=dict(
                color=top_cust['total_pallets'],
                colorscale=[[0, '#4f46e5'], [0.5, '#818cf8'], [1, '#c084fc']],
                cornerradius=6
            ),
            text=[f"{v:.0f} пал. · {n} зак." for v, n in zip(top_cust['total_pallets'], top_cust['order_count'])],
            textposition='auto',
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{y}</b><br>Паллет: %{x:.1f}<extra></extra>'
        ))
        fig_cust.update_layout(
            **PLOTLY_LAYOUT,
            height=500,
            yaxis_title=None,
            xaxis_title="Паллеты",
        )
        st.plotly_chart(fig_cust, width='stretch')


# ──────────────────────────────────────────────
# TAB 2: GEOGRAPHY
# ──────────────────────────────────────────────
with tab2:
    st.markdown("### 🗺️ География продаж 2025")

    if 'country' in df_sop_f.columns:
        geo_data = df_sop_f.groupby('country').agg(
            orders=('country', 'count'),
            pallets=('pallets', 'sum')
        ).reset_index().sort_values('pallets', ascending=False)
        geo_data['eur'] = geo_data['pallets'] * EUR_PER_PALLET

        # World map
        fig_map = px.choropleth(
            geo_data,
            locations='country',
            locationmode='country names',
            color='pallets',
            hover_name='country',
            hover_data={'orders': True, 'pallets': ':.1f'},
            color_continuous_scale=['#1e1b4b', '#3730a3', '#4f46e5', '#818cf8', '#a78bfa', '#c084fc', '#e879f9'],
            labels={'pallets': 'Паллеты', 'orders': 'Заказы'}
        )
        fig_map.update_layout(
            **PLOTLY_LAYOUT,
            height=450,
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                lakecolor='rgba(15,15,35,0.6)',
                landcolor='rgba(30,30,60,0.5)',
                showframe=False,
                showcoastlines=True,
                coastlinecolor='rgba(99,102,241,0.2)',
                projection_type='natural earth'
            ),
            coloraxis_colorbar=dict(
                title=dict(text="Паллеты", font=dict(color='#c7d2fe')),
                tickfont=dict(color='#94a3b8'),
            )
        )
        st.plotly_chart(fig_map, width='stretch')

        # Top countries chart
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### 📊 Топ-20 стран по заказам")
            top_geo = geo_data.sort_values('orders', ascending=True).tail(20)
            fig_geo_bar = go.Figure(go.Bar(
                y=top_geo['country'],
                x=top_geo['orders'],
                orientation='h',
                marker=dict(
                    color=top_geo['orders'],
                    colorscale=[[0, '#1e40af'], [0.5, '#38bdf8'], [1, '#22d3ee']],
                    cornerradius=5
                ),
                text=top_geo['orders'],
                textposition='auto',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Заказов: %{x}<extra></extra>'
            ))
            fig_geo_bar.update_layout(**PLOTLY_LAYOUT, height=550, xaxis_title="Заказы")
            st.plotly_chart(fig_geo_bar, width='stretch')

        with col_b:
            st.markdown("### 📐 Топ-20 стран по объёму (паллеты)")
            top_geo_vol = geo_data.sort_values('pallets', ascending=True).tail(20)
            fig_geo_vol = go.Figure(go.Bar(
                y=top_geo_vol['country'],
                x=top_geo_vol['pallets'],
                orientation='h',
                marker=dict(
                    color=top_geo_vol['pallets'],
                    colorscale=[[0, '#065f46'], [0.5, '#34d399'], [1, '#6ee7b7']],
                    cornerradius=5
                ),
                text=[f"{v:.0f}" for v in top_geo_vol['pallets']],
                textposition='auto',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Паллет: %{x:.1f}<extra></extra>'
            ))
            fig_geo_vol.update_layout(**PLOTLY_LAYOUT, height=550, xaxis_title="Паллеты")
            st.plotly_chart(fig_geo_vol, width='stretch')

        # Regional breakdown
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("### 🌐 Региональная сводка")

        # Build a simple region mapping
        region_map = {
            'Iraq': 'Middle East', 'Qatar': 'Middle East', 'Saudi Arabia': 'Middle East',
            'Azerbaijan': 'Middle East', 'Georgia': 'Middle East',
            'Sri Lanka': 'Asia', 'Vietnam': 'Asia', 'Malaysia': 'Asia',
            'Cambodja': 'Asia', 'Indonesia': 'Asia', 'Nepal': 'Asia',
            'Myanmar': 'Asia', 'Bangladesh': 'Asia', 'Thailand': 'Asia',
            'Philippines': 'Asia', 'Laos': 'Asia',
            'Zimbabwe': 'Africa', 'Senegal': 'Africa', 'Burkina Faso': 'Africa',
            'Ghana': 'Africa', 'Zambia': 'Africa', 'Tchad': 'Africa',
            'Democratic Republic of the Congo': 'Africa', 'Benin': 'Africa',
            'Mali': 'Africa', 'Ethiopia': 'Africa', 'Tanzania': 'Africa',
            'Ivory Coast': 'Africa', 'Mozambique': 'Africa', 'Kenya': 'Africa',
            'Cameroon': 'Africa', 'Niger': 'Africa', 'Madagascar': 'Africa',
            'Rwanda': 'Africa', 'Uganda': 'Africa', 'Somalia': 'Africa',
            'Sudan': 'Africa', 'Togo': 'Africa', 'Guinea': 'Africa',
            'Bulgaria': 'Europe', 'Cyprus': 'Europe', 'Hungary': 'Europe',
            'Albania': 'Europe', 'Serbia': 'Europe', 'Ireland': 'Europe',
            'Republic of North Macedonia': 'Europe', 'Romania': 'Europe',
            'Lithuania': 'Europe', 'Croatia': 'Europe', 'Malta': 'Europe',
            'Greece': 'Europe', 'Ukraine': 'Europe', 'Slovenia': 'Europe',
            'Bosnia and Herzegovina': 'Europe', 'Kosovo': 'Europe',
            'Russia': 'CIS', 'Belarus': 'CIS', 'Uzbekistan': 'CIS',
            'Kazakhstan': 'CIS', 'Kyrgyzstan': 'CIS', 'Tajikistan': 'CIS',
            'Afghanistan': 'CIS',
        }

        geo_data['region'] = geo_data['country'].map(region_map).fillna('Other')
        region_agg = geo_data.groupby('region').agg(
            orders=('orders', 'sum'),
            pallets=('pallets', 'sum'),
            countries=('country', 'count')
        ).sort_values('orders', ascending=False).reset_index()

        region_colors = {'Middle East': '#fb923c', 'Asia': '#38bdf8', 'Africa': '#34d399',
                         'Europe': '#818cf8', 'CIS': '#e879f9', 'Other': '#64748b'}

        fig_region = go.Figure(data=[go.Pie(
            labels=region_agg['region'],
            values=region_agg['orders'],
            hole=0.55,
            marker=dict(
                colors=[region_colors.get(r, '#64748b') for r in region_agg['region']],
                line=dict(color='#0f0f23', width=2)
            ),
            textinfo='label+percent+value',
            textfont=dict(size=13, color='#e0e7ff'),
            hovertemplate='<b>%{label}</b><br>Заказов: %{value}<br>Доля: %{percent}<extra></extra>'
        )])
        fig_region.update_layout(**PLOTLY_LAYOUT, height=400, showlegend=True)
        st.plotly_chart(fig_region, width='stretch')


# ──────────────────────────────────────────────
# TAB 3: PRODUCTS
# ──────────────────────────────────────────────
with tab3:
    st.markdown("### 📦 Анализ продуктов (2025)")

    has_product = len(df_orders_f) > 0 and 'product' in df_orders_f.columns
    qty_col = 'quantity' if has_product and 'quantity' in df_orders_f.columns else None
    order_col = 'order_number' if has_product and 'order_number' in df_orders_f.columns else None

    if has_product and qty_col:
        # Top products by quantity — safe agg
        agg_dict = {'total_qty': (qty_col, 'sum')}
        if order_col:
            agg_dict['order_count'] = (order_col, 'nunique')
        else:
            agg_dict['order_count'] = (qty_col, 'count')

        prod_data = df_orders_f.groupby('product').agg(**agg_dict
        ).sort_values('total_qty', ascending=False).head(25).reset_index()

        col_p1, col_p2 = st.columns(2)

        with col_p1:
            st.markdown("#### 🏆 Топ-25 продуктов по объёму (шт.)")
            fig_prod = go.Figure(go.Bar(
                y=prod_data['product'][::-1],
                x=prod_data['total_qty'][::-1],
                orientation='h',
                marker=dict(
                    color=prod_data['total_qty'][::-1],
                    colorscale=[[0, '#7c3aed'], [0.5, '#a78bfa'], [1, '#e879f9']],
                    cornerradius=5
                ),
                text=[f"{v:,.0f}" for v in prod_data['total_qty'][::-1]],
                textposition='auto',
                textfont=dict(color='white', size=10),
                hovertemplate='<b>%{y}</b><br>Кол-во: %{x:,.0f}<extra></extra>'
            ))
            fig_prod.update_layout(**PLOTLY_LAYOUT, height=700, xaxis_title="Количество (шт.)")
            st.plotly_chart(fig_prod, width='stretch')

        with col_p2:
            st.markdown("#### 📋 Топ-25 продуктов по числу заказов")
            agg_dict2 = {'order_count': (order_col, 'nunique') if order_col else (qty_col, 'count'),
                         'total_qty': (qty_col, 'sum')}
            prod_by_orders = df_orders_f.groupby('product').agg(**agg_dict2
            ).sort_values('order_count', ascending=False).head(25).reset_index()

            fig_prod_orders = go.Figure(go.Bar(
                y=prod_by_orders['product'][::-1],
                x=prod_by_orders['order_count'][::-1],
                orientation='h',
                marker=dict(
                    color=prod_by_orders['order_count'][::-1],
                    colorscale=[[0, '#0e7490'], [0.5, '#22d3ee'], [1, '#67e8f9']],
                    cornerradius=5
                ),
                text=prod_by_orders['order_count'][::-1],
                textposition='auto',
                textfont=dict(color='white', size=10),
                hovertemplate='<b>%{y}</b><br>Заказов: %{x}<extra></extra>'
            ))
            fig_prod_orders.update_layout(**PLOTLY_LAYOUT, height=700, xaxis_title="Кол-во заказов")
            st.plotly_chart(fig_prod_orders, width='stretch')

        # Product-Country matrix
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("### 🗂️ Матрица: Продукт × Страна (топ-10 × топ-10)")

        if 'country' in df_orders_f.columns:
            top10_products = df_orders_f.groupby('product')[qty_col].sum().nlargest(10).index.tolist()
            top10_countries = df_orders_f.groupby('country')[qty_col].sum().nlargest(10).index.tolist()

            matrix_data = df_orders_f[
                df_orders_f['product'].isin(top10_products) &
                df_orders_f['country'].isin(top10_countries)
            ].groupby(['product', 'country'])[qty_col].sum().unstack(fill_value=0)

            if len(matrix_data) > 0:
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=matrix_data.values,
                    x=matrix_data.columns.tolist(),
                    y=matrix_data.index.tolist(),
                    colorscale=[[0, '#0f0f23'], [0.25, '#312e81'], [0.5, '#4f46e5'],
                                [0.75, '#818cf8'], [1, '#c084fc']],
                    text=[[f"{v:,.0f}" if v > 0 else "" for v in row] for row in matrix_data.values],
                    texttemplate="%{text}",
                    textfont=dict(size=10, color='white'),
                    hovertemplate='<b>%{y}</b> → %{x}<br>Кол-во: %{z:,.0f}<extra></extra>'
                ))
                fig_heatmap.update_layout(**PLOTLY_LAYOUT, height=450)
                fig_heatmap.update_xaxes(tickangle=45)
                st.plotly_chart(fig_heatmap, width='stretch')

    else:
        st.info("Нет данных по продуктам для выбранных фильтров.")


# ──────────────────────────────────────────────
# TAB 4: PAYMENT & DEBTS
# ──────────────────────────────────────────────
with tab4:
    st.markdown("### 💳 Условия оплаты и финансовый статус (2025)")

    # KPI row for payments
    c_p1, c_p2, c_p3, c_p4 = st.columns(4)

    with c_p1:
        pct_prepaid = (prepaid / total_orders * 100) if total_orders > 0 else 0
        st.markdown(kpi_card(f"{prepaid}", "Предоплата (PREPAYMENT)", f"{pct_prepaid:.0f}% от всех", 'positive', 'green'), unsafe_allow_html=True)
    with c_p2:
        pct_lc = (lc_total / total_orders * 100) if total_orders > 0 else 0
        st.markdown(kpi_card(f"{lc_total}", "Аккредитив (LC)", f"{pct_lc:.0f}% от всех", 'neutral', 'blue'), unsafe_allow_html=True)
    with c_p3:
        pct_payment = (payment_due / total_orders * 100) if total_orders > 0 else 0
        st.markdown(kpi_card(f"{payment_due}", "Ожидает оплату", f"{pct_payment:.0f}% от всех", 'negative', 'orange'), unsafe_allow_html=True)
    with c_p4:
        pct_noinfo = (no_payment_info / total_orders * 100) if total_orders > 0 else 0
        st.markdown(kpi_card(f"{no_payment_info}", "Без данных оплаты", f"{pct_noinfo:.0f}% от всех", 'neutral', 'red'), unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_pay1, col_pay2 = st.columns(2)

    with col_pay1:
        st.markdown("#### 📊 Распределение условий оплаты")
        if 'payment_status' in df_sop_f.columns:
            pay_data = df_sop_f['payment_status'].fillna('Не указано').value_counts().reset_index()
            pay_data.columns = ['payment', 'count']

            pay_colors = [PAYMENT_COLORS.get(p, '#64748b') for p in pay_data['payment']]

            fig_pay = go.Figure(data=[go.Pie(
                labels=pay_data['payment'],
                values=pay_data['count'],
                hole=0.55,
                marker=dict(colors=pay_colors, line=dict(color='#0f0f23', width=2)),
                textinfo='label+percent+value',
                textfont=dict(size=12, color='#e0e7ff'),
                hovertemplate='<b>%{label}</b><br>Заказов: %{value}<br>Доля: %{percent}<extra></extra>'
            )])
            fig_pay.update_layout(**PLOTLY_LAYOUT, height=400, showlegend=False)
            st.plotly_chart(fig_pay, width='stretch')

    with col_pay2:
        st.markdown("#### 🌍 Условия оплаты по странам (топ-15)")
        if 'payment_status' in df_sop_f.columns and 'country' in df_sop_f.columns:
            pay_country = df_sop_f.groupby(['country', 'payment_status']).size().reset_index(name='count')
            top_pay_countries = df_sop_f.groupby('country').size().nlargest(15).index.tolist()
            pay_country = pay_country[pay_country['country'].isin(top_pay_countries)]

            fig_pay_country = px.bar(
                pay_country,
                x='country', y='count',
                color='payment_status',
                color_discrete_map=PAYMENT_COLORS,
                barmode='stack',
                labels={'count': 'Заказы', 'payment_status': 'Оплата', 'country': 'Страна'}
            )
            fig_pay_country.update_layout(**PLOTLY_LAYOUT, height=400)
            fig_pay_country.update_xaxes(tickangle=45)
            fig_pay_country.update_traces(marker=dict(cornerradius=4))
            st.plotly_chart(fig_pay_country, width='stretch')

    # OPO payment with pallets volume
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### 📐 Объём (паллеты) и выручка по условиям оплаты")

    if 'payment_status' in df_sop_f.columns and 'pallets' in df_sop_f.columns:
        pay_vol = df_sop_f.groupby(df_sop_f['payment_status'].fillna('Не указано')).agg(
            total_pallets=('pallets', 'sum'),
            orders=('pallets', 'count')
        ).sort_values('total_pallets', ascending=True).reset_index()
        pay_vol['eur'] = pay_vol['total_pallets'] * EUR_PER_PALLET

        pay_vol_colors = [PAYMENT_COLORS.get(p, '#64748b') for p in pay_vol['payment_status']]

        fig_pay_vol = go.Figure(go.Bar(
            y=pay_vol['payment_status'],
            x=pay_vol['eur'],
            orientation='h',
            marker=dict(color=pay_vol_colors, cornerradius=6),
            text=[f"€{e:,.0f} · {v:,.0f} пал. ({n} зак.)" for e, v, n in zip(pay_vol['eur'], pay_vol['total_pallets'], pay_vol['orders'])],
            textposition='auto',
            textfont=dict(color='white', size=12),
            hovertemplate='<b>%{y}</b><br>Выручка: €%{x:,.0f}<extra></extra>'
        ))
        fig_pay_vol.update_layout(**PLOTLY_LAYOUT, height=300, xaxis_title="Выручка (EUR)")
        st.plotly_chart(fig_pay_vol, width='stretch')

    # Detailed table: Orders with payment issues
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### 🔍 Заказы с задолженностью / ожиданием оплаты")

    if 'payment_status' in df_sop_f.columns:
        debt_orders = df_sop_f[df_sop_f['payment_status'].isin(['PAYMENT', 'LC OPEN'])].copy()
        if len(debt_orders) > 0:
            display_cols = [c for c in ['proforma', 'company', 'country', 'pallets',
                                        'payment_status', 'status', 'order_date', 'promised_date']
                           if c in debt_orders.columns]
            debt_display = debt_orders[display_cols].sort_values('order_date', ascending=False)
            debt_display.columns = [c.replace('_', ' ').title() for c in debt_display.columns]
            st.dataframe(debt_display, width='stretch', height=300)
        else:
            st.success("✅ Нет заказов с открытой задолженностью в текущей выборке!")


# ──────────────────────────────────────────────
# TAB 5: ORDER DETAILS TABLE
# ──────────────────────────────────────────────
with tab5:
    st.markdown("### 📋 Детализация заказов 2025")

    # S&OP view
    st.markdown("#### Основная таблица S&OP")
    if len(df_sop_f) > 0:
        display_sop = df_sop_f.copy()
        sop_cols = [c for c in ['proforma', 'company', 'country', 'pallets', 'status',
                                'order_date', 'promised_date', 'payment_status',
                                'supply_status', 'shipment_date']
                    if c in display_sop.columns]
        display_sop = display_sop[sop_cols].sort_values('order_date', ascending=False)
        col_labels = {
            'proforma': 'Proforma', 'company': 'Компания', 'country': 'Страна',
            'pallets': 'Паллеты', 'status': 'Статус', 'order_date': 'Дата заказа',
            'promised_date': 'Дата отгрузки', 'payment_status': 'Оплата',
            'supply_status': 'Supply', 'shipment_date': 'Факт. отгрузка'
        }
        display_sop = display_sop.rename(columns=col_labels)
        st.dataframe(display_sop, width='stretch', height=500)
    else:
        st.info("Нет данных для отображения.")

    # Product lines
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### Детализация по продуктам")
    if len(df_orders_f) > 0:
        order_cols = [c for c in ['order_number', 'customer_code', 'country',
                                  'product', 'quantity', 'origin', 'order_date']
                      if c in df_orders_f.columns]
        display_orders = df_orders_f[order_cols].sort_values('order_date', ascending=False)
        order_labels = {
            'order_number': '№ Заказа', 'customer_code': 'Клиент', 'country': 'Страна',
            'product': 'Продукт', 'quantity': 'Кол-во', 'origin': 'Производство',
            'order_date': 'Дата'
        }
        display_orders = display_orders.rename(columns=order_labels)
        st.dataframe(display_orders, width='stretch', height=500)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:40px 0 20px; color:#475569; font-size:0.8rem;">
    <hr class="section-divider">
    Sales Analytics Dashboard 2025 · Powered by Streamlit & Plotly<br>
    Data source: ORDERS.xlsx · Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """
</div>
""", unsafe_allow_html=True)
