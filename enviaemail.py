import streamlit as st
import pandas as pd
import os

# Nome do arquivo onde os dados serão armazenados
DATA_FILE = "agendamentos.csv"

# Função para carregar os agendamentos existentes
def carregar_agendamentos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Professor", "Data", "Horário", "Arquivo"])

# Função para salvar novos agendamentos
def salvar_agendamento(professor, data, horario, arquivo):
    df = carregar_agendamentos()
    novo_agendamento = pd.DataFrame([[professor, data, horario, arquivo]], 
                                    columns=["Professor", "Data", "Horário", "Arquivo"])
    df = pd.concat([df, novo_agendamento], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Interface do Streamlit
st.title("📅 Agendamento de Aulas - Professores")
st.write("Preencha as informações abaixo para agendar sua aula e enviar arquivos.")

# Formulário de agendamento
with st.form("agendamento_form"):
    professor = st.text_input("👨‍🏫 Nome do Professor")
    data = st.date_input("📆 Data da Aula")
    horario = st.time_input("⏰ Horário da Aula")
    arquivo = st.file_uploader("📂 Enviar Arquivo (opcional)", type=["pdf", "docx", "xlsx", "png", "jpg"])
    
    submit = st.form_submit_button("✅ Agendar Aula")

    if submit:
        if not professor or not data or not horario:
            st.warning("⚠️ Todos os campos obrigatórios devem ser preenchidos!")
        else:
            arquivo_nome = arquivo.name if arquivo else "Nenhum arquivo"
            salvar_agendamento(professor, data, horario, arquivo_nome)
            st.success(f"🎉 Aula de {professor} agendada para {data} às {horario}!")
            st.balloons()

# Mostrar todos os agendamentos
st.subheader("📋 Agendamentos Registrados")
df_agendamentos = carregar_agendamentos()
st.dataframe(df_agendamentos)

# Botão para baixar os agendamentos em CSV
csv = df_agendamentos.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Baixar Agendamentos em CSV", data=csv, file_name="agendamentos.csv", mime="text/csv")
