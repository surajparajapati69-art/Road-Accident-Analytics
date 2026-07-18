import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import time


st.set_page_config(page_title="Road Accident Intelligence", page_icon="🚨", layout="wide", initial_sidebar_state="expanded")

# Glassmorphism & Premium UI CSS
st.markdown("""
<style>
    /* Main Theme adjustments */
    .reportview-container { background: #0e1117; }
    
    /* Glassmorphism KPI Cards */
    .kpi-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.125);
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 191, 255, 0.2);
        border: 1px solid rgba(0, 191, 255, 0.5);
    }
    .kpi-value { font-size: 32px; font-weight: 800; color: #00BFFF; margin-bottom: 5px; }
    .kpi-label { font-size: 14px; font-weight: 500; color: #A0AEC0; text-transform: uppercase; letter-spacing: 1px;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0e1117; }
    ::-webkit-scrollbar-thumb { background: #00BFFF; border-radius: 4px; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def kpi_card(title, value):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{title}</div>
        </div>
    """, unsafe_allow_html=True)

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        title_x=0.5,
        title_font=dict(size=18, color="#ffffff"),
        font=dict(color="#A0AEC0")
    )
    return fig


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("road_accident.csv")
        # Ensure Date column is datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Month'] = df['Date'].dt.month_name()
            df['Year'] = df['Date'].dt.year
        return df
    except Exception as e:
        st.error(f"🚨 Error loading dataset: {e}. Please ensure 'road_accident.csv' is in the directory.")
        st.stop()

