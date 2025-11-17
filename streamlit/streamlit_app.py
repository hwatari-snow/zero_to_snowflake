import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from snowflake.snowpark.context import get_active_session

# ページ設定 - 爽やかなテーマ
st.set_page_config(
    page_title="🌊 売上分析ダッシュボード",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - 爽やかな色合い
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4da6ff;
    }
    .metric-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    h1 {
        color: #1976d2;
        text-align: center;
        margin-bottom: 2rem;
    }
    h2, h3 {
        color: #1565c0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #e1f5fe 0%, #b3e5fc 100%);
    }
</style>
""", unsafe_allow_html=True)

# Snowflakeセッション取得
session = get_active_session()

# サイドバー - 強化されたフィルター機能
st.sidebar.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, #1976d2, #42a5f5); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='margin: 0; color: white;'>🔍 フィルター設定</h3>
</div>
""", unsafe_allow_html=True)

# フィルターオプション取得
@st.cache_data
def get_filter_options():
    try:
        categories = session.sql("SELECT DISTINCT product_category FROM TB_101.ANALYTICS.SALES_DATA ORDER BY 1").to_pandas()
        regions = session.sql("SELECT DISTINCT region FROM TB_101.ANALYTICS.SALES_DATA ORDER BY 1").to_pandas()
        segments = session.sql("SELECT DISTINCT customer_segment FROM TB_101.ANALYTICS.SALES_DATA ORDER BY 1").to_pandas()
        dates = session.sql("SELECT MIN(sale_date) as min_date, MAX(sale_date) as max_date FROM TB_101.ANALYTICS.SALES_DATA").to_pandas()
        return {
            'categories': categories['PRODUCT_CATEGORY'].tolist(),
            'regions': regions['REGION'].tolist(),
            'segments': segments['CUSTOMER_SEGMENT'].tolist(),
            'min_date': dates['MIN_DATE'].iloc[0],
            'max_date': dates['MAX_DATE'].iloc[0]
        }
    except Exception as e:
        st.sidebar.error(f"フィルターデータ取得エラー: {str(e)}")
        return None

filter_options = get_filter_options()

# デフォルトフィルター値
default_filters = {
    'date_range': None,
    'categories': [],
    'regions': [],
    'segments': []
}

