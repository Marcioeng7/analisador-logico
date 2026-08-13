"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro e Desenvolvedor ADS)
Versão: V24.0 (Super Plataforma Integrada: Estatísticas, Quiz ADS e Matrizes A e B)
Ano: 2026
"""

import streamlit as st
import math
from fractions import Fraction
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

# Configuração global da página Web do Streamlit
st.set_page_config(page_title="Central Analítica & ADS", page_icon="🖥️", layout="wide")

# --- ARQUITETURA DE BANCO DE DADOS SIMULADA ---
if "tabela_usuarios" not in st.session_state:
    st.session_state["tabela_usuarios"] = {"marcio": "admin123", "professor": "ads2026"}
if "tabela_historico" not in st.session_state:
    st.session_state["tabela_historico"] = []
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None
if "quiz_pontuacao" not in st.session_state:
    st.session_state["quiz_pontuacao"] = 0

# --- FUNÇÃO AUXILIAR: LEITOR DE PLANILHAS ---
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

# --- SISTEMA 1: PROCESSAMENTO DE MATRIZ PURA (MATRIZ A) ---
def processar_matriz_pura(matriz, escalar_mult=1.0):
    try:
        matriz = [[x * escalar_mult for x in linha] for linha in matriz]
        num_linhas, num_colunas = len(matriz), len(matriz) if len(matriz) > 0 else 0
        if not all(len(l) == num_colunas for l in matriz): return "Erro: Linhas desalinhadas.", None, None
        transposta = [[matriz[j][i] for j in range(num_linhas)] for i in range(num_colunas)]
        todos_valores = [x for linha in matriz for x in linha]
        det_txt = "N/A"
        if num_linhas == num_colunas:
            if num_linhas == 2: det_txt = f"{round((matriz*matriz)-(matriz*matriz), 4)}"
            elif num_linhas == 3:
                d1 = (matriz*matriz*matriz) + (matriz*matriz*matriz) + (matriz*matriz*matriz)
                d2 = (matriz*matriz*matriz) + (matriz*matriz*matriz) + (matriz*matriz*matriz)
                det_txt = f"{round(d1 - d2, 4)}"
        relatorio = f"**Dimensão:** {num_linhas}x{num_colunas} | **Determinante:** {det_txt} | **Média Global:** {round(sum(todos_valores)/len(todos_valores), 4)}"
        fig = plt.figure(figsize=(4, 2.5))
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(np.arange(0, num_colunas, 1), np.arange(0, num_linhas, 1))
        ax.plot_surface(X, Y, np.array(matriz), cmap="coolwarm", edgecolor='none', alpha=0.9)
        ax.set_title("Superfície 3D - Matriz A", fontsize=8, fontweight="bold")
        return relatorio, transposta, fig
    except Exception as e:
        return f"Erro analítico: {str(e)}", None, None

# --- SISTEMA 2: TESTE DE CONVERGÊNCIA DE SÉRIES ---
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

# --- SISTEMA 3: LEITOR DE PADRÕES E PAINEL ESTATÍSTICO (OPÇÃO A) ---
def identificar_padrao(sequencia):
    n = len(sequencia)
    if n < 3: return "Insira pelo menos 3 números.", None
    serie_txt = checar_convergencia_serie(sequencia)
    p_termo = float(sequencia)
    
    # Geração Estatística Descritiva Avançada
    arr = np.array(sequencia)
    estatisticas = (
        f"---  \n📊 **Painel Estatístico Descritivo (Módulo de Dados):**  \n"
        f"• Média Aritmética: {round(np.mean(arr), 4)} | • Mediana Central: {round(np.median(arr), 4)}  \n"
        f"• Desvio Padrão: {round(np.std(arr), 4)} | • Variância da Amostra: {round(np.var(arr), 4)}  \n"
        f"• Amplitude Máxima Total (Máx - Mín): {round(np.max(arr) - np.min(arr), 4)}"
    )

    if all(isinstance(x, int) and x > 0 for x in sequencia):
        f_validos = [i for i in range(1, 14) if math.factorial(i) == int(p_termo)]
        if f_validos and all(sequencia[i] == math.factorial(f_validos + i) for i in range(n)):
            return f"Sequência Fatorial (n!){serie_txt}\n\n{estatisticas}", math.factorial(f_validos + n)
    if all(x >= 0 for x in sequencia) and (p_termo**0.5).is_integer():
        r_start = int(p_termo**0.5)
        if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
            return f"Sequência de Quadrados Perfeitos (n²){serie_txt}\n\n{estatisticas}", (r_start + n)**2
    if all(sequencia[i] == (round(p_termo**(1/3)) + i)**3 for i in range(n)):
        return f"Sequência de Cubos Perfeitos (n³){serie_txt}\n\n{estatisticas}", (round(p_termo**(1/3)) + n)**3
    if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
        return f"Sequência de Fibonacci\n\n{estatisticas}", sequencia[-1] + sequencia[-2]
    if n >= 2:
        razao_pa = sequencia - sequencia
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            return f"Progressão Aritmética (PA) | Razão: {razao_pa}{serie_txt}\n\n{estatisticas}", sequencia[-1] + razao_pa
    if all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia / sequencia
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            return f"Progressão Geométrica (PG) | Razão: *({round(razao_pg, 4)}){serie_txt}\n\n{estatisticas}", int(sequencia[-1] * razao_pg)
    return (f"Padrão estrutural não reconhecido.\n\n{estatisticas}", None)

# --- INTERFACE VISUAL DA PLATAFORMA ---
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
                st.success("Registrado!")
            else: st.error("Inválido ou já existe.")
else:
    st.sidebar.write(f"👤 Logado: `{st.session_state['usuario_logado']}`")
    if st.sidebar.button("Sair"):
        st.session_state["usuario_logado"] = None
        st.rerun()

st.title("🖥️ Central Computacional Prática de ADS & Engenharia")
if st.session_state["usuario_logado"] is None:
    st.warning("⚠️ Efetue o login ou crie sua conta na barra lateral.")
    st.info("💡 Teste rápido: Usuário: `marcio` | Senha: `admin123`")
else:
    arq = st.file_uploader("Importar Planilha (Opcional)", type=["xlsx", "csv"])
    d_plan, t_dado = extrair_dados_do_arquivo(arq) if arq else (None, None)
    ab1, ab2, ar3, ab4, ab5, ab6 = st.tabs(["🔢 Sequências & Bases", "🧮 Matrizes A & B 3D", "🧠 Tabela Verdade", "🧪 Quiz Simulador ADS", "🗄️ Banco de Dados", "📚 Disciplinas TCC"])

    with ab1:
        txt_seq = st.text_input("Sequência:", ", ".join(str(x) for x in d_plan) if t_dado == "sequencia" else "1, 2, 3, 4")
        if st.button("Analisar Sequência"):
            seq_l = [int(float(x)) if float(x).is_integer() else float(x) for x in txt_seq.split(",") if x.strip()]
            pad, prox = identificar_padrao(seq_l)
            st.success(f"### {pad}")
            if prox is not None: st.metric("Próximo Termo", str(prox))
            fig, ax = plt.subplots(figsize=(5, 1.8))
            ax.plot(range(1, len(seq_l) + 1), seq_l, marker='o', color='#2980b9')
            st.pyplot(fig)
        st.markdown("---  \n**🧮 Conversor de Sistemas de Numeração (Arquitetura de Computadores)**")
        dec = st.number_input("Decimal:", min_value=0, value=42)
        st.write(f"**Binário:** `{bin(dec)[2:]}` | **Octal:** `{oct(dec)[2:]}` | **Hexadecimal:** `{hex(dec)[2:].upper()}`")

    with ab2:
        st.subheader("Operações Avançadas entre Duas Matrizes (Opção C)")
        v_matA = st.text_area("Estrutura da Matriz A:", ";\n".join(", ".join(str(x) for x in l) for l in d_plan) if t_dado == "matriz" else "1,2;\n3,4", height=70)
        v_matB = st.text_area("Estrutura da Matriz B:", "5,6;\n7,8", height=70)
        k = st.number_input("Multiplicador Escalar K (Apenas para Matriz A):", value=1.0)
        
        if st.button("Calcular Operações Matriciais"):
            try:
                matA = np.array([[float(x) for x in l.split(",") if x.strip()] for l in v_matA.split(";") if l.strip()])
                matB = np.array([[float(x) for x in l.split(",") if x.strip()] for l in v_matB.split(";") if l.strip()])
                rel, trans, fig_m = processar_matriz_pura(matA.tolist(), k)
                
                st.markdown(rel)
                if fig_m: st.pyplot(fig_m)
                
                if matA.shape == matB.shape:
                    st.markdown("---")
                    st.markdown("**Soma Aditiva (A + B):**")
                    st.code(str(matA + matB))
                    st.markdown("**Subtração Linear (A - B):**")
                    st.code(str(matA - matB))
                    if matA.shape[1] == matB.shape[0]:
                        st.markdown("**Multiplicação de Engenharia (A × B):**")
                        st.code(str(np.dot(matA, matB)))
                else: st.warning("Dimensões incompatíveis para Soma/Subtração direta.")
            except Exception as ex: st.error(f"Erro na matriz: {str(ex)}")

    with ar3:
        log_in = st.text_input("Expressão:", "(A AND B) -> NOT C")
        if st.button("Gerar Tabela Verdade"):
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

    with ab4:
        st.header("🧪 Quiz Simulador ADS - Treinamento para Provas (Opção B)")
        st.markdown("Responda às questões reais de concursos e avalie seus conhecimentos antes das provas escolares!")
        q1 = st.radio("**Questão 1:** Na arquitetura de computadores, o número decimal **10** equivale a qual representação binária de máquina?", ["A) 1001", "B) 1010", "C) 1100", "D) 1111"])
        if st.button("Validar Questão 1"):
            if q1.startswith("B"): st.success("🎯 Resposta Correta! 10 em decimal é igual a 1010 em binário (8 + 2). Nota 10!")
            else: st.error("❌ Resposta Incorreta. Tente novamente ou use o conversor da Aba 1 para checar a conversão!")

    with ab5:
        st.header("🗄️ Tabelas Relacionais em Memória")
        if st.session_state["tabela_historico"]: st.dataframe(pd.DataFrame(st.session_state["tabela_historico"]))
        else: st.info("Banco vazio.")

    with ab6:
        st.header("📚 Vínculo do Sistema com as Disciplinas de ADS")
        st.markdown("* **Lógica Matemática e Análise de Dados:** Avaliação binária combinatória, classificação formal e rotinas de métricas estatísticas descritivas calculadas em lote via NumPy.")
        st.markdown("* **Arquitetura de Computadores:** Conversão ativa de barramento decimal nativo para registradores de base 2, 8 e 16.")
        st.markdown("* **Álgebra Linear:** Multiplicação matricial complexa de matrizes A e B por produto escalar e produto interno.")
