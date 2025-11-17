import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

# Snowflakeセッション取得
session = get_active_session()

# ページ設定
st.set_page_config(
    page_title="顧客分析ダッシュボード",
    page_icon="👥",
    layout="wide"
)

# タイトル
st.title("👥 Tasty Bytes 顧客分析ダッシュボード")
st.markdown("---")

# データ取得
@st.cache_data
def get_customer_data():
    query = """
    SELECT 
        CUSTOMER_ID,
        FIRST_NAME,
        LAST_NAME,
        CITY,
        COUNTRY,
        TOTAL_SALES,
        VISITED_LOCATION_IDS_ARRAY,
        ARRAY_SIZE(VISITED_LOCATION_IDS_ARRAY) as visited_locations_count
    FROM TB_101.ANALYTICS.CUSTOMER_LOYALTY_METRICS_V
    WHERE TOTAL_SALES > 0
    """
    return session.sql(query).to_pandas()

# サイドバーフィルター
st.sidebar.header("🔍 フィルター")

customer_data = get_customer_data()

# 国選択
countries = ["全て"] + sorted(customer_data['COUNTRY'].unique().tolist())
selected_country = st.sidebar.selectbox("国を選択", countries)

# 売上範囲選択
min_sales = int(customer_data['TOTAL_SALES'].min())
max_sales = int(customer_data['TOTAL_SALES'].max())
sales_range = st.sidebar.slider(
    "売上範囲 ($)",
    min_sales,
    max_sales,
    (min_sales, max_sales)
)

# データフィルタリング
filtered_data = customer_data[
    (customer_data['TOTAL_SALES'] >= sales_range[0]) & 
    (customer_data['TOTAL_SALES'] <= sales_range[1])
]

if selected_country != "全て":
    filtered_data = filtered_data[filtered_data['COUNTRY'] == selected_country]

# 主要指標（前のバージョンに戻す）
st.header("📊 顧客概要")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("総顧客数", f"{len(filtered_data):,}")

with col2:
    avg_sales = filtered_data['TOTAL_SALES'].mean()
    st.metric("平均売上", f"${avg_sales:.2f}")

with col3:
    avg_locations = filtered_data['VISITED_LOCATIONS_COUNT'].mean()
    st.metric("平均訪問店舗数", f"{avg_locations:.1f}")

with col4:
    total_revenue = filtered_data['TOTAL_SALES'].sum()
    st.metric("総売上", f"${total_revenue:,.2f}")

st.markdown("---")

# シンプルなグラフエリア
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 国別顧客分布")
    
    country_counts = filtered_data['COUNTRY'].value_counts().head(8)
    
    fig = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        title='国別顧客数',
        labels={'x': '国', 'y': '顧客数'},
        color=country_counts.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 売上分布")
    
    fig = px.histogram(
        filtered_data,
        x='TOTAL_SALES',
        nbins=15,
        title='顧客売上分布',
        labels={'TOTAL_SALES': '売上 ($)', 'count': '顧客数'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# 都市別分析
st.subheader("🏙️ 都市別顧客分析")

city_analysis = filtered_data.groupby('CITY').agg({
    'CUSTOMER_ID': 'count',
    'TOTAL_SALES': ['sum', 'mean'],
    'VISITED_LOCATIONS_COUNT': 'mean'
}).round(2)

city_analysis.columns = ['顧客数', '総売上', '平均売上', '平均訪問店舗数']
city_analysis = city_analysis.sort_values('顧客数', ascending=False).head(10)

# 都市別の棒グラフ
fig = px.bar(
    x=city_analysis.index,
    y=city_analysis['顧客数'],
    title='都市別顧客数トップ10',
    labels={'x': '都市', 'y': '顧客数'},
    color=city_analysis['平均売上'],
    color_continuous_scale='Viridis'
)
fig.update_layout(
    height=400,
    xaxis_tickangle=-45
)
st.plotly_chart(fig, use_container_width=True)

# ランキングセクション
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 売上トップ10顧客")
    
    top_customers = filtered_data.nlargest(10, 'TOTAL_SALES')[
        ['FIRST_NAME', 'LAST_NAME', 'CITY', 'COUNTRY', 'TOTAL_SALES']
    ].copy()
    
    top_customers['顧客名'] = top_customers['FIRST_NAME'] + ' ' + top_customers['LAST_NAME']
    
    fig = px.bar(
        x=top_customers['TOTAL_SALES'],
        y=top_customers['顧客名'],
        orientation='h',
        title='売上トップ10',
        labels={'x': '売上 ($)', 'y': '顧客名'},
        color_discrete_sequence=['#ff7f0e']
    )
    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎪 訪問店舗数トップ10顧客")
    
    top_visitors = filtered_data.nlargest(10, 'VISITED_LOCATIONS_COUNT')[
        ['FIRST_NAME', 'LAST_NAME', 'CITY', 'COUNTRY', 'VISITED_LOCATIONS_COUNT', 'TOTAL_SALES']
    ].copy()
    
    top_visitors['顧客名'] = top_visitors['FIRST_NAME'] + ' ' + top_visitors['LAST_NAME']
    
    fig = px.bar(
        x=top_visitors['VISITED_LOCATIONS_COUNT'],
        y=top_visitors['顧客名'],
        orientation='h',
        title='訪問店舗数トップ10',
        labels={'x': '訪問店舗数', 'y': '顧客名'},
        color_discrete_sequence=['#2ca02c']
    )
    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)


# 詳細データテーブル
st.subheader("📋 顧客詳細データ")

display_data = filtered_data[
    ['FIRST_NAME', 'LAST_NAME', 'CITY', 'COUNTRY', 'TOTAL_SALES', 'VISITED_LOCATIONS_COUNT']
].copy()

display_data.columns = ['名前', '姓', '都市', '国', '売上 ($)', '訪問店舗数']

st.dataframe(
    display_data.head(20),
    column_config={
        "売上 ($)": st.column_config.NumberColumn("売上 ($)", format="$%.2f")
    },
    use_container_width=True,
    hide_index=True
)

# フッター
st.markdown("---")
st.caption("データソース: TB_101.ANALYTICS.CUSTOMER_LOYALTY_METRICS_V")