df = load_data()


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2065/2065245.png", width=80)
    st.markdown("## 🚨 AI Traffic Auth")
    st.markdown("Enterprise Intelligence")
    st.markdown("---")
    
    # Live Date & Time
    st.info(f"🕒 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
    menu = st.radio(
        "📊 NAVIGATION MENU",
        ["1️⃣ Home Dashboard", "2️⃣ Accident Analytics", "3️⃣ Victim Analytics", 
         "4️⃣ Vehicle Analytics", "5️⃣ Location Analytics", "6️⃣ Risk & Environment", "7️⃣ Dataset & About"]
    )
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray;'>Designed for Enterprise BI</div>", unsafe_allow_html=True)

if menu == "1️⃣ Home Dashboard":
    st.title("🌐 Executive Accident Intelligence")
    st.markdown("A high-level overview of the complete road accident dataset.")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Total Accidents", f"{len(df):,}")
    with c2: kpi_card("Total Casualties", f"{df['Number_of_Casualties'].sum():,}" if 'Number_of_Casualties' in df else "N/A")
    with c3: kpi_card("Avg Casualties", f"{df['Number_of_Casualties'].mean():.2f}" if 'Number_of_Casualties' in df else "N/A")
    with c4: kpi_card("Avg Vehicles", f"{df['Number_of_Vehicles'].mean():.2f}" if 'Number_of_Vehicles' in df else "N/A")
    with c5: kpi_card("High Risk", f"{len(df[df['Accident_Risk'] == 'High']):,}" if 'Accident_Risk' in df else "N/A")

    c6, c7, c8, c9, c10 = st.columns(5)
    with c6: kpi_card("States Covered", f"{df['State'].nunique():,}" if 'State' in df else "N/A")
    with c7: kpi_card("Cities Covered", f"{df['City'].nunique():,}" if 'City' in df else "N/A")
    with c8: kpi_card("Vehicle Types", f"{df['Vehicle_Type'].nunique():,}" if 'Vehicle_Type' in df else "N/A")
    with c9: kpi_card("Male Victims", f"{len(df[df['Gender'] == 'Male']):,}" if 'Gender' in df else "N/A")
    with c10: kpi_card("Female Victims", f"{len(df[df['Gender'] == 'Female']):,}" if 'Gender' in df else "N/A")
    
    st.markdown("---")
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        if 'Date' in df:
            trend_df = df.groupby('Month').size().reset_index(name='Count')
            fig = style_chart(px.line(trend_df, x='Month', y='Count', title="📉 Monthly Accident Trend", markers=True, color_discrete_sequence=['#00BFFF']))
            st.plotly_chart(fig, use_container_width=True)
            
    with r1c2:
        if 'Accident_Severity' in df:
            fig = style_chart(px.pie(df, names='Accident_Severity', title="⚠️ Severity Distribution", hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r))
            st.plotly_chart(fig, use_container_width=True)

    
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        if 'State' in df:
            st_df = df['State'].value_counts().head(10).reset_index()
            fig = style_chart(px.bar(st_df, x='count', y='State', orientation='h', title="🏆 Top 10 States", color='count', color_continuous_scale="Blues"))
            st.plotly_chart(fig, use_container_width=True)
            
    with r2c2:
        if 'Vehicle_Type' in df:
            vt_df = df['Vehicle_Type'].value_counts().head(10).reset_index()
            fig = style_chart(px.bar(vt_df, x='Vehicle_Type', y='count', title="🚗 Vehicle Type Distribution", color='count', color_continuous_scale="Teal"))
            st.plotly_chart(fig, use_container_width=True)

elif menu == "2️⃣ Accident Analytics":
    st.title("📈 Detailed Accident Analytics")
    
    # Filters
    st.markdown("### 🔍 Filter Criteria")
    f1, f2, f3, f4 = st.columns(4)
    state_filt = f1.selectbox("Select State", ["All"] + list(df['State'].dropna().unique())) if 'State' in df else "All"
    city_filt = f2.selectbox("Select City", ["All"] + list(df['City'].dropna().unique())) if 'City' in df else "All"
    road_filt = f3.selectbox("Road Type", ["All"] + list(df['Road_Type'].dropna().unique())) if 'Road_Type' in df else "All"
    weat_filt = f4.selectbox("Weather", ["All"] + list(df['Weather_Conditions'].dropna().unique())) if 'Weather_Conditions' in df else "All"
    
    filt_df = df.copy()
    if state_filt != "All": filt_df = filt_df[filt_df['State'] == state_filt]
    if city_filt != "All": filt_df = filt_df[filt_df['City'] == city_filt]
    if road_filt != "All": filt_df = filt_df[filt_df['Road_Type'] == road_filt]
    if weat_filt != "All": filt_df = filt_df[filt_df['Weather_Conditions'] == weat_filt]
    
    # KPIs
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Filtered Accidents", f"{len(filt_df):,}")
    with k2: kpi_card("Fatalities", f"{len(filt_df[filt_df['Accident_Severity']=='Fatal']):,}" if 'Accident_Severity' in filt_df else "0")
    with k3: kpi_card("Highest State", str(filt_df['State'].mode()[0]) if not filt_df.empty and 'State' in filt_df else "N/A")
    with k4: kpi_card("Highest City", str(filt_df['City'].mode()[0]) if not filt_df.empty and 'City' in filt_df else "N/A")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if 'Road_Type' in filt_df:
            fig = style_chart(px.bar(filt_df['Road_Type'].value_counts().reset_index(), x='Road_Type', y='count', title="🛣️ Road Type Analysis", color='count', color_continuous_scale="Purples"))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if 'Speed_Limit' in filt_df:
            fig = style_chart(px.pie(filt_df, names='Speed_Limit', title="🛑 Speed Limit Analysis", hole=0.3, color_discrete_sequence=px.colors.sequential.Agsunset))
            st.plotly_chart(fig, use_container_width=True)
            
    if all(col in filt_df.columns for col in ['State', 'City', 'Accident_Severity']):
        fig = style_chart(px.sunburst(filt_df.dropna(subset=['State', 'City', 'Accident_Severity']), path=['State', 'City', 'Accident_Severity'], title="🌍 Accident Hierarchy (Sunburst)", color='Accident_Severity'))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)


