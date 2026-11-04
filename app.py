import streamlit as st
import requests
import json

st.set_page_config(page_title="Ateliê IA", page_icon="✦", layout="wide")

# Cada especialista tem uma responsabilidade principal. O modo de trabalho define a tarefa desta rodada.
NUCLEI = {
    "Literatura e narrativa": [
        ("Arquiteto de histórias", "Estrutura, enredo, ritmo, conflitos e coerência da narrativa."),
        ("Especialista em personagens", "Personalidade, motivações, passado, relações, arco e consistência dos personagens."),
        ("Especialista em diálogos", "Voz individual, subtexto, naturalidade, tensão e ritmo das conversas."),
        ("Editor literário", "Qualidade da prosa, estilo, fluidez, ritmo e força emocional."),
    ],
    "Ilustração e produção visual": [
        ("Diretor de arte", "Conceito visual, linguagem estética, referências e unidade artística."),
        ("Designer de personagens", "Aparência, figurino, silhueta, expressões e continuidade visual."),
        ("Compositor visual", "Enquadramento, composição, luz, cor e leitura da imagem."),
    ],
    "Pesquisa e verificação": [
        ("Pesquisador", "Localiza e organiza informações relevantes para responder à pergunta."),
        ("Verificador de fatos", "Examina afirmações, datas, números e possíveis contradições."),
        ("Analista de fontes", "Avalia origem, confiabilidade, limitações e qualidade das evidências."),
    ],
    "Produção acadêmica": [
        ("Orientador acadêmico", "Problema, objetivos, estrutura, argumentação e adequação acadêmica."),
        ("Especialista em metodologia", "Métodos, procedimentos, variáveis e coerência metodológica."),
        ("Revisor acadêmico", "Clareza, coesão, linguagem formal e normas indicadas pelo usuário."),
    ],
    "Pesquisa científica": [
        ("Pesquisador científico", "Conceitos, literatura científica e estado do conhecimento."),
        ("Analista metodológico", "Desenho de pesquisa, amostra, método, limitações e validade."),
        ("Revisor científico", "Coerência entre hipótese, método, resultados e conclusões."),
    ],
    "Finanças e economia": [
        ("Analista financeiro", "Orçamento, custos, indicadores e cenários financeiros."),
        ("Analista econômico", "Mercados, conjuntura, incentivos e relações econômicas."),
        ("Planejador financeiro", "Metas, organização financeira e comparação de cenários."),
    ],
    "Negócios e gestão": [
        ("Estrategista de negócios", "Modelo de negócio, posicionamento, oportunidades e estratégia."),
        ("Analista de processos", "Fluxos de trabalho, gargalos, eficiência e melhoria operacional."),
        ("Especialista em gestão", "Planejamento, metas, equipes e tomada de decisão."),
    ],
    "Psicologia e comportamento": [
        ("Pesquisador em psicologia", "Conceitos e evidências da literatura psicológica."),
        ("Analista comportamental", "Hábitos, motivação, decisões e padrões de comportamento."),
        ("Especialista em comunicação", "Relações interpessoais, escuta e comunicação assertiva."),
    ],
    "Jurídico": [
        ("Pesquisador jurídico", "Pesquisa de legislação, doutrina e entendimentos jurídicos."),
        ("Analista de legislação", "Interpretação textual, requisitos e relações entre normas."),
        ("Revisor de documentos jurídicos", "Organização, clareza e identificação de pontos que exigem revisão."),
    ],
    "Revisão e qualidade": [
        ("Revisor de conteúdo", "Gramática, clareza, coesão e precisão da linguagem."),
        ("Auditor de consistência", "Contradições, lacunas, premissas e continuidade interna."),
        ("Crítico especializado", "Avaliação rigorosa segundo critérios definidos para o trabalho."),
    ],
    "Educação e pedagogia": [
        ("Designer instrucional", "Objetivos de aprendizagem, sequência didática e materiais."),
        ("Especialista em aprendizagem", "Explicações, prática, progressão e dificuldades comuns."),
        ("Tutor", "Acompanhamento didático e explicações adaptadas à dúvida."),
    ],
    "Jornalismo e comunicação": [
        ("Pesquisador jornalístico", "Apuração, contexto, perguntas e organização de informações."),
        ("Editor jornalístico", "Estrutura, clareza, precisão e adequação ao público."),
        ("Analista de comunicação", "Mensagem, público, canal e estratégia comunicacional."),
    ],
    "Documentação técnica": [
        ("Redator técnico", "Instruções, manuais e explicações técnicas claras."),
        ("Arquiteto de documentação", "Estrutura, navegação, organização e padrões documentais."),
        ("Revisor técnico", "Precisão terminológica, completude e consistência."),
    ],
    "Tradução e localização": [
        ("Tradutor", "Tradução fiel ao sentido, contexto e intenção do original."),
        ("Revisor linguístico", "Naturalidade, gramática, registro e consistência terminológica."),
        ("Especialista em localização", "Adaptação cultural, regional e contextual."),
    ],
    "História e cultura": [
        ("Pesquisador histórico", "Contexto temporal, acontecimentos e interpretação histórica."),
        ("Analista cultural", "Símbolos, práticas, valores e contextos culturais."),
        ("Curador de referências", "Seleção e organização de referências culturais relevantes."),
    ],
    "Ciências sociais e políticas públicas": [
        ("Pesquisador social", "Fenômenos sociais, conceitos e evidências."),
        ("Analista de políticas públicas", "Problemas públicos, desenho, implementação e avaliação."),
        ("Analista de dados sociais", "Indicadores, tendências e limites de interpretação."),
    ],
    "Saúde e ciências da vida": [
        ("Pesquisador em saúde", "Literatura e conceitos científicos relacionados à saúde."),
        ("Analista de evidências", "Qualidade, limitações e força das evidências científicas."),
        ("Educador em saúde", "Explicações acessíveis, prevenção e informação responsável."),
    ],
    "Engenharia, arquitetura e construção": [
        ("Analista de engenharia", "Princípios técnicos, requisitos e alternativas de solução."),
        ("Especialista em projetos", "Escopo, etapas, compatibilização e documentação."),
        ("Revisor de especificações", "Coerência, requisitos, riscos e pontos a validar tecnicamente."),
    ],
    "Tecnologia e computação": [
        ("Arquiteto de software", "Estrutura de sistemas, componentes e decisões técnicas."),
        ("Desenvolvedor", "Implementação, depuração e explicação de código."),
        ("Analista de sistemas", "Requisitos, fluxos, integrações e comportamento esperado."),
    ],
    "Dados e inteligência analítica": [
        ("Analista de dados", "Limpeza, exploração e interpretação de dados."),
        ("Especialista em métricas", "Indicadores, definições, comparações e acompanhamento."),
        ("Especialista em visualização", "Gráficos, tabelas e comunicação de resultados."),
    ],
    "Meio ambiente e agricultura": [
        ("Pesquisador ambiental", "Ecossistemas, impactos e evidências ambientais."),
        ("Analista de sustentabilidade", "Indicadores, impactos e práticas sustentáveis."),
        ("Especialista agro", "Sistemas agrícolas, produção e informação técnica."),
    ],
    "Design, produto e UX": [
        ("Designer de produto", "Funcionalidade, estrutura e experiência do produto."),
        ("Pesquisador UX", "Necessidades, comportamento e pesquisa com usuários."),
        ("Especialista em usabilidade", "Fluxos, acessibilidade, clareza e facilidade de uso."),
    ],
    "Publicidade, conteúdo e comércio digital": [
        ("Estrategista de conteúdo", "Pilares editoriais, formatos, calendário e distribuição."),
        ("Copywriter", "Textos persuasivos, títulos, chamadas e páginas de venda."),
        ("Analista de comércio digital", "Jornada de compra, catálogo, conversão e canais digitais."),
    ],
    "Roteiro e audiovisual": [
        ("Roteirista", "Premissa, estrutura, cenas, diálogos e progressão dramática."),
        ("Editor de roteiro", "Ritmo, clareza, continuidade e força das cenas."),
        ("Consultor audiovisual", "Linguagem de câmera, som, montagem e execução visual."),
    ],
    "Games e experiências interativas": [
        ("Game designer", "Regras, sistemas, progressão e experiência de jogo."),
        ("Designer narrativo", "História interativa, escolhas, personagens e ramificações."),
        ("Analista de mecânicas", "Equilíbrio, interação, feedback e clareza das regras."),
    ],
    "Moda, beleza e estilo": [
        ("Diretor criativo de moda", "Conceito, identidade visual e direção de coleção."),
        ("Consultor de estilo", "Combinações, proporção, ocasião e identidade pessoal."),
        ("Pesquisador de tendências", "Referências, movimentos e tendências de consumo."),
    ],
    "Viagens, turismo e hospitalidade": [
        ("Planejador de viagens", "Roteiros, logística, orçamento e prioridades."),
        ("Pesquisador de destinos", "Atrações, contexto local e informações práticas."),
        ("Consultor de hospitalidade", "Experiência do visitante e qualidade do serviço."),
    ],
    "Gastronomia e alimentação": [
        ("Desenvolvedor de receitas", "Ingredientes, técnicas, proporções e preparo."),
        ("Pesquisador gastronômico", "Culinária, ingredientes, tradições e referências."),
        ("Editor culinário", "Clareza de receitas, etapas e apresentação."),
    ],
    "Artes, música e cultura criativa": [
        ("Pesquisador de artes", "Movimentos, técnicas, obras e contextos artísticos."),
        ("Diretor criativo", "Conceito, linguagem e unidade de projetos criativos."),
        ("Crítico cultural", "Análise estética, contexto e interpretação crítica."),
    ],
    "Esportes e desempenho físico": [
        ("Analista esportivo", "Regras, desempenho, tática e contexto esportivo."),
        ("Pesquisador de desempenho", "Evidências sobre treinamento e desempenho físico."),
        ("Planejador de treinamento", "Organização geral de metas e rotinas, com limites de segurança."),
    ],
    "Organização pessoal e produtividade": [
        ("Planejador de projetos", "Etapas, prioridades, prazos e entregáveis."),
        ("Organizador de rotinas", "Rotinas, compromissos e organização prática."),
        ("Especialista em produtividade", "Foco, processos pessoais e redução de atrito."),
    ],
}

