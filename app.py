import streamlit as st
import requests

st.set_page_config(page_title="Ateliê IA", page_icon="✦", layout="wide")

NUCLEI = {
    "Literatura e narrativa": ["Arquiteto de histórias", "Especialista em personagens", "Especialista em diálogos", "Editor literário"],
    "Ilustração e produção visual": ["Diretor de arte", "Designer de personagens", "Especialista em composição visual"],
    "Pesquisa e verificação": ["Pesquisador", "Verificador de fatos", "Analista de fontes"],
    "Produção acadêmica": ["Orientador acadêmico", "Especialista em estrutura textual", "Revisor acadêmico"],
    "Pesquisa científica": ["Pesquisador científico", "Analista metodológico", "Revisor científico"],
    "Finanças e economia": ["Analista financeiro", "Analista econômico", "Planejador financeiro"],
    "Negócios e gestão": ["Consultor de negócios", "Analista de processos", "Especialista em gestão"],
    "Psicologia e comportamento": ["Analista comportamental", "Pesquisador em psicologia", "Especialista em comunicação"],
    "Jurídico": ["Pesquisador jurídico", "Analista de documentos", "Organizador de argumentos"],
    "Revisão e qualidade": ["Revisor crítico", "Auditor de consistência", "Editor de clareza"],
    "Educação e pedagogia": ["Planejador educacional", "Criador de atividades", "Explicador didático"],
    "Jornalismo e comunicação": ["Repórter pesquisador", "Editor de texto", "Analista de comunicação"],
    "Documentação técnica": ["Redator técnico", "Organizador de documentação", "Revisor técnico"],
    "Tradução e localização": ["Tradutor", "Revisor de tradução", "Especialista em localização"],
    "História e cultura": ["Pesquisador histórico", "Analista cultural", "Curador de referências"],
    "Ciências sociais e políticas públicas": ["Pesquisador social", "Analista de políticas públicas", "Analista de dados sociais"],
    "Saúde e ciências da vida": ["Pesquisador em saúde", "Organizador de informação científica", "Revisor de conteúdo em saúde"],
    "Engenharia, arquitetura e construção": ["Analista de projetos", "Pesquisador técnico", "Revisor de especificações"],
    "Tecnologia e computação": ["Arquiteto de software", "Programador", "Analista de tecnologia"],
    "Dados e inteligência analítica": ["Analista de dados", "Especialista em métricas", "Intérprete de resultados"],
    "Meio ambiente e agricultura": ["Pesquisador ambiental", "Analista de sustentabilidade", "Especialista agro"],
    "Design, produto e UX": ["Designer de produto", "Pesquisador UX", "Especialista em experiência"],
    "Publicidade, conteúdo e comércio digital": ["Estrategista de conteúdo", "Copywriter", "Analista de marketing digital"],
    "Roteiro e audiovisual": ["Roteirista", "Editor de roteiro", "Consultor audiovisual"],
    "Jogos e experiências interativas": ["Game designer", "Designer narrativo", "Analista de mecânicas"],
    "Moda, beleza e estilo": ["Consultor de estilo", "Pesquisador de tendências", "Diretor criativo de moda"],
    "Viagem, turismo e hospitalidade": ["Planejador de viagens", "Pesquisador de destinos", "Consultor de hospitalidade"],
    "Gastronomia e alimentação": ["Pesquisador gastronômico", "Desenvolvedor de receitas", "Editor culinário"],
    "Artes, música e cultura criativa": ["Pesquisador artístico", "Curador criativo", "Consultor de linguagem artística"],
    "Esportes e desempenho físico": ["Analista esportivo", "Pesquisador de desempenho", "Planejador de treino informativo"],
    "Organização pessoal e produtividade": ["Planejador de projetos", "Organizador de rotinas", "Especialista em produtividade"],
}

MODES = ["Criar", "Pesquisar", "Analisar", "Planejar", "Revisar", "Criticar e sugerir melhorias", "Explicar"]

