import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(
    page_title="Prática Streamlit analise de dados - upload e download",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Análise de Dados Interativa")
st.markdown("---")

@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file, sep=None, encoding='utf-8') 
        
        elif file.name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file, sep=';', encoding='utf-8')
        
        else:
            st.error("Formato não suportado!")
            
            return None
    
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        
        return None

@st.cache_data
def to_excel(df):
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        
        df.to_excel(writer, index=False)
    
    return output.getvalue()

@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def get_image_download_link(fig, filename, text):
    
    buf = BytesIO()
    
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    
    buf.seek(0)
    
    b64 = base64.b64encode(buf.read()).decode()
    
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'

st.sidebar.header("📤 Upload de Dados")
uploaded_file = st.sidebar.file_uploader(
    
    "Carregue seu arquivo (CSV ou Excel)",
    
    type=['csv', 'xlsx', 'xls']
)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:

        st.sidebar.header("🔍 Filtros ")
        
        with st.sidebar.form("filters_form"):

            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                
                selected_num_col = st.selectbox("Coluna numérica para filtrar:", numeric_cols)
                
                min_val = float(df[selected_num_col].min())
                max_val = float(df[selected_num_col].max())
                
                val_range = st.slider(
                    f"Intervalo de {selected_num_col}",
                    min_val, max_val, (min_val, max_val)
                )

            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            cat_filters = {}
            for col in cat_cols:
                
                unique_vals = df[col].unique().tolist()
                
                selected_vals = st.multiselect(
                    f"Valores de {col}",
                    unique_vals,
                    default=unique_vals
                )
                
                cat_filters[col] = selected_vals

            st.sidebar.markdown("### Configurações de Visualização")
            
            chart_type = st.sidebar.selectbox(
                "Tipo de gráfico:",
                
                ["Barra", "Linha", "Histograma", "Boxplot", "Dispersão"]
            )
            
            submit_button = st.form_submit_button("Aplicar Filtros")

        filtered_df = df.copy()
        
        if numeric_cols:
            
            filtered_df = filtered_df[
                (filtered_df[selected_num_col] >= val_range[0]) & 
                (filtered_df[selected_num_col] <= val_range[1])
            ]
        
        for col, vals in cat_filters.items():
            
            if vals:
                filtered_df = filtered_df[filtered_df[col].isin(vals)]

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dados Originais")
            st.write(f"Total de registros: {len(df)}")
            st.dataframe(df.head())
        
        with col2:
            st.subheader("Dados Filtrados")
            st.write(f"🔍 Registros após filtros: {len(filtered_df)}")
            st.dataframe(filtered_df.head())
        
        st.markdown("---")

        st.subheader("Visualização dos Dados")

        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("Eixo X:", df.columns)
        
        with col2:
            y_axis = st.selectbox("Eixo Y:", [None] + df.columns.tolist())

        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == "Barra":
            if y_axis:
                
                sns.barplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
            
            else:
                
                filtered_df[x_axis].value_counts().plot(kind='bar', ax=ax)
            
            ax.set_title(f"Gráfico de Barras: {x_axis} {'vs ' + y_axis if y_axis else ''}")
        
        elif chart_type == "Linha":
            if y_axis:
                
                sns.lineplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
            
            else:
                
                st.warning("Selecione uma coluna para o eixo Y")
            
            ax.set_title(f"Gráfico de Linhas: {x_axis} vs {y_axis}")
        
        elif chart_type == "Histograma":
            
            sns.histplot(data=filtered_df, x=x_axis, kde=True, ax=ax)
            
            ax.set_title(f"Histograma de {x_axis}")
        
        elif chart_type == "Boxplot":
            if y_axis:
                
                sns.boxplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
            
            else:
                
                sns.boxplot(data=filtered_df, x=x_axis, ax=ax)
            
            ax.set_title(f"Boxplot: {x_axis} {'vs ' + y_axis if y_axis else ''}")
        
        elif chart_type == "Dispersão":
            if y_axis:
                
                sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
                
                ax.set_title(f"Gráfico de Dispersão: {x_axis} vs {y_axis}")
            
            else:
                
                st.warning("Selecione uma coluna para o eixo Y")

        st.pyplot(fig)

        st.markdown(get_image_download_link(
           
            fig, 
            
            f"grafico_{chart_type.lower()}.png", 
            
            "Download do Gráfico (PNG)"
        ), unsafe_allow_html=True)
        
        st.markdown("---")

        st.subheader("📥 Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Exportar dados filtrados (Excel)",
                
                data=to_excel(filtered_df),
                
                file_name="dados_filtrados.xlsx",
                
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            st.download_button(
                
                label="Exportar dados filtrados (CSV)",
                
                data=to_csv(filtered_df),
                
                file_name="dados_filtrados.csv",
                
                mime="text/csv"
            )

        st.markdown("---")
        st.subheader("Estatísticas")
        st.dataframe(filtered_df.describe())
        
else:
    st.info("ℹ️ Faça upload de um arquivo para começar a análise")

st.markdown("---")
st.markdown("Prática com Streamlit - Módulo 19 - Tarefa 2")