WORKFLOWS = {
    "Criar e desenvolver": {
        "description": "Para produzir algo novo a partir da sua ideia.",
        "tasks": ["Criar do zero", "Desenvolver uma ideia existente", "Escrever uma primeira versão", "Construir um projeto completo", "Criar alternativas diferentes"]
    },
    "Pesquisar e descobrir": {
        "description": "Para investigar um assunto e organizar conhecimento.",
        "tasks": ["Fazer uma pesquisa aprofundada", "Encontrar e organizar evidências", "Explicar um assunto", "Comparar opções ou abordagens", "Investigar uma pergunta específica"]
    },
    "Analisar e decidir": {
        "description": "Para entender problemas, avaliar cenários e tomar decisões.",
        "tasks": ["Analisar uma situação", "Identificar problemas e causas", "Avaliar riscos e oportunidades", "Comparar soluções", "Construir uma recomendação fundamentada"]
    },
    "Melhorar e revisar": {
        "description": "Para trabalhar em cima de um material que já existe.",
        "tasks": ["Revisar e corrigir", "Reescrever e aprimorar", "Fazer uma crítica detalhada", "Verificar coerência e qualidade", "Sugerir melhorias sem reescrever tudo"]
    },
    "Planejar e organizar": {
        "description": "Para transformar um objetivo em etapas concretas.",
        "tasks": ["Montar um plano de ação", "Estruturar etapas e cronograma", "Definir estratégia e prioridades", "Organizar informações e materiais", "Preparar uma execução passo a passo"]
    },
}