if filter_options:
    # 日付範囲フィルター
    st.sidebar.markdown("### 📅 日付範囲")
    date_filter_type = st.sidebar.selectbox(
        "期間選択方法",
        ["全期間", "カスタム範囲", "最近7日間", "最近30日間"]
    )
    
    if date_filter_type == "カスタム範囲":
        date_range = st.sidebar.date_input(
            "期間を選択",
            value=(filter_options['min_date'], filter_options['max_date']),
            min_value=filter_options['min_date'],
            max_value=filter_options['max_date']
        )
    elif date_filter_type == "最近7日間":
        end_date = filter_options['max_date']
        start_date = end_date - timedelta(days=7)
        date_range = (start_date, end_date)
    elif date_filter_type == "最近30日間":
        end_date = filter_options['max_date']
        start_date = end_date - timedelta(days=30)
        date_range = (start_date, end_date)
    else:
        date_range = (filter_options['min_date'], filter_options['max_date'])
    
    # カテゴリフィルター
    st.sidebar.markdown("### 🏷️ 商品カテゴリ")
    category_filter_type = st.sidebar.radio(
        "選択方法",
        ["すべて", "選択"],
        key="category_filter"
    )
    
    if category_filter_type == "選択":
        selected_categories = st.sidebar.multiselect(
            "カテゴリを選択",
            options=filter_options['categories'],
            default=filter_options['categories']
        )
    else:
        selected_categories = filter_options['categories']
    
    # 地域フィルター
    st.sidebar.markdown("### 🗾 地域")
    region_filter_type = st.sidebar.radio(
        "選択方法",
        ["すべて", "選択"],
        key="region_filter"
    )
    
    if region_filter_type == "選択":
        selected_regions = st.sidebar.multiselect(
            "地域を選択",
            options=filter_options['regions'],
            default=filter_options['regions']
        )
    else:
        selected_regions = filter_options['regions']
    
    # 顧客セグメントフィルター
    st.sidebar.markdown("### 👥 顧客セグメント")
    segment_filter_type = st.sidebar.radio(
        "選択方法",
        ["すべて", "選択"],
        key="segment_filter"
    )
    
    if segment_filter_type == "選択":
        selected_segments = st.sidebar.multiselect(
            "セグメントを選択",
            options=filter_options['segments'],
            default=filter_options['segments']
        )
    else:
        selected_segments = filter_options['segments']
    
    # 売上範囲フィルター（追加機能）
    st.sidebar.markdown("### 💰 売上範囲")
    sales_filter = st.sidebar.checkbox("売上範囲でフィルター")
    if sales_filter:
        min_sales = st.sidebar.number_input("最小売上", min_value=0, value=0, step=10000)
        max_sales = st.sidebar.number_input("最大売上", min_value=0, value=1000000, step=10000)
    else:
        min_sales, max_sales = 0, float('inf')
    
    # フィルターリセット・適用ボタン
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 リセット", use_container_width=True):
            st.rerun()
    with col2:
        apply_filters = st.button("✅ 適用", use_container_width=True, type="primary")
    
    # WHERE句構築
    conditions = []
    
    # 日付条件
    if len(date_range) == 2:
        conditions.append(f"sale_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    # カテゴリ条件
    if selected_categories and len(selected_categories) < len(filter_options['categories']):
        category_list = "', '".join(selected_categories)
        conditions.append(f"product_category IN ('{category_list}')")
    
    # 地域条件
    if selected_regions and len(selected_regions) < len(filter_options['regions']):
        region_list = "', '".join(selected_regions)
        conditions.append(f"region IN ('{region_list}')")
    
    # セグメント条件
    if selected_segments and len(selected_segments) < len(filter_options['segments']):
        segment_list = "', '".join(selected_segments)
        conditions.append(f"customer_segment IN ('{segment_list}')")
    
    # 売上範囲条件
    if sales_filter:
        if max_sales != float('inf'):
            conditions.append(f"total_sales BETWEEN {min_sales} AND {max_sales}")
        else:
            conditions.append(f"total_sales >= {min_sales}")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # フィルター状況表示
    st.sidebar.markdown("---")
    filter_summary = f"""
    **📋 適用中のフィルター:**
    - 期間: {date_filter_type}
    - カテゴリ: {len(selected_categories)}個
    - 地域: {len(selected_regions)}個  
    - セグメント: {len(selected_segments)}個
    - 売上範囲: {'有効' if sales_filter else '無効'}
    """
    st.sidebar.info(filter_summary)
    
    # デバッグ情報（開発時のみ）
    with st.sidebar.expander("🔧 SQL確認", expanded=False):
        st.code(f"WHERE {where_clause}")

else:
    where_clause = "1=1"
    st.sidebar.error("フィルターデータを取得できませんでした")

# メインタイトル
st.markdown("<h1>🌊 売上分析ダッシュボード</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
st.markdown("---")

# データサマリー表示
def show_data_summary(where_clause):
    summary_query = f"""
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT product_category) as categories,
        COUNT(DISTINCT region) as regions,
        MIN(sale_date) as earliest_date,
        MAX(sale_date) as latest_date,
        SUM(total_sales) as total_revenue,
        AVG(total_sales) as avg_sales,
        SUM(profit) as total_profit
    FROM TB_101.ANALYTICS.SALES_DATA
    WHERE {where_clause}
    """
    
    try:
        summary_df = session.sql(summary_query).to_pandas()
        
        st.markdown("### 📊 データ概要")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            records = summary_df.iloc[0]['TOTAL_RECORDS']
            st.markdown(f"""
            <div class="metric-container">
                <h4 style="color: #1976d2; margin: 0;">📈 総レコード数</h4>
                <h2 style="color: #0d47a1; margin: 5px 0;">{records:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            revenue = summary_df.iloc[0]['TOTAL_REVENUE']
            st.markdown(f"""
            <div class="metric-container">
                <h4 style="color: #1976d2; margin: 0;">💰 総売上</h4>
                <h2 style="color: #0d47a1; margin: 5px 0;">¥{revenue:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            profit = summary_df.iloc[0]['TOTAL_PROFIT']
            margin = (profit / revenue * 100) if revenue > 0 else 0
            st.markdown(f"""
            <div class="metric-container">
                <h4 style="color: #1976d2; margin: 0;">📊 総利益</h4>
                <h2 style="color: #0d47a1; margin: 5px 0;">¥{profit:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_sales = summary_df.iloc[0]['AVG_SALES']
            st.markdown(f"""
            <div class="metric-container">
                <h4 style="color: #1976d2; margin: 0;">📈 平均売上</h4>
                <h2 style="color: #0d47a1; margin: 5px 0;">¥{avg_sales:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        return True
    except Exception as e:
        st.error(f"データサマリー取得エラー: {str(e)}")
        return False

# データサマリー表示
if show_data_summary(where_clause):
    st.markdown("---")
    
    # カテゴリ別売上チャート
    st.markdown("### 🎨 カテゴリ別売上分析")
    
    try:
        category_query = f"""
        SELECT 
            product_category,
            SUM(total_sales) as total_sales,
            SUM(profit) as total_profit,
            COUNT(*) as transaction_count,
            AVG(total_sales) as avg_sales
        FROM TB_101.ANALYTICS.SALES_DATA
        WHERE {where_clause}
        GROUP BY product_category
        ORDER BY total_sales DESC
        """
        
        category_df = session.sql(category_query).to_pandas()
        
        if not category_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # パステルカラーの円グラフ
                fig_pie = px.pie(
                    category_df,
                    values='TOTAL_SALES',
                    names='PRODUCT_CATEGORY',
                    title="📊 カテゴリ別売上分布",
                    color_discrete_sequence=['#81d4fa', '#a5d6a7', '#ffcc80']
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    font=dict(size=12),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # 爽やかな棒グラフ
                fig_bar = px.bar(
                    category_df,
                    x='PRODUCT_CATEGORY',
                    y='TOTAL_SALES',
                    title="💰 カテゴリ別売上額",
                    color='TOTAL_PROFIT',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(
                    xaxis_title="カテゴリ",
                    yaxis_title="売上 (¥)",
                    yaxis_tickformat=",.",
                    height=400
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("選択されたフィルター条件に該当するデータがありません。")
    
    except Exception as e:
        st.error(f"チャート作成エラー: {str(e)}")

else:
    st.warning("データベースへの接続に問題があります。管理者にお問い合わせください。")