elif menu == "3️⃣ Victim Analytics":
    st.title("👥 Victim & Casualty Analytics")
    
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total Casualties", f"{df['Number_of_Casualties'].sum():,}" if 'Number_of_Casualties' in df else "N/A")
    with c2: kpi_card("Male Victims", f"{len(df[df['Gender'] == 'Male']):,}" if 'Gender' in df else "N/A")
    with c3: kpi_card("Female Victims", f"{len(df[df['Gender'] == 'Female']):,}" if 'Gender' in df else "N/A")
    
    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        if 'Gender' in df:
            fig = style_chart(px.pie(df, names='Gender', title="🚻 Gender Distribution", color_discrete_sequence=['#00BFFF', '#FF1493']))
            st.plotly_chart(fig, use_container_width=True)
    with r2:
        if 'Number_of_Casualties' in df and 'Accident_Severity' in df:
            fig = style_chart(px.box(df, x='Accident_Severity', y='Number_of_Casualties', title="⚕️ Casualties vs Severity", color='Accident_Severity'))
            st.plotly_chart(fig, use_container_width=True)
            
    if 'State' in df and 'Number_of_Casualties' in df:
        st_cas = df.groupby('State')['Number_of_Casualties'].sum().reset_index().sort_values('Number_of_Casualties', ascending=False).head(15)
        fig = style_chart(px.bar(st_cas, x='State', y='Number_of_Casualties', title="🗺️ Casualties by State", text='Number_of_Casualties', color='Number_of_Casualties', color_continuous_scale="Reds"))
        st.plotly_chart(fig, use_container_width=True)

elif menu == "4️⃣ Vehicle Analytics":
    st.title("🚙 Vehicle Involvement Intelligence")
    
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total Vehicles Involved", f"{df['Number_of_Vehicles'].sum():,}" if 'Number_of_Vehicles' in df else "N/A")
    with c2: kpi_card("Highest Vehicle Type", str(df['Vehicle_Type'].mode()[0]) if 'Vehicle_Type' in df else "N/A")
    with c3: kpi_card("Highest Risk Vehicle", str(df[df['Accident_Risk']=='High']['Vehicle_Type'].mode()[0]) if 'Accident_Risk' in df and 'Vehicle_Type' in df else "N/A")
    
    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        if 'Vehicle_Type' in df and 'Accident_Severity' in df:
            fig = style_chart(px.histogram(df, x='Vehicle_Type', color='Accident_Severity', barmode='group', title="🚦 Vehicle vs Severity"))
            st.plotly_chart(fig, use_container_width=True)
    with r2:
        if 'Vehicle_Type' in df and 'Road_Type' in df:
            fig = style_chart(px.density_heatmap(df, x='Vehicle_Type', y='Road_Type', title="🔥 Vehicle vs Road Type Heatmap", color_continuous_scale="Viridis"))
            st.plotly_chart(fig, use_container_width=True)
            
    if 'Vehicle_Type' in df:
        fig = style_chart(px.treemap(df.dropna(subset=['Vehicle_Type', 'Accident_Risk']), path=[px.Constant("Vehicles"), 'Vehicle_Type', 'Accident_Risk'], title="🌳 Vehicle Risk Treemap"))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "5️⃣ Location Analytics":
    st.title("📍 Geographical Location Analytics")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("States", f"{df['State'].nunique():,}" if 'State' in df else "0")
    with c2: kpi_card("Cities", f"{df['City'].nunique():,}" if 'City' in df else "0")
    with c3: kpi_card("Urban Cases", f"{len(df[df['Urban_or_Rural_Area']=='Urban']):,}" if 'Urban_or_Rural_Area' in df else "0")
    with c4: kpi_card("Rural Cases", f"{len(df[df['Urban_or_Rural_Area']=='Rural']):,}" if 'Urban_or_Rural_Area' in df else "0")
    
    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        if 'Urban_or_Rural_Area' in df:
            fig = style_chart(px.pie(df, names='Urban_or_Rural_Area', title="🏙️ Urban vs Rural Distribution", hole=0.5, color_discrete_sequence=['#FF4B4B', '#00BFFF']))
            st.plotly_chart(fig, use_container_width=True)
    with r2:
        if 'City' in df:
            city_df = df['City'].value_counts().head(15).reset_index()
            fig = style_chart(px.bar(city_df, x='count', y='City', orientation='h', title="🏢 Top 15 Cities", color='count', color_continuous_scale="Plasma"))
            st.plotly_chart(fig, use_container_width=True)

    if 'State' in df and 'City' in df:
        fig = style_chart(px.treemap(df.dropna(subset=['State', 'City']), path=[px.Constant("India"), 'State', 'City'], title="🗺️ Location Treemap (States & Cities)"))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "6️⃣ Risk & Environment":
    st.title("🌪️ Risk, Weather & Environment Insights")
    
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("High Risk Cases", f"{len(df[df['Accident_Risk']=='High']):,}" if 'Accident_Risk' in df else "N/A")
    with c2: kpi_card("Most Common Weather", str(df['Weather_Conditions'].mode()[0]) if 'Weather_Conditions' in df else "N/A")
    with c3: kpi_card("Holiday Effects", f"{len(df[df['Holiday']=='Yes']):,}" if 'Holiday' in df else "N/A")
    
    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        if 'Weather_Conditions' in df:
            fig = style_chart(px.bar(df['Weather_Conditions'].value_counts().reset_index(), x='Weather_Conditions', y='count', title="🌧️ Weather Impact", color='count', color_continuous_scale="Teal"))
            st.plotly_chart(fig, use_container_width=True)
    with r2:
        if 'Light_Conditions' in df:
            fig = style_chart(px.pie(df, names='Light_Conditions', title="💡 Light Conditions Impact", hole=0.3, color_discrete_sequence=px.colors.sequential.matter))
            st.plotly_chart(fig, use_container_width=True)
            
    if 'Time_of_Day' in df and 'Accident_Risk' in df:
        fig = style_chart(px.histogram(df, x='Time_of_Day', color='Accident_Risk', barmode='stack', title="⏰ Time of Day vs Risk"))
        st.plotly_chart(fig, use_container_width=True)