def get_api_key():
    typed_key = st.session_state.get("api_key_input", "").strip()
    if typed_key:
        return typed_key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""

def gemini_request(api_key, prompt, temperature=0.7):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    response = requests.post(
        url,
        params={"key": api_key},
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}],
              "generationConfig": {"temperature": temperature, "maxOutputTokens": 5000}},
        timeout=120,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Erro {response.status_code}: {response.text[:900]}")
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def run_team(api_key, user_prompt, nuclei, agents, workflow, task, director, review, history):
    context = ""
    if history:
        context = "\n\nCONTEXTO DA CONVERSA:\n" + "\n".join(
            ("Usuária: " if m["role"] == "user" else "Resultado anterior: ") + m["content"]
            for m in history[-6:]
        )
    task_brief = f"""PEDIDO DA USUÁRIA:
{user_prompt}

TIPO DE TRABALHO: {workflow}
TAREFA DESTA RODADA: {task}
NÚCLEOS SELECIONADOS: {', '.join(nuclei)}
{context}

REGRAS GERAIS:
- Responda em português do Brasil, salvo se a usuária pedir outro idioma.
- Não invente fatos, pesquisas, fontes, citações, estatísticas ou ações que não realizou.
- Separe fatos, hipóteses e incertezas quando isso fizer diferença.
- Não afirme que consultou a internet ou fontes externas se não fez isso.
- Respeite o escopo do especialista e o pedido da usuária.
"""
    contributions = []
    for name, specialty in agents:
        individual_prompt = f"""Você é o(a) especialista "{name}" do Ateliê IA.
SUA ÚNICA ESPECIALIDADE NESTA EQUIPE: {specialty}
Trabalhe somente nessa responsabilidade. Não tente assumir o papel dos outros especialistas.
{task_brief}
Entregue sua contribuição de forma concreta, completa e útil. Se algo estiver fora da sua especialidade, sinalize em vez de inventar.
"""
        contributions.append((name, gemini_request(api_key, individual_prompt)))
    if len(contributions) == 1 and not director and not review:
        return contributions[0][1], contributions
    synthesis = f"""Você é o integrador do Ateliê IA. Organize as contribuições abaixo para responder ao pedido da usuária.
{task_brief}
DIRETOR/ORQUESTRADOR: {"ATIVO — integre divergências e entregue uma resposta unificada." if director else "DESATIVADO — não assuma autoridade; apenas organize as contribuições sem apagar discordâncias relevantes."}
REVISÃO: {"ATIVA — faça uma revisão crítica de precisão, completude e clareza antes de finalizar." if review else "DESATIVADA — não acrescente uma etapa de revisão separada."}

CONTRIBUIÇÕES INDIVIDUAIS:
"""
    for name, contribution in contributions:
        synthesis += f"\n--- {name} ---\n{contribution}\n"
    synthesis += "\nEntregue a resposta final. Não invente consenso: mostre divergências relevantes e incertezas."
    final = gemini_request(api_key, synthesis, temperature=0.5)
    return final, contributions

