import base64
import datetime
import streamlit as st
import pandas as pd

# Carrega o arquivo csv com os dados dos pacientes, caso ele exista
try:
    df = pd.read_csv('dados_pacientes.csv', index_col=0)
except FileNotFoundError:
    df = pd.DataFrame(columns=['CPF', 'Nome Completo', 'Nome da Mãe', 'Endereço', 'CEP', 'Data de Nascimento'])

# Define a função para cadastrar um novo paciente
def cadastrar_paciente(cpf, nome, mae, endereco, cep, dn):
    # Verifica se o paciente já existe no DataFrame
    global df
    if cpf in df['CPF'].values:
        st.warning("Este CPF já está cadastrado.")
    # Verifica se todos os campos foram preenchidos corretamente
    elif cpf and nome and mae and endereco and cep and dn:
        # Cria um novo DataFrame com os dados do novo paciente
        novo_paciente = pd.DataFrame({
            "CPF": [cpf],
            "Nome Completo": [nome],
            "Nome da Mãe": [mae],
            "Endereço": [endereco],
            "CEP": [cep],
            "Data de Nascimento": [dn]
        })
        # Adiciona o novo paciente ao DataFrame principal
        df = pd.concat([df, novo_paciente], ignore_index=True)
        # Salva os dados atualizados no arquivo csv
        df.to_csv('dados_pacientes.csv')
        st.success("Paciente cadastrado com sucesso!")
    else:
        st.warning("Por favor, preencha todos os campos corretamente.")

# Define a página para cadastrar um novo paciente
def cadastrar():
    global df
    st.title("Cadastro de Paciente")
    cpf = st.text_input('CPF')
    nome = st.text_input('Nome Completo')
    mae = st.text_input('Nome da Mãe')
    endereco = st.text_input('Endereço')
    cep = st.text_input('CEP')
    dn = st.date_input('Data de Nascimento', min_value=datetime.date(1900, 1, 1))
    if st.button('Cadastrar'):
        cadastrar_paciente(cpf, nome, mae, endereco, cep, dn)

# Define a página para visualizar os dados dos pacientes
def visualizar():
    global df
    st.title("Visualizar Pacientes")
    
    # Verifica se há pacientes cadastrados
    if len(df) > 0:
        # Exibe os dados dos pacientes em uma tabela
        st.table(df)
        # Adiciona um botão para fazer o download do arquivo csv
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="dados_pacientes.csv">Download do arquivo CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Nenhum paciente cadastrado.")

def pesquisar():
    global df
    st.title("Pesquisar Pacientes")
    # Cria um campo de texto para o usuário inserir o valor a ser pesquisado
    search_term = st.text_input("Digite o valor a ser pesquisado:")
    # Verifica se o campo de pesquisa foi preenchido
    if search_term:
        # Filtra o DataFrame com base no valor de pesquisa em todas as colunas
        search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]
        # Verifica se há resultados da pesquisa
        if len(search_results) > 0:
            # Exibe os resultados da pesquisa em uma tabela
            st.table(search_results)
        else:
            st.warning("Nenhum resultado encontrado.")

# Define a página principal da aplicação
def main():
    st.set_page_config(page_title="Cadastro Conecte SUS", page_icon=":heart:", layout="wide")
    st.title("Cadastro Conecte SUS")
    menu = st.sidebar.selectbox("Selecione uma opção:", ("Cadastro de Paciente", "Visualizar Pacientes", "Pesquisar Pacientes"))
    if menu == "Cadastro de Paciente":
        cadastrar()
    elif menu == "Visualizar Pacientes":
        visualizar()
    elif menu == "Pesquisar Pacientes":
        pesquisar()
if __name__ == '__main__':
    main()