def call_gemini(messages, agents, nuclei, mode, director, review):
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None, "A interface está pronta, mas falta conectar uma chave gratuita da API Gemini. Ela será adicionada em Settings → Secrets no Streamlit, sem ficar exposta no código."
    agent_text = ", ".join(agents) if agents else "Assistente geral"
    system = f"""Você é o motor de uma plataforma de produção intelectual e criativa chamada Ateliê IA.
Núcleos escolhidos pelo usuário: {', '.join(nuclei) or 'nenhum'}.
Especialistas ativados explicitamente: {agent_text}.
Modo de trabalho: {mode}.
Diretor/orquestrador: {'ativado' if director else 'desativado'}.
Revisão: {'solicitada' if review else 'não solicitada'}.
Respeite rigorosamente a seleção: não invente agentes adicionais nem diga que especialistas inexistentes foram consultados.
Os especialistas devem contribuir apenas dentro de suas especialidades. Diferencie fatos confirmados, inferências e incertezas. Nunca invente fontes, dados ou citações. Em temas jurídicos, médicos e financeiros, informe limites e recomende validação profissional quando necessário.
Se o diretor estiver ativado, organize a resposta e integre perspectivas; caso contrário, responda de forma direta. Se revisão estiver ativada, finalize com uma breve checagem crítica e possíveis melhorias.
Responda em português do Brasil, salvo pedido diferente. Seja claro, útil e específico."""
    contents = [{"role":"user","parts":[{"text":system + "\n\nConversa:\n" + "\n".join([("Usuária: " if m["role"]=="user" else "Ateliê IA: ") + m["content"] for m in messages])}]}]
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    try:
        response = requests.post(url, params={"key":api_key}, json={"contents":contents, "generationConfig":{"temperature":0.8, "maxOutputTokens":4096}}, timeout=90)
        if response.status_code != 200:
            return None, f"A API respondeu com erro {response.status_code}: {response.text[:700]}"
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"], None
    except Exception as exc:
        return None, f"Não consegui acessar a API: {exc}"

st.markdown("""
<style>
.main {background:#fffafd}
[data-testid="stSidebar"] {background:#fff4f8}
h1 {color:#8f5274}
.stButton>button {border-radius:12px}
</style>
""", unsafe_allow_html=True)

st.title("✦ Ateliê IA")
st.caption("Um espaço de criação, pesquisa e trabalho com especialistas selecionados por você.")
with st.sidebar:
    st.header("Configurar equipe")
    chosen_nuclei = st.multiselect("Núcleos de trabalho", list(NUCLEI.keys()), default=["Literatura e narrativa"])
    available_agents = []
    for nucleus in chosen_nuclei:
        available_agents.extend(NUCLEI[nucleus])
    chosen_agents = st.multiselect("Especialistas que participarão", available_agents, default=available_agents[:2])
    mode = st.selectbox("O que a equipe fará?", MODES)
    director = st.toggle("Ativar diretor/orquestrador", value=False)
    review = st.toggle("Solicitar revisão crítica", value=False)
    st.divider()
    st.caption("A equipe só usa os núcleos e especialistas que você selecionar. A recomendação automática ainda não ativa ninguém sem sua aprovação.")

col1, col2 = st.columns([3,1])
with col1:
    st.subheader("Seu espaço de trabalho")
with col2:
    if st.button("Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.expander("Equipe selecionada", expanded=False):
    st.write("**Núcleos:** " + (", ".join(chosen_nuclei) if chosen_nuclei else "Nenhum selecionado"))
    st.write("**Especialistas:** " + (", ".join(chosen_agents) if chosen_agents else "Nenhum selecionado"))
    st.write("**Diretor:** " + ("Ativado" if director else "Desativado") + " · **Revisão:** " + ("Ativada" if review else "Desativada"))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Descreva o que você quer criar, descobrir ou resolver...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("A equipe está trabalhando..."):
            answer, error = call_gemini(st.session_state.messages, chosen_agents, chosen_nuclei, mode, director, review)
            if error:
                st.warning(error)
                st.markdown("**Enquanto isso:** você já pode explorar os núcleos e montar sua equipe. A conversa com IA será liberada assim que a chave for conectada.")
                st.session_state.messages.append({"role":"assistant","content":error})
            else:
                st.markdown(answer)
                st.session_state.messages.append({"role":"assistant","content":answer})

st.divider()
st.caption("Versão inicial de testes · As equipes salvas, colaboração multiagente avançada, editor visual e geração de imagens serão adicionados nas próximas etapas.")