elif menu == "7️⃣ Dataset & About":
    tab1, tab2 = st.tabs(["📂 Dataset Explorer", "ℹ️ About Project"])
    
    with tab1:
        st.subheader("Dataset Overview")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Rows", df.shape[0])
        d2.metric("Total Columns", df.shape[1])
        d3.metric("Missing Values", df.isnull().sum().sum())
        d4.metric("Duplicate Rows", df.duplicated().sum())
        
        st.markdown("---")
        st.subheader("Interactive Dataset Preview")
        search_col = st.selectbox("Search by Column", df.columns)
        search_val = st.text_input(f"Enter value to search in {search_col}")
        
        show_df = df.copy()
        if search_val:
            show_df = show_df[show_df[search_col].astype(str).str.contains(search_val, case=False, na=False)]
        
        st.dataframe(show_df.head(500), use_container_width=True)
        
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=show_df.to_csv(index=False).encode('utf-8'),
            file_name='filtered_accident_data.csv',
            mime='text/csv',
        )
        
        st.markdown("---")
        st.subheader("🔥 Correlation Matrix")
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            corr_fig = style_chart(px.imshow(numeric_df.corr(), text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r"))
            st.plotly_chart(corr_fig, use_container_width=True)

    with tab2:
        st.markdown("""
        ###  Project Overview
        This **Road Accident Intelligence Dashboard** is an enterprise-grade Business Intelligence application designed to analyze complex traffic and accident datasets. It transforms raw data into actionable visual insights regarding severity, demographics, vehicles, locations, and environmental risks.
        
        ### Technologies Used
        *   **Frontend & Framework:** Streamlit
        *   **Data Manipulation:** Pandas, NumPy
        *   **Data Visualization:** Plotly Express, Plotly Graph Objects
        *   **Styling:** Custom CSS (Glassmorphism, Dark Theme)
        
        ### Dashboard Modules
        1.  **Home Dashboard:** Executive overview and high-level KPIs.
        2.  **Accident Analytics:** In-depth severity and road-type analysis.
        3.  **Victim Analytics:** Demographic breakdown of casualties.
        4.  **Vehicle Analytics:** Evaluation of vehicle types and associated risks.
        5.  **Location Analytics:** Geographical mapping using treemaps and bar charts.
        6.  **Risk & Environment:** Impact of weather, light, and seasons.
        7.  **Dataset Explorer:** Live interactive data preview, cleaning reports, and downloads.
        
        ### Developer Details
        *   **Developed for:** Data Analytics & BI Portfolio
        *   **UI/UX Standard:** Enterprise Corporate Level
        """)