# Visual
st.markdown("""
<style>
.block-container {padding-top: 1.8rem; max-width: 1250px;}
[data-testid="stSidebar"] {background: #fff4f8;}
.hero {padding: 1.35rem 1.55rem; border-radius: 18px; background: linear-gradient(115deg,#2b2037,#75445f); color: white; margin-bottom: 1.1rem;}
.hero h1 {color:white; margin:0; font-size:2.15rem;}
.hero p {color:#f8eaf1; margin:.35rem 0 0 0;}
.section-note {color:#756875; font-size:.92rem;}
div.stButton > button {border-radius:11px; min-height:2.6rem;}
/* Contraste dos campos e mensagens: funciona também em tema escuro. */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    color: #241b2b !important;
    -webkit-text-fill-color: #241b2b !important;
    border: 1px solid #b9a8b5 !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #766977 !important;
    -webkit-text-fill-color: #766977 !important;
    opacity: 1 !important;
}
div[data-testid="stAlert"] {
    border-radius: 10px !important;
}
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
    color: #29212b !important;
    -webkit-text-fill-color: #29212b !important;
}
div[data-testid="stAlert"][kind="warning"] {
    background: #fff2c6 !important;
    border: 1px solid #d6a62b !important;
}
div[data-testid="stAlert"][kind="success"] {
    background: #e5f5e9 !important;
    border: 1px solid #68a879 !important;
}
div[data-testid="stAlert"][kind="error"] {
    background: #fde8e8 !important;
    border: 1px solid #d77b7b !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>✦ Ateliê IA</h1><p>Você escolhe o trabalho, os núcleos e os especialistas. A equipe executa dentro do escopo definido por você.</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "saved_teams" not in st.session_state:
    st.session_state.saved_teams = {}
if "selected_agents" not in st.session_state:
    st.session_state.selected_agents = []
if "selected_nuclei" not in st.session_state:
    st.session_state.selected_nuclei = ["Literatura e narrativa"]

with st.sidebar:
    st.header("Conexão com IA")
    st.text_input("Chave Gemini API", type="password", key="api_key_input", placeholder="Cole sua chave aqui")
    st.caption("A chave é usada nesta sessão. Não a publique no GitHub.")
    if st.button("Testar conexão", use_container_width=True):
        key = get_api_key()
        if not key:
            st.warning("Primeiro cole sua chave Gemini.")
        else:
            try:
                test = gemini_request(key, "Responda apenas: conexão funcionando.", temperature=0)
                st.success("Conexão funcionando!")
            except Exception as e:
                st.error(str(e))
    st.divider()
    st.caption("A versão atual usa a API Gemini. A cota gratuita depende dos limites e das condições vigentes do Google.")

tabs = st.tabs(["Workspace", "Equipes", "Catálogo"])

with tabs[0]:
    st.subheader("1. O que você quer fazer?")
    st.caption("Escolha o tipo de trabalho. Depois selecione a tarefa específica.")
    workflow = st.radio("Tipo de trabalho", list(WORKFLOWS.keys()), horizontal=True, label_visibility="collapsed")
    st.info(WORKFLOWS[workflow]["description"])
    task = st.selectbox("Tarefa desta rodada", WORKFLOWS[workflow]["tasks"])

    st.divider()
    st.subheader("2. Quais áreas precisam participar?")
    st.caption("Você pode combinar quantos núcleos forem necessários. Nenhum núcleo é ativado sozinho.")
    selected_nuclei = st.multiselect("Selecionar núcleos", list(NUCLEI.keys()), default=st.session_state.selected_nuclei, placeholder="Comece digitando uma área...")
    st.session_state.selected_nuclei = selected_nuclei

    available = []
    for nucleus in selected_nuclei:
        for agent_name, specialty in NUCLEI[nucleus]:
            available.append((agent_name, specialty, nucleus))
    labels = [f"{name} · {nucleus}" for name, specialty, nucleus in available]
    label_to_agent = {f"{name} · {nucleus}": (name, specialty) for name, specialty, nucleus in available}
    default_labels = [label for label in labels if label.split(" · ")[0] in st.session_state.selected_agents]
    selected_labels = st.multiselect(
        "Selecionar especialistas",
        labels,
        default=default_labels,
        placeholder="Escolha quem vai trabalhar nesta tarefa...",
        help="Cada especialista tem uma responsabilidade principal. Selecione apenas os que fazem sentido para o trabalho."
    )
    selected_agents = [label_to_agent[label] for label in selected_labels]
    st.session_state.selected_agents = [name for name, specialty in selected_agents]

    if selected_agents:
        with st.expander("Entenda o papel de cada especialista selecionado", expanded=False):
            for name, specialty in selected_agents:
                st.markdown(f"**{name}**")
                st.caption(specialty)

    st.divider()
    st.subheader("3. Como a equipe deve trabalhar?")
    c1, c2 = st.columns(2)
    with c1:
        director = st.toggle("Diretor / orquestrador", value=False, help="Coordena e integra as contribuições. Não substitui sua decisão.")
    with c2:
        review = st.toggle("Revisão crítica final", value=True, help="Faz uma checagem adicional da resposta antes da entrega.")
    st.caption("Cada especialista recebe a tarefa dentro da própria especialidade. Quando há mais de um, as contribuições são reunidas em uma etapa final.")

    st.divider()
    st.subheader("4. Descreva o trabalho")
    prompt = st.text_area("Seu pedido", height=170, placeholder="Explique o que você precisa. Você pode colar um texto, apresentar uma ideia, fazer uma pergunta ou descrever um projeto.")
    extra = st.text_area("Contexto e orientações (opcional)", height=90, placeholder="Público, tom, tamanho, referências, restrições ou critérios...")
    full_prompt = prompt.strip()
    if extra.strip():
        full_prompt += "\n\nORIENTAÇÕES ADICIONAIS:\n" + extra.strip()

    can_run = bool(full_prompt and selected_agents)
    if st.button("✦ Executar equipe", type="primary", use_container_width=True, disabled=not can_run):
        api_key = get_api_key()
        if not api_key:
            st.error("A equipe está configurada, mas a conexão com a IA ainda não foi ativada. Cole uma chave Gemini no painel à esquerda e teste a conexão.")
        else:
            st.session_state.messages.append({"role": "user", "content": full_prompt})
            with st.spinner(f"{len(selected_agents)} especialista(s) trabalhando individualmente..."):
                try:
                    result, contributions = run_team(api_key, full_prompt, selected_nuclei, selected_agents, workflow, task, director, review, st.session_state.messages[:-1])
                    st.session_state.last_result = result
                    st.session_state.last_contributions = contributions
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    st.success("Trabalho concluído.")
                except Exception as e:
                    st.error(f"Não foi possível concluir: {e}")
    if st.session_state.get("last_result"):
        st.divider()
        st.subheader("Resultado do trabalho")
        st.markdown(st.session_state.last_result)
        st.download_button("Baixar resultado em Markdown", st.session_state.last_result, file_name="resultado_atelie.md", mime="text/markdown")
        with st.expander("Ver contribuições individuais dos especialistas"):
            for name, contribution in st.session_state.get("last_contributions", []):
                st.markdown(f"### {name}")
                st.markdown(contribution)

    st.divider()
    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = ""
        st.session_state.last_contributions = []
        st.rerun()

with tabs[1]:
    st.subheader("Equipes de trabalho")
    st.caption("Salve combinações de especialistas para reutilizar durante esta sessão. O salvamento permanente em conta será implementado depois.")
    team_name = st.text_input("Nome da equipe", placeholder="Ex.: Equipe de desenvolvimento de romances")
    if st.button("Salvar equipe atual", disabled=not (team_name.strip() and st.session_state.selected_agents)):
        st.session_state.saved_teams[team_name.strip()] = {
            "nuclei": list(st.session_state.selected_nuclei),
            "agents": list(st.session_state.selected_agents)
        }
        st.success(f"Equipe '{team_name}' salva nesta sessão.")
    if st.session_state.saved_teams:
        for name, team in st.session_state.saved_teams.items():
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.caption("Núcleos: " + ", ".join(team["nuclei"]))
                st.caption("Especialistas: " + ", ".join(team["agents"]))
                if st.button("Carregar equipe", key="load_"+name):
                    st.session_state.selected_nuclei = team["nuclei"]
                    st.session_state.selected_agents = team["agents"]
                    st.success("Equipe selecionada. Volte ao Workspace para continuar.")
    else:
        st.info("Você ainda não salvou nenhuma equipe nesta sessão.")

with tabs[2]:
    st.subheader("Catálogo dos 31 núcleos")
    st.caption("Abra uma área para conhecer os especialistas disponíveis e o foco principal de cada um.")
    for nucleus, agents in NUCLEI.items():
        with st.expander(f"{nucleus} · {len(agents)} especialistas"):
            for name, specialty in agents:
                st.markdown(f"**{name}**")
                st.write(specialty)

st.caption("Ateliê IA · protótipo em evolução. A chave Gemini e os limites gratuitos são administrados pelo provedor da API. Para decisões médicas, jurídicas ou financeiras, valide informações com profissionais habilitados.")
