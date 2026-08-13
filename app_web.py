"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro e Desenvolvedor ADS)
Versão: V27.0 (Divisão Avançada em 5 Blocos - PDF + Espectral)
Ano: 2026
"""

import streamlit as st
import math
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

# Componentes estruturais do motor de PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="Central Analítica & ADS", page_icon="🖥️", layout="wide")

# ===================================================================
# 1. MOTOR DE PERSISTÊNCIA REAL DE DADOS (ARQUIVOS CSV)
# ===================================================================
ARQUIVO_USERS = "usuarios.csv"
ARQUIVO_RANKING = "ranking.csv"
ARQUIVO_HISTORICO = "historico.csv"

def carregar_dados_locais():
    if os.path.exists(ARQUIVO_USERS):
        df = pd.read_csv(ARQUIVO_USERS)
        st.session_state["tabela_usuarios"] = dict(zip(df["usuario"], df["senha"]))
    else:
        st.session_state["tabela_usuarios"] = {"marcio": "admin123", "professor": "ads2026"}
        pd.DataFrame(list(st.session_state["tabela_usuarios"].items()), columns=["usuario", "senha"]).to_csv(ARQUIVO_USERS, index=False)

    if os.path.exists(ARQUIVO_RANKING):
        df = pd.read_csv(ARQUIVO_RANKING)
        st.session_state["tabela_ranking"] = dict(zip(df["usuario"], df["pontos"]))
    else:
        st.session_state["tabela_ranking"] = {"marcio": 1, "professor": 0}
        pd.DataFrame(list(st.session_state["tabela_ranking"].items()), columns=["usuario", "pontos"]).to_csv(ARQUIVO_RANKING, index=False)

    if os.path.exists(ARQUIVO_HISTORICO):
        st.session_state["tabela_historico"] = pd.read_csv(ARQUIVO_HISTORICO).to_dict(orient="records")
    else:
        st.session_state["tabela_historico"] = []
        pd.DataFrame(columns=["Timestamp", "Usuário", "Questão", "Resultado"]).to_csv(ARQUIVO_HISTORICO, index=False)

def salvar_tabela_usuarios():
    df = pd.DataFrame(list(st.session_state["tabela_usuarios"].items()), columns=["usuario", "senha"])
    df.to_csv(ARQUIVO_USERS, index=False)

def salvar_tabela_ranking():
    df = pd.DataFrame(list(st.session_state["tabela_ranking"].items()), columns=["usuario", "pontos"])
    df.to_csv(ARQUIVO_RANKING, index=False)

def salvar_tabela_historico():
    df = pd.DataFrame(st.session_state["tabela_historico"])
    df.to_csv(ARQUIVO_HISTORICO, index=False)

carregar_dados_locais()

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None
if "indice_pergunta" not in st.session_state:
    st.session_state["indice_pergunta"] = 0
if "quiz_concluido" not in st.session_state:
    st.session_state["quiz_concluido"] = False

# ===================================================================
# BANCO DE DADOS ESTÁTICO DE QUESTÕES DO QUIZ
# ===================================================================
BANCO_QUESTOES = [
    {"pergunta": "Na arquitetura de computadores, o número decimal 10 equivale a qual representação binária?", "opcoes": ["A) 1001", "B) 1010", "C) 1100", "D) 1111"], "correta": "B"},
    {"pergunta": "Qual das seguintes estruturas de dados utiliza o princípio LIFO (Last In, First Out)?", "opcoes": ["A) Fila (Queue)", "B) Lista Encadeada", "C) Pilha (Stack)", "D) Árvore Binária"], "correta": "C"},
    {"pergunta": "Na Engenharia de Software, qual diagrama da UML é focado no aspecto comportamental e na interação de atores com o sistema?", "opcoes": ["A) Diagrama de Classes", "B) Diagrama de Casos de Uso", "C) Diagrama de Implantação", "D) Diagrama de Objetos"], "correta": "B"},
    {"pergunta": "Qual é a complexidade de tempo no pior caso para o algoritmo de ordenação Bubble Sort?", "opcoes": ["A) O(1)", "B) O(n log n)", "C) O(n)", "D) O(n²)"], "correta": "D"}
]

# ===================================================================
# 2. MOTOR COMPACTO DE EXPORTAÇÃO PDF (REPORTLAB)
# ===================================================================
def gerar_pdf_relatorio(titulo_doc, texto_conteudo):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle('TituloEng', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#2c3e50'), spaceAfter=15)
    style_corpo = ParagraphStyle('CorpoEng', parent=styles['Normal'], fontSize=11, leading=15, spaceAfter=8)
    
    story = []
    story.append(Paragraph(f"<b>{titulo_doc}</b>", style_titulo))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", style_corpo))
    story.append(Paragraph(f"Operador Responsável: {st.session_state['usuario_logado']}", style_corpo))
    story.append(Spacer(1, 15))
    
    for linha in texto_conteudo.split('\n'):
        if linha.strip():
            story.append(Paragraph(linha.replace('**', '<b>').replace('**', '</b>'), style_corpo))
            
    doc.build(story)
    buffer.seek(0)
    return buffer

# ===================================================================
# 3. MÓDULO ESTATÍSTICO E ALGORÍTMICO DE SEQUÊNCIAS
# ===================================================================
def extrair_dados_do_arquivo(arquivo_carregado):
    try:
        nome_arquivo = arquivo_carregado.name
        df = pd.read_csv(arquivo_carregado, header=None) if nome_arquivo.endswith('.csv') else pd.read_excel(arquivo_carregado, header=None)
        dados = df.values.tolist()
        if len(dados) == 1:
            return [float(x) for x in dados if pd.notna(x)], "sequencia"
        return [[float(x) for x in linha if pd.notna(x)] for linha in dados], "matriz"
    except Exception:
        st.error("Erro ao ler o arquivo.")
        return None, None

def calcular_regressao_linear(sequencia):
    try:
        x = np.arange(1, len(sequencia) + 1, dtype=float)
        y = np.array(sequencia, dtype=float)
        a, b = np.polyfit(x, y, 1)
        y_pred = a * x + b
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_quadrado = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
        return a, b, r_quadrado, x, y_pred
    except Exception:
        return 0.0, 0.0, 0.0, None, None

def checar_convergencia_serie(sequencia):
    n = len(sequencia)
    if n < 3: return ""
    if all(abs(sequencia[i] - (1 / (i + 1))) < 0.05 for i in range(n)): return "\n\n**Série:** Harmônica Divergente."
    if all(x != 0 for x in sequencia):
        try:
            r_prop = sequencia / sequencia
            if abs(r_prop) < 1 and all(abs((sequencia[i] / sequencia[i-1]) - r_prop) < 0.01 for i in range(1, n)):
                return f"\n\n**Série:** Geométrica Convergente. Limite: **{round(sequencia/(1-r_prop), 4)}**."
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
# 4. INTERFACE SIDEBAR (SISTEMA DE AUTENTICAÇÃO PERSISTENTE)
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
                
                salvar_tabela_usuarios()
                salvar_tabela_ranking()
                
                st.success("Registrado com sucesso no banco de dados!")
            else: st.error("Inválido ou já existe.")
else:
    st.sidebar.write(f"👤 Logado: `{st.session_state['usuario_logado']}`")
    if st.sidebar.button("Sair"):
        st.session_state["usuario_logado"] = None
        st.session_state["indice_pergunta"] = 0
        st.session_state["quiz_concluido"] = False
        st.rerun()

# ===================================================================
# 5. FUNÇÃO MATRICIAL COMPLETA (INVERSA + TRANSPOSTA + AUTOVALORES)
# ===================================================================
def processar_matriz_pura(matriz, escalar_mult=1.0):
    t_inicio = time.perf_counter()
    try:
        np_matriz = np.array(matriz, dtype=float) * escalar_mult
        num_linhas, num_colunas = np_matriz.shape
        transposta = np_matriz.T.tolist()
        
        det_txt = "N/A (Não Quadrada)"
        inversa_np = None
        autovalores = None
        autovetores = None
        
        if num_linhas == num_colunas:
            det_val = float(np.linalg.det(np_matriz))
            det_txt = f"{round(det_val, 4)}"
            if abs(det_val) > 1e-9:
                inversa_np = np.linalg.inv(np_matriz)
            
            # Cálculo de Autovalores e Autovetores via NumPy
            autovalores, autovetores = np.linalg.eig(np_matriz)
        
        t_fim = time.perf_counter()
        delta_t = (t_fim - t_inicio) * 1000
        relatorio = f"**Dimensão:** {num_linhas}x{num_colunas} | **Determinante:** {det_txt} | **Média Global:** {round(float(np.mean(np_matriz)), 4)}"
        
        # Plotagem adaptativa da malha topográfica
        fig = plt.figure(figsize=(4, 2.5))
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(np.arange(0, num_colunas, 1), np.arange(0, num_linhas, 1))
        ax.plot_surface(X, Y, np_matriz, cmap="coolwarm", edgecolor='none', alpha=0.9)
        ax.set_title("Superfície 3D Adaptativa", fontsize=8, fontweight="bold")
        
        return relatorio, transposta, inversa_np, autovalores, autovetores, fig, delta_t
    except Exception as e:
        return f"Erro analítico matricial: {str(e)}", None, None, None, None, None, 0.0

# ===================================================================
# 6. CORPO PRINCIPAL E INTERFACE GRÁFICA DE ABAS
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
    # ABA 1: SEQUÊNCIAS, BASES E NOVO MOTOR DE REGRESSÃO LINEAR
    # ---------------------------------------------------------------
    with ab1:
        txt_seq = st.text_input("Sequência:", ", ".join(str(x) for x in d_plan) if t_dado == "sequencia" else "1, 2, 3, 4")
        if st.button("Analisar Sequência e Modelar Tendência"):
            try:
                seq_l = [int(float(x)) if float(x).is_integer() else float(x) for x in txt_seq.split(",") if x.strip()]
                
                pad, prox, dt_s = identificar_padrao(seq_l)
                st.success(f"### {pad}")
                if prox is not None: st.metric("Próximo Termo Identificado", str(prox))
                st.info(f"⚡ **Desempenho Algorítmico:** Processado em **{round(dt_s, 4)} ms**")
                
                a, b, r2, x_val, y_pred = calcular_regressao_linear(seq_l)
                txt_regressao = (
                    f"📊 **Análise de Regressão Linear Simples:**\n"
                    f"• Equação de Tendência Ajustada: y = {round(a,4)}x + ({round(b,4)})\n"
                    f"• Coeficiente de Determinação (R²): {round(r2, 4)}"
                )
                st.markdown(txt_regressao)
                
                fig, ax = plt.subplots(figsize=(5, 1.8))
                ax.scatter(range(1, len(seq_l) + 1), seq_l, color='#e74c3c', label='Dados Originais', zorder=5)
                ax.plot(x_val, y_pred, color='#2980b9', linestyle='--', label='Reta de Regressão')
                ax.legend(fontsize=6)
                st.pyplot(fig)
                plt.close(fig)
                
                # Geração de PDF Técnico da Sequência
                conteudo_pdf_seq = f"{pad}\n\n{txt_regressao}"
                pdf_data = gerar_pdf_relatorio("Relatório Técnico - Análise de Sequências e Regressão", conteudo_pdf_seq)
                st.download_button("📥 Exportar Relatório em PDF", pdf_data, "relatorio_sequencia.pdf", "application/pdf")
                
            except Exception as e: st.error(f"Erro: {str(e)}")
        
        st.markdown("---  \n**🧮 Conversor de Sistemas de Numeração (Arquitetura de Computadores)**")
        dec = st.number_input("Decimal:", min_value=0, value=42)
        st.write(f"**Binário:** `{bin(dec)[2:]}` | **Octal:** `{oct(dec)[2:]}` | **Hexadecimal:** `{hex(dec)[2:].upper()}`")

    # ---------------------------------------------------------------
    # ABA 2: OPERAÇÕES MATRICIAIS AVANÇADAS E TOPOGRAFIA ADAPTATIVA
    # ---------------------------------------------------------------
    with ab2:
        st.subheader("Operações Avançadas entre Duas Matrizes")
        v_matA = st.text_area("Estrutura da Matriz A:", ";\n".join(", ".join(str(x) for x in l) for l in d_plan) if t_dado == "matriz" else "1,2;3,4", height=70)
        v_matB = st.text_area("Estrutura da Matriz B:", "5,6;7,8", height=70)
        k = st.number_input("Multiplicador Escalar K (Matriz A):", value=1.0)
        if st.button("Calcular Operações Matriciais"):
            try:
                linhasA = [l.strip() for l in v_matA.split(";") if l.strip()]
                matrizA_list = [[float(x) for x in linha.split(",") if x.strip()] for linha in linhasA]
                linhasB = [l.strip() for l in v_matB.split(";") if l.strip()]
                matrizB_list = [[float(x) for x in linha.split(",") if x.strip()] for linha in linhasB]
                
                rel, trans, inv_np, autovalores, autovetores, fig_m, dt_m = processar_matriz_pura(matrizA_list, k)
                st.markdown(rel)
                st.info(f"⚡ **Desempenho Algorítmico:** Concluído em **{round(dt_m, 4)} ms**")
                
                if fig_m: 
                    st.pyplot(fig_m)
                    plt.close(fig_m)
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown("**Matriz Transposta de A ($A^T$):**")
                    st.code(str(np.array(trans)))
                with col_m2:
                    st.markdown("**Matriz Inversa de A ($A^{-1}$):**")
                    if inv_np is not None:
                        st.code(str(np.round(inv_np, 4)))
                    else:
                        st.warning("Inversa Indisponível (Determinante Nulo ou Não Quadrada).")
                
                # Exibição Espectral Avançada
                st.markdown("---")
                st.subheader("🧬 Decomposição Espectral (Autovalores e Autovetores)")
                if autovalores is not None:
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown("**Autovalores ($\lambda$):**")
                        st.code(str(np.round(autovalores, 4)))
                    with col_e2:
                        st.markdown("**Autovetores (V):**")
                        st.code(str(np.round(autovetores, 4)))
                else:
                    st.warning("Decomposição indisponível (A matriz precisa ser quadrada).")
                
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
                
                # Geração de PDF Técnico da Álgebra Matricial
                conteudo_pdf_mat = f"{rel}\n\nAutovalores:\n{str(np.round(autovalores, 4)) if autovalores is not None else 'N/A'}\n\nAutovetores:\n{str(np.round(autovetores, 4)) if autovetores is not None else 'N/A'}"
                pdf_data_mat = gerar_pdf_relatorio("Relatório Técnico - Análise Linear e Espectral", conteudo_pdf_mat)
                st.download_button("📥 Exportar Laudo Técnico em PDF", pdf_data_mat, "laudo_matricial.pdf", "application/pdf")
                
            except Exception as ex: st.error(f"Erro no processamento da matriz: {str(ex)}")

    # ---------------------------------------------------------------
    # ABA 3: TABELA VERDADE PROPOSICIONAL (CONDICIONAL E BICONDICIONAL)
    # ---------------------------------------------------------------
    with ar3:
        st.header("Análise Analítica de Proposições")
        log_in = st.text_input("Expressão:", "(A AND B) <-> NOT C")
        if st.button("Gerar Tabela Verdade"):
            try:
                vars_l = sorted(list(set([c for c in log_in if c.isalpha() and c.isupper()])))
                txt_t = " | ".join(vars_l) + f" | {log_in} \n" + "-"*40 + "\n"
                resultados = []
                
                for comb in list(itertools.product([True, False], repeat=len(vars_l))):
                    ctx = dict(zip(vars_l, comb))
                    expr = log_in.upper().replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    
                    if "<->" in expr:
                        partes_bi = expr.split("<->")
                        expr = f"({partes_bi[0].strip()}) == ({partes_bi[1].strip()})"
                        
                    if "->" in expr:
                        partes_cond = expr.split("->")
                        expr = f"not ({partes_cond[0].strip()}) or ({partes_cond[1].strip()})"
                        
                    res = eval(expr, {}, ctx)
                    resultados.append(res)
                    txt_t += " | ".join("V" if ctx[v] else "F" for v in vars_l) + f" | {'V' if res else 'F'}\n"
                    
                st.code(txt_t)
                classif = "TAUTOLOGIA" if all(resultados) else "CONTRADIÇÃO" if not any(resultados) else "CONTINGÊNCIA"
                st.write(f"**Classificação:** {classif}")
                
                col_down1, col_down2 = st.columns(2)
                with col_down1:
                    st.download_button("📥 Baixar Tabela (.txt)", txt_t, "tabela.txt")
                with col_down2:
                    # Geração de Relatório PDF da Tabela Verdade
                    pdf_data_log = gerar_pdf_relatorio("Laudo Lógico - Mapeamento de Proposições", f"Expressão: {log_in}\nClassificação: {classif}\n\nEstrutura mapeada e validada com sucesso.")
                    st.download_button("📥 Baixar Laudo em PDF", pdf_data_log, "laudo_logico.pdf", "application/pdf")
            except Exception as e: st.error(f"Erro na sintaxe lógica: {str(e)}")

    # ---------------------------------------------------------------
    # ABA 4: QUIZ ROTATIVO COM PERSISTÊNCIA EM DISCO
    # ---------------------------------------------------------------
    with ab4:
        st.header("🧪 Quiz Simulador ADS & Painel de Liderança")
        user_atual = st.session_state["usuario_logado"]
        idx = st.session_state["indice_pergunta"]
        
        if not st.session_state["quiz_concluido"] and idx < len(BANCO_QUESTOES):
            questao_atual = BANCO_QUESTOES[idx]
            st.markdown(f"### **Questão {idx + 1}:**")
            alternativa_selecionada = st.radio(questao_atual["pergunta"], questao_atual["opcoes"], key=f"quiz_radio_{idx}")
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("Validar Resposta"):
                    letra_escolhida = alternativa_selecionada.split(")")[0].strip()
                    if letra_escolhida == questao_atual["correta"]:
                        st.session_state["tabela_ranking"][user_atual] = st.session_state["tabela_ranking"].get(user_atual, 0) + 1
                        st.success(f"🎯 Correto, {user_atual.capitalize()}! +1 Ponto computado.")
                        st.session_state["tabela_historico"].append({"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Usuário": user_atual, "Questão": idx + 1, "Result": "Acertou"})
                    else:
                        st.error(f"❌ Incorreto! A resposta correta era a alternativa {questao_atual['correta']}.")
                        st.session_state["tabela_historico"].append({"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Usuário": user_atual, "Questão": idx + 1, "Result": "Errou"})
                    salvar_tabela_ranking()
                    salvar_tabela_historico()
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
    # ABA 5: BANCO DE DADOS (COM FUNCIONALIDADE DE LIMPEZA INTEGRADA)
    # ---------------------------------------------------------------
    with ab5:
        st.header("🗄️ Visualização das Tabelas do Banco de Dados")
        st.subheader("🛠️ Painel Avançado de Governança")
        if st.button("🚨 Limpar Histórico e Eventos do Sistema"):
            st.session_state["tabela_historico"] = []
            salvar_tabela_historico()
            st.toast("Banco de dados histórico resetado com sucesso!", icon="🗑️")
            st.rerun()
            
        st.markdown("---")
        if st.session_state["tabela_historico"]: 
            st.markdown("### Histórico Geral de Tentativas no Quiz (Carregado de `historico.csv`)")
            st.dataframe(pd.DataFrame(st.session_state["tabela_historico"]), use_container_width=True)
        else: 
            st.info("Banco de dados histórico vazio. Responda ao quiz para gerar logs físicos.")

    # ---------------------------------------------------------------
    # ABA 6: DOCUMENTAÇÃO DE ENGENHARIA
    # ---------------------------------------------------------------
    with ab6:
        st.header("📚 Engenharia de Software e Especificação Técnica")
        col_eng1, col_col2 = st.columns(2)
        with col_eng1:
            st.subheader("📋 Requisitos Funcionais (RF)")
            st.info("* **RF001 - Autocadastro:** Módulo de credenciais persistidas localmente em CSV.\n* **RF002 - Controle de Sessão:** Bloqueio de visualizações para sessões nulas.\n* **RF003 - Análise de Performance:** Cronometragem algorítmica real via hardware (ms).\n* **RF004 - Governança de Dados:** Purga e expurgo de tabelas físicas pelo administrador.\n* **RF005 - Estatística Avançada:** Modelagem matemática preditiva por Regressão Linear com cálculo de $R^2$.\n* **RF006 - Módulo de Relatórios:** Geração nativa e dinâmica de laudos em formato PDF via ReportLab.")
        with col_col2:
            st.subheader("📝 Cenário de Caso de Uso: Efetuar Cadastro")
            st.success("* **Atores:** Usuário Acadêmico ou Professor.\n* **Fluxo:** Navega para 'Criar Conta' -> Insere ID exclusivo e Chave -> Salva na tabela física local -> Libera Token.")

