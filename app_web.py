"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro e Desenvolvedor ADS)
Versão: V26.2 (Divisão Estrutural em Blocos + Quiz Dinâmico)
Ano: 2026
"""

import streamlit as st
import math
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="Central Analítica & ADS", page_icon="🖥️", layout="wide")

# ===================================================================
# 1. INICIALIZAÇÃO DO ESTADO GLOBAL (SESSION STATE)
# ===================================================================
if "tabela_usuarios" not in st.session_state:
    st.session_state["tabela_usuarios"] = {"marcio": "admin123", "professor": "ads2026"}
if "tabela_historico" not in st.session_state:
    st.session_state["tabela_historico"] = []
if "tabela_ranking" not in st.session_state:
    st.session_state["tabela_ranking"] = {"marcio": 1, "professor": 0}
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# Estados do Quiz Dinâmico Rotativo
if "indice_pergunta" not in st.session_state:
    st.session_state["indice_pergunta"] = 0
if "quiz_concluido" not in st.session_state:
    st.session_state["quiz_concluido"] = False

# Banco de dados de questões do Quiz de ADS & Engenharia
BANCO_QUESTOES = [
    {
        "pergunta": "Na arquitetura de computadores, o número decimal 10 equivale a qual representação binária?",
        "opcoes": ["A) 1001", "B) 1010", "C) 1100", "D) 1111"],
        "correta": "B"
    },
    {
        "pergunta": "Qual das seguintes estruturas de dados utiliza o princípio LIFO (Last In, First Out)?",
        "opcoes": ["A) Fila (Queue)", "B) Lista Encadeada", "C) Pilha (Stack)", "D) Árvore Binária"],
        "correta": "C"
    },
    {
        "pergunta": "Na Engenharia de Software, qual diagrama da UML é focado no aspecto comportamental e na interação de atores com o sistema?",
        "opcoes": ["A) Diagrama de Classes", "B) Diagrama de Casos de Uso", "C) Diagrama de Implantação", "D) Diagrama de Objetos"],
        "correta": "B"
    },
    {
        "pergunta": "Qual é a complexidade de tempo no pior caso para o algoritmo de ordenação Bubble Sort?",
        "opcoes": ["A) O(1)", "B) O(n log n)", "C) O(n)", "D) O(n²)"],
        "correta": "D"
    }
]

# ===================================================================
# 2. FUNÇÕES UTILITÁRIAS E ALGORÍTMICAS
# ===================================================================
def extrair_dados_do_arquivo(arquivo_carregado):
    try:
        nome_arquivo = arquivo_carregado.name
        df = pd.read_csv(arquivo_carregado, header=None) if nome_arquivo.endswith('.csv') else pd.read_excel(arquivo_carregado, header=None)
        dados = df.values.tolist()
        if len(dados) == 1:
            return [float(x) for x in dados[0] if pd.notna(x)], "sequencia"
        return [[float(x) for x in linha if pd.notna(x)] for linha in dados], "matriz"
    except Exception:
        st.error("Erro ao ler o arquivo.")
        return None, None

def processar_matriz_pura(matriz, escalar_mult=1.0):
    t_inicio = time.perf_counter()
    try:
        np_matriz = np.array(matriz, dtype=float) * escalar_mult
        num_linhas, num_colunas = np_matriz.shape
        transposta = np_matriz.T.tolist()
        det_txt = "N/A"
        if num_linhas == num_colunas and (num_linhas == 2 or num_linhas == 3):
            det_txt = f"{round(float(np.linalg.det(np_matriz)), 4)}"
        t_fim = time.perf_counter()
        delta_t = (t_fim - t_inicio) * 1000
        relatorio = f"**Dimensão:** {num_linhas}x{num_colunas} | **Determinante:** {det_txt} | **Média Global:** {round(float(np.mean(np_matriz)), 4)}"
        
        fig = plt.figure(figsize=(4, 2.5))
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(np.arange(0, num_colunas, 1), np.arange(0, num_linhas, 1))
        ax.plot_surface(X, Y, np_matriz, cmap="coolwarm", edgecolor='none', alpha=0.9)
        ax.set_title("Superfície 3D - Matriz A", fontsize=8, fontweight="bold")
        return relatorio, transposta, fig, delta_t
    except Exception as e:
        return f"Erro analítico matricial: {str(e)}", None, None, 0.0

def checar_convergencia_serie(sequencia):
    n = len(sequencia)
    if n < 3: return ""
    if all(abs(sequencia[i] - (1 / (i + 1))) < 0.05 for i in range(n)): return "\n\n**Série:** Harmônica Divergente."
    if all(x != 0 for x in sequencia):
        try:
            r_prop = sequencia[1] / sequencia[0]
            if abs(r_prop) < 1 and all(abs((sequencia[i] / sequencia[i-1]) - r_prop) < 0.01 for i in range(1, n)):
                return f"\n\n**Série:** Geométrica Convergente. Limite: **{round(sequencia[0]/(1-r_prop), 4)}**."
        except Exception: pass
    return ""

def identificar_padrao(sequencia):
    t_inicio = time.perf_counter()
    n = len(sequencia)
    if n < 3: return "Insira pelo menos 3 números.", None, 0.0
    serie_txt = checar_convergencia_serie(sequencia)
    
    p_termo = float(sequencia[0])
    arr = np.array(sequencia)
    estatisticas = (
        f"---  \n📊 **Painel Estatístico Descritivo (Módulo de Dados):**  \n"
        f"• Média Aritmética: {round(np.mean(arr), 4)} | • Mediana Central: {round(np.median(arr), 4)}  \n"
        f"• Desvio Padrão: {round(np.std(arr), 4)} | • Variância da Amostra: {round(np.var(arr), 4)}  \n"
        f"• Amplitude Máxima Total (Máx - Mín): {round(np.max(arr) - np.min(arr), 4)}"
    )
    resultado_padrao = "Padrão estrutural não reconhecido."
    proximo_num = None

    if all(isinstance(x, int) and x > 0 for x in sequencia):
        f_validos = [i for i in range(1, 14) if math.factorial(i) == int(p_termo)]
        if f_validos and all(sequencia[i] == math.factorial(f_validos[0] + i) for i in range(n)):
            resultado_padrao = f"Sequência Fatorial (n!){serie_txt}"
            proximo_num = math.factorial(f_validos[0] + n)
    if proximo_num is None and all(x >= 0 for x in sequencia) and (p_termo**0.5).is_integer():
        r_start = int(p_termo**0.5)
        if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
            resultado_padrao = f"Sequência de Quadrados Perfeitos (n²){serie_txt}"
            proximo_num = (r_start + n)**2
    if proximo_num is None and all(sequencia[i] == (round(p_termo**(1/3)) + i)**3 for i in range(n)):
        resultado_padrao = f"Sequência de Cubos Perfeitos (n³){serie_txt}"
        proximo_num = (round(p_termo**(1/3)) + n)**3
    if proximo_num is None and all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
        resultado_padrao = "Sequência de Fibonacci"
        proximo_num = sequencia[-1] + sequencia[-2]
    if proximo_num is None and n >= 2:
        razao_pa = sequencia[1] - sequencia[0]
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            resultado_padrao = f"Progressão Aritmética (PA) | Razão: {razao_pa}{serie_txt}"
            proximo_num = sequencia[-1] + razao_pa
    if proximo_num is None and all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia[1] / sequencia[0]
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            resultado_padrao = f"Progressão Geométrica (PG) | Razão: *({round(razao_pg, 4)}){serie_txt}"
            proximo_num = int(sequencia[-1] * razao_pg)
    t_fim = time.perf_counter()
    delta_t = (t_fim - t_inicio) * 1000
    return f"{resultado_padrao}\n\n{estatisticas}", proximo_num, delta_t

# ===================================================================
# 3. INTERFACE SIDEBAR (SISTEMA DE AUTENTICAÇÃO)
# ===================================================================
st.sidebar.title("🔒 Área de Acesso")
if st.session_state["usuario_logado"] is None:
    acesso1, acesso2 = st.sidebar.tabs(["Acessar", "Criar Conta"])
    with acesso1:
        c_user = st.text_input("Usuário:", key="l_user")
        c_pass = st.text_input("Senha:", type="password", key="l_pass")
        if st.button("Entrar", key="b_log"):
            if c_user in st.session_state["tabela_usuarios"] and st.session_state["tabela_usuarios"][c_user] == c_pass:
                st.session_state["usuario_logado"] = c_user
                st.rerun()
            else: st.error("Incorreto.")
    with acesso2:
        n_user = st.text_input("Novo Usuário:", key="c_user").strip().lower()
        n_pass = st.text_input("Nova Senha:", type="password", key="c_pass")
        if st.button("Registrar", key="b_cad"):
            if n_user and n_pass and n_user not in st.session_state["tabela_usuarios"]:
                st.session_state["tabela_usuarios"][n_user] = n_pass
                st.session_state["tabela_ranking"][n_user] = 0
                st.success("Registrado!")
            else: st.error("Inválido ou já existe.")
else:
    st.sidebar.write(f"👤 Logado: `{st.session_state['usuario_logado']}`")
    if st.sidebar.button("Sair"):
        st.session_state["usuario_logado"] = None
        st.session_state["indice_pergunta"] = 0
        st.session_state["quiz_concluido"] = False
        st.rerun()

# ===================================================================
# 4. CORPO PRINCIPAL E NAVEGAÇÃO DE ABAS
# ===================================================================
st.title("🖥️ Central Computacional Prática de ADS & Engenharia")
if st.session_state["usuario_logado"] is None:
    st.warning("⚠️ Efetue o login ou crie sua conta na barra lateral.")
    st.info("💡 Teste rápido: Usuário: `marcio` | Senha: `admin123`")
else:
    arq = st.file_uploader("Importar Planilha (Opcional)", type=["xlsx", "csv"])
    d_plan, t_dado = extrair_dados_do_arquivo(arq) if arq else (None, None)
    ab1, ab2, ar3, ab4, ab5, ab6 = st.tabs([
        "🔢 Sequências & Bases", 
        "🧮 Matrizes A & B 3D", 
        "🧠 Tabela Verdade", 
        "🧪 Quiz & Ranking ADS", 
        "🗄️ Banco de Dados", 
        "📚 Engenharia de Software"
    ])

    # ---------------------------------------------------------------
    # ABA 1: SEQUÊNCIAS E CONVERSÃO DE BASES (PURIFICADA)
    # ---------------------------------------------------------------
    with ab1:
        txt_seq = st.text_input("Sequência:", ", ".join(str(x) for x in d_plan) if t_dado == "sequencia" else "1, 2, 3, 4")
        if st.button("Analisar Sequência"):
            try:
                seq_l = [int(float(x)) if float(x).is_integer() else float(x) for x in txt_seq.split(",") if x.strip()]
                pad, prox, dt_s = identificar_padrao(seq_l)
                st.success(f"### {pad}")
                if prox is not None: st.metric("Próximo Termo", str(prox))
                st.info(f"⚡ **Desempenho Algorítmico:** Processado em **{round(dt_s, 4)} ms** | Complexidade: $O(n)$")
                fig, ax = plt.subplots(figsize=(5, 1.8))
                ax.plot(range(1, len(seq_l) + 1), seq_l, marker='o', color='#2980b9')
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e: st.error(f"Erro: {str(e)}")
        
        st.markdown("---  \n**🧮 Conversor de Sistemas de Numeração (Arquitetura de Computadores)**")
        dec = st.number_input("Decimal:", min_value=0, value=42)
        # CORREÇÃO CIRÚRGICA: Removido método invisível/fictício .white() que crashava a aplicação
        st.write(f"**Binário:** `{bin(dec)[2:]}` | **Octal:** `{oct(dec)[2:]}` | **Hexadecimal:** `{hex(dec)[2:].upper()}`")

    # ---------------------------------------------------------------
    # ABA 2: OPERAÇÕES MATRICIAIS E SUPERFÍCIE 3D
    # ---------------------------------------------------------------
    with ab2:
        st.subheader("Operações Avançadas entre Duas Matrizes")
        v_matA = st.text_area("Estrutura da Matriz A:", ";\n".join(", ".join(str(x) for x in l) for l in d_plan) if t_dado == "matriz" else "1,2;\n3,4", height=70)
        v_matB = st.text_area("Estrutura da Matriz B:", "5,6;\n7,8", height=70)
        k = st.number_input("Multiplicador Escalar K (Matriz A):", value=1.0)
        if st.button("Calcular Operações Matriciais"):
            try:
                linhasA = [l.strip() for l in v_matA.split(";") if l.strip()]
                matrizA_list = [[float(x) for x in linha.split(",") if x.strip()] for linha in linhasA]
                linhasB = [l.strip() for l in v_matB.split(";") if l.strip()]
                matrizB_list = [[float(x) for x in linha.split(",") if x.strip()] for linha in linhasB]
                
                rel, trans, fig_m, dt_m = processar_matriz_pura(matrizA_list, k)
                st.markdown(rel)
                st.info(f"⚡ **Desempenho Algorítmico:** Operação matricial concluída em **{round(dt_m, 4)} ms** | Complexidade: $O(n^3)$")
                if fig_m: 
                    st.pyplot(fig_m)
                    plt.close(fig_m)
                
                matA, matB = np.array(matrizA_list, dtype=float), np.array(matrizB_list, dtype=float)
                if matA.shape == matB.shape:
                    st.markdown("---")
                    st.markdown("**Soma Aditiva (A + B):**")
                    st.code(str(matA + matB))
                    st.markdown("**Subtração Linear (A - B):**")
                    st.code(str(matA - matB))
                    st.markdown("**Multiplicação de Engenharia (A × B):**")
                    st.code(str(np.dot(matA, matB)))
                else: st.warning("Dimensões incompatíveis para Soma/Subtração direta.")
            except Exception as ex: st.error(f"Erro no processamento da matriz: {str(ex)}")

    # ---------------------------------------------------------------
    # ABA 3: TABELA VERDADE PROPOSICIONAL
    # ---------------------------------------------------------------
    with ar3:
        st.header("Análise Analítica de Proposições")
        log_in = st.text_input("Expressão:", "(A AND B) -> NOT C")
        if st.button("Gerar Tabela Verdade"):
            try:
                vars_l = sorted(list(set([c for c in log_in if c.isalpha() and c.isupper()])))
                txt_t = " | ".join(vars_l) + f" | {log_in} \n" + "-"*30 + "\n"
                resultados = []
                for comb in list(itertools.product([True, False], repeat=len(vars_l))):
                    ctx = dict(zip(vars_l, comb))
                    expr = log_in.upper().replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    if "->" in expr:
                        p = expr.split("->")
                        expr = f"not ({p[0].strip()}) or ({p[1].strip()})"
                    res = eval(expr, {}, ctx)
                    resultados.append(res)
                    txt_t += " | ".join("V" if ctx[v] else "F" for v in vars_l) + f" | {'V' if res else 'F'}\n"
                st.code(txt_t)
                st.write("**Classificação:** TAUTOLOGIA" if all(resultados) else "**Classificação:** CONTRADIÇÃO" if not any(resultados) else "**Classificação:** CONTINGÊNCIA")
                st.download_button("📥 Baixar Tabela (.txt)", txt_t, "tabela.txt")
            except Exception as e: st.error(f"Erro na sintaxe lógica: {str(e)}")

    # ---------------------------------------------------------------
    # ABA 4: QUIZ ROTATIVO E DINÂMICO (CORRIGIDO)
    # ---------------------------------------------------------------
    with ab4:
        st.header("🧪 Quiz Simulador ADS & Painel de Liderança")
        
        user_atual = st.session_state["usuario_logado"]
        idx = st.session_state["indice_pergunta"]
        
        # Verifica se ainda existem perguntas disponíveis no banco
        if not st.session_state["quiz_concluido"] and idx < len(BANCO_QUESTOES):
            questao_atual = BANCO_QUESTOES[idx]
            
            st.markdown(f"### **Questão {idx + 1}:**")
            # Utilizar uma chave única vinculada ao índice força o Streamlit a resetar o radiobutton na mudança de questão
            alternativa_selecionada = st.radio(
                questao_atual["pergunta"], 
                questao_atual["opcoes"], 
                key=f"quiz_radio_{idx}"
            )
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("Validar Resposta"):
                    letra_escolhida = alternativa_selecionada.split(")")[0].strip()
                    if letra_escolhida == questao_atual["correta"]:
                        st.session_state["tabela_ranking"][user_atual] = st.session_state["tabela_ranking"].get(user_atual, 0) + 1
                        st.success(f"🎯 Correto, {user_atual.capitalize()}! +1 Ponto computado.")
                        
                        # Alimenta o histórico do banco de dados na Aba 5
                        st.session_state["tabela_historico"].append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Usuário": user_atual,
                            "Questão": idx + 1,
                            "Resultado": "Acertou"
                        })
                    else:
                        st.error(f"❌ Incorreto! A resposta correta era a alternativa {questao_atual['correta']}.")
                        st.session_state["tabela_historico"].append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Usuário": user_atual,
                            "Questão": idx + 1,
                            "Resultado": "Errou"
                        })
            with col_q2:
                if st.button("Próxima Questão ➡️"):
                    if st.session_state["indice_pergunta"] + 1 < len(BANCO_QUESTOES):
                        st.session_state["indice_pergunta"] += 1
                    else:
                        st.session_state["quiz_concluido"] = True
                    st.rerun()
        else:
            st.balloons()
            st.success("🎉 Você concluiu todas as questões disponíveis no banco analítico!")
            if st.button("Reiniciar Quiz 🔄"):
                st.session_state["indice_pergunta"] = 0
                st.session_state["quiz_concluido"] = False
                st.rerun()
                
        st.markdown("---")
        st.subheader("🏆 Quadro de Líderes do Sistema (`tb_ranking_quiz`)")
        df_ranking = pd.DataFrame(list(st.session_state["tabela_ranking"].items()), columns=["Usuário", "Pontos Computados"])
        df_ranking = df_ranking.sort_values(by="Pontos Computados", ascending=False).reset_index(drop=True)
        st.dataframe(df_ranking, use_container_width=True)

    # ---------------------------------------------------------------
    # ABA 5: BANCO DE DADOS (LOG DE EVENTOS DO QUIZ)
    # ---------------------------------------------------------------
    with ab5:
        st.header("🗄️ Visualização das Tabelas do Banco de Dados")
        if st.session_state["tabela_historico"]: 
            st.markdown("### Histórico de Tentativas no Quiz (`tb_log_eventos`)")
            st.dataframe(pd.DataFrame(st.session_state["tabela_historico"]), use_container_width=True)
        else: 
            st.info("Banco de dados histórico vazio. Responda ao quiz para gerar logs.")

    # ---------------------------------------------------------------
    # ABA 6: DOCUMENTAÇÃO DE ENGENHARIA
    # ---------------------------------------------------------------
    with ab6:
        st.header("📚 Engenharia de Software e Especificação Técnica")
        col_eng1, col_col2 = st.columns(2)
        with col_eng1:
            st.subheader("📋 Requisitos Funcionais (RF)")
            st.info("* **RF001 - Autocadastro:** Módulo de credenciais em hash dinâmico.\n* **RF002 - Controle de Sessão:** Bloqueio de visualizações para sessões nulas.\n* **RF003 - Análise de Performance:** Cronometragem algorítmica real via hardware (ms).")
        with col_col2:
            st.subheader("📝 Cenário de Caso de Uso: Efetuar Cadastro")
            st.success("* **Atores:** Usuário Acadêmico ou Professor.\n* **Fluxo:** Navega para 'Criar Conta' -> Insere ID exclusivo e Chave -> Mapeia na Tabela Hash do Servidor -> Libera Token.")
