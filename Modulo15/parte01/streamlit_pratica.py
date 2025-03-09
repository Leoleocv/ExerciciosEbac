import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import time


st.set_page_config(
    page_title="Pratica Streamlit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
@st.cache_data
def load_data():
    
    df = df = pd.read_csv('./input/SINASC_RO_2019.csv')
    df.DTNASC = pd.to_datetime(df.DTNASC)
    
    return df


if 'contador' not in st.session_state:
    st.session_state.contador = 0

if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

def incrementar_contador():
    st.session_state.contador += 1

def adicionar_favorito(item):
    if item not in st.session_state.favoritos:
        st.session_state.favoritos.append(item)



@st.cache_data
def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    fig, ax = plt.subplots(figsize=[15, 5])
    
    pivot = pd.pivot_table(df, values=value, index=index, aggfunc=func)

    if opcao == 'nada':
        pivot.plot(ax=ax)
    elif opcao == 'unstack':
        pivot.unstack().plot(ax=ax)
    elif opcao == 'sort':
        pivot.sort_values(value).plot(ax=ax)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    
    plt.tight_layout()

    st.pyplot(fig)
    
    return None


with st.sidebar:
    st.title("Menu")
    pagina = st.radio(
        "Selecione uma página:",
        ["Pagina inicial", "Visualização de Dados", "Widget exemplo", "Cache e Performance", "Session State"]
    )
    
    st.divider()

    with st.expander("Sobre esta aplicação"):
        st.write("Esta aplicação demonstra algumas funcionalidades do Streamlit.")
        st.info("Criada para fins de pratica sobre as funcionalidades do Streamlit.")
    
    st.write("Status da sessão:")
    st.write(f"Contador: {st.session_state.contador}")

    if st.button("Incrementar Contador", on_click=incrementar_contador):
        pass


st.title("Pratica de Streamlit de acordo com a Tarefa 01 do Modulo 15!")
st.subheader("Enunciado:")
st.caption("leia o conteúdo da documentação e crie uma aplicação com streamlit reproduzindo pelo menos 20 códigos extraídos das páginas.")

df = load_data()

if pagina == "Pagina inicial":
    st.title("Pagina inicial")

    st.subheader("Resumo dos Dados")
    st.dataframe(df.describe(), use_container_width=True)
        
        

elif pagina == "Visualização de Dados":
    st.subheader("Explorando Gráficos")
    
    viz_type = st.selectbox(
        "Escolha um gráfico para visualizar:",
        ["Média da idade da mãe por data", "média idade mae, divisao de sexo do bebe", "Média peso bebe x data", "Peso mediano bebe x escolaridade da mae", "APGAR1 médio x tempo de gestação"]
    )
    
    if viz_type == "Média da idade da mãe por data":
        st.subheader("Média da idade da mãe por data")
        
        plota_pivot_table(df, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
        
        
    elif viz_type == "média idade mae, divisao de sexo do bebe":
        st.subheader("média idade mae")
        
        plota_pivot_table(df, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
        
        
    elif viz_type == "Média peso bebe x data":
        st.subheader("Média peso bebe")
        
        plota_pivot_table(df, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
        
        
    elif viz_type == "Peso mediano bebe x escolaridade da mae":
        st.subheader("Peso mediano bebe")
        
        plota_pivot_table(df, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
                
    elif viz_type == "APGAR1 médio x tempo de gestação":
        st.subheader("APGAR1 médio")
        
        plota_pivot_table(df, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')

elif pagina == "Widget exemplo":
    st.title("Widgets exemplo")
    
    peso_min = st.slider("Peso mínimo do bebê", int(df['PESO'].min()), int(df['PESO'].max()), int(df['PESO'].min()))
    
    df_filtrado = df[df['PESO'] >= peso_min]
    
    st.dataframe(df_filtrado, use_container_width=True)

elif pagina == "Cache e Performance":
    st.title("Cache e Performance")
    start_time = time.time()
    _ = load_data()
    first_load_time = time.time() - start_time
    st.metric("Tempo de carregamento (s)", f"{first_load_time:.6f}")

elif pagina == "Session State":
    st.subheader("Demonstração de Session State")
    
    st.write(f"Valor atual do contador: {st.session_state.contador}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Incrementar"):
            
            st.session_state.contador += 1
            
            st.rerun()
    
    with col2:
        if st.button("Decrementar"):
            
            st.session_state.contador -= 1
            
            st.rerun()
    
    with col3:
        if st.button("Zerar"):
           
            st.session_state.contador = 0
            st.rerun()

    st.subheader("Lista de Favoritos")
    
    novo_favorito = st.text_input("Adicione um novo item aos favoritos")
    
    if st.button("Adicionar item") and novo_favorito:
        
        adicionar_favorito(novo_favorito)
        
        st.rerun()
    
    if st.session_state.favoritos:
        
        st.write("Seus itens favoritos:")
        
        for i, fav in enumerate(st.session_state.favoritos):
            
            st.write(f"{i+1}. {fav}")
    
    else:
        st.info("Você ainda não adicionou nenhum item aos favoritos.")
    
    if st.button("Limpar favoritos"):
        
        st.session_state.favoritos = []
        
        st.rerun()
    
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'questions': [
                {'question': 'Qual é a capital de Rondônia?', 'answer': 'Porto Velho'},
                {'question': 'Qual é a moeda do Brasil?', 'answer': 'Real'},
                {'question': 'Qual o maior rio do Brasil?', 'answer': 'Amazonas'}
            ],
            'completed': False
        }


    st.subheader("Quiz Simples")

    if not st.session_state.quiz_state['completed']:
        current = st.session_state.quiz_state['current_question']
        question = st.session_state.quiz_state['questions'][current]
    
        st.write(f"Questão {current + 1} de {len(st.session_state.quiz_state['questions'])}")
        st.write(question['question'])
    
        user_answer = st.text_input("Sua resposta:", key=f"quiz_answer_{current}")
    
    if st.button("Verificar Resposta"):
        if user_answer.lower() == question['answer'].lower():
            st.success("Correto!")
            st.session_state.quiz_state['score'] += 1
        else:
            st.error(f"Incorreto. A resposta correta é: {question['answer']}")
        
        if current < len(st.session_state.quiz_state['questions']) - 1:
            st.session_state.quiz_state['current_question'] += 1
        else:
            st.session_state.quiz_state['completed'] = True
        
        st.rerun()
    else:
        st.success(f"Sua pontuação: {st.session_state.quiz_state['score']} de {len(st.session_state.quiz_state['questions'])}")
    
    if st.button("Reiniciar Quiz"):
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'questions': st.session_state.quiz_state['questions'],
            'completed': False
        }
        st.rerun()

  

st.divider()
with st.container():
    st.caption("Pratica com as funcionalidades do Streamlit")
    st.write("Pratica utilizando widgets, visualizações, cache e session state")

    