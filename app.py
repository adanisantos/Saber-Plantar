import streamlit as st
import google.generativeai as genai

# Inicializa o modelo Gemini e armazena-o em st.session_state para persistência
# Esta é a parte crucial para o erro que você está a ver.
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = genai.GenerativeModel('gemini-2.0-flash') # Modelo de visão para sugestões de vasos

   # --- Configuração da Página Streamlit (DEVE SER A PRIMEIRA CHAMADA DO ST) ---
st.set_page_config(page_title="Chatbot de Plantas", page_icon="🌿", layout="centered")

# --- Função para obter informações e sugestões de vasos da Gemini ---
def obter_informacao_planta(nome_planta):
    try:
        # Acessa o modelo a partir de st.session_state
        model = st.session_state["gemini_model"]
        prompt = [
            f"Forneça informações sobre os cuidados da planta chamada '{nome_planta}'. Seja conciso e relevante para um iniciante.",
            "Além disso, sugira 3 tipos de vasos que seriam adequados para essa planta, fornecendo uma breve descrição de cada um e incluindo, se possível, links para imagens desses vasos. Se não for possível um link direto, descreva o vaso de forma que uma busca por imagem seja fácil."
        ]
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao buscar informações sobre '{nome_planta}': {e}"

# --- Interface do Chatbot com Streamlit ---
st.title("🌿 Chatbot de Plantas com Gemini")
st.markdown("Pergunte-me sobre cuidados com plantas e sugestões de vasos!")

# Inicializa o histórico de mensagens na sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Olá! Pergunte-me sobre plantas."}]

# Exibe as mensagens do histórico
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Caixa de entrada para o usuário
if prompt := st.chat_input("Digite o nome de uma planta..."):
    # Adiciona a mensagem do usuário ao histórico e exibe
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Obtém a resposta do Gemini
    with st.spinner("Buscando informações..."): # Mostra um indicador de carregamento
        resposta_gemini = obter_informacao_planta(prompt)

    st.session_state["messages"].append({"role": "assistant", "content": resposta_gemini})
    st.chat_message("assistant").write(resposta_gemini)

