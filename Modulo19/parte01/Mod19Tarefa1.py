import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def multiselect_filter(dataframe, column, selected_values):
    
    if 'all' in selected_values:
        return dataframe
    else:
        return dataframe[dataframe[column].isin(selected_values)].reset_index(drop=True)

def main():
 
    st.set_page_config(
        page_title='Tips dataset streamlit pratica', 
        layout="wide",
        initial_sidebar_state='expanded'
    )
    
    st.write('# Tips Dataset')
    st.markdown("---")

    tips_raw = sns.load_dataset('tips')
    tips = tips_raw.copy()

    with st.sidebar.form(key='analise'):

        max_bill = float(tips['total_bill'].max())
        min_bill = float(tips['total_bill'].min())
        
        bill_range = st.slider(
            label='Faixa de valor da conta', 
            min_value=min_bill,
            max_value=max_bill, 
            value=(min_bill, max_bill),
            step=0.1
        )

        days_list = tips['day'].unique().tolist()
        days_list.append('all')
        days_selected = st.multiselect(
            "Selecione os dias", 
            days_list, 
            ['all']
        )

        time_options = ['all'] + tips['time'].unique().tolist()
        time_selected = st.radio(
            "Selecione tempo do dia", 
            time_options
        )

        size_list = tips['size'].unique().tolist()
        size_list.append('all')
        size_selected = st.multiselect(
            "Selecione o tamanho da mesa", 
            size_list, 
            ['all']
        )

        submit_button = st.form_submit_button(label='Aplicar')

    filtered_tips = tips[
        (tips['total_bill'] >= bill_range[0]) & 
        (tips['total_bill'] <= bill_range[1])
    ]
    
    filtered_tips = multiselect_filter(filtered_tips, 'day', days_selected)
    filtered_tips = multiselect_filter(filtered_tips, 'size', size_selected)
    
    if time_selected != 'all':
        filtered_tips = filtered_tips[filtered_tips['time'] == time_selected]

    st.write('## Dataset Overview')
    col1, col2 = st.columns(2)
    
    with col1:
        st.write('### Dataset original')
        st.dataframe(tips_raw.head())
    
    with col2:
        st.write('### Dataset filtrado')
        st.dataframe(filtered_tips.head())

    st.markdown("---")
    st.write('## Visualização dos dados')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    sns.histplot(tips_raw['tip'], kde=True, ax=ax1)
    ax1.set_title('Distribuição gorjeta (tips original)', fontweight='bold')
    ax1.set_xlabel('quantia da gorjeta')

    sns.histplot(filtered_tips['tip'], kde=True, ax=ax2)
    ax2.set_title('Distribuição gorjeta (tips filtrado)', fontweight='bold')
    ax2.set_xlabel('quantia da gorjeta')
    
    st.pyplot(plt)

    st.markdown("---")
    st.write('## Resumo estatisticas')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write('### summary do dataset nao filtrado')
        st.write(tips_raw.describe())
    
    with col2:
        st.write('### summary dataset filtrado')
        st.write(filtered_tips.describe())

if __name__ == '__main__':
    main()