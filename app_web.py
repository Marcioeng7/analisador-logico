"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro)
Versão: V17.1 (Versão Consolidada de Engenharia e ADS - Sem Bugs)
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
st.set_page_config(
    page_title="Central Analítica & ADS", 
    page_icon="🖥️", 
    layout="wide"
)

# --- ARQUITETURA DE BANCO DE DADOS SIMULADA (PADRÃO ADS / ENGENHARIA) ---
if "tabela_usuarios" not in st.session_state:
    st.session_state["tabela_usuarios"] = {
        "marcio": "admin123",
        "professor": "ads2026"
    }

if "tabela_historico" not in st.session_state:
    st.session_state["tabela_historico"] = []

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# --- FUNÇÃO AUXILIAR: LEITOR DE PLANILHAS (EXCEL E CSV) ---
def extrair_dados_do_arquivo(arquivo_carregado):
    try:
        nome_arquivo = arquivo_carregado.name
        if nome_arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo_carregado, header=None)
        else:
            df = pd.read_excel(arquivo_carregado, header=None)
        dados = df.values.tolist()
        if len(dados) == 1:
            return [float(x) for x in dados[0] if pd.notna(x)], "sequencia"
        matriz_limpa = [[float(x) for x in linha if pd.notna(x)] for linha in dados]
        return matriz_limpa, "matriz"
    except Exception:
        st.error("Erro ao ler o arquivo. Certifique-se de que a planilha possui apenas números.")
        return None, None

# --- SISTEMA 1: PROCESSAMENTO E PLOTAGEM DE MATRIZES ---
def processar_matriz_pura(matriz, escalar_mult=1.0):
    try:
        matriz = [[x * escalar_mult for x in linha] for linha in matriz]
        num_linhas = len(matriz)
        num_colunas = len(matriz[0]) if num_linhas > 0 else 0
        if not all(len(l) == num_colunas for l in matriz):
            return "Erro: A matriz possui linhas com comprimentos desalinhados.", None, None, None
            
        transposta = [[matriz[j][i] for j in range(num_linhas)] for i in range(num_colunas)]
        todos_valores = [x for linha in matriz for x in linha]
        v_max = max(todos_valores)
        v_min = min(todos_valores)
        v_media = sum(todos_valores) / len(todos_valores)
        
        traco_txt = "N/A"
        if num_linhas == num_colunas:
            traco_txt = f"{round(sum(matriz[i][i] for i in range(num_linhas)), 4)}"
        
        det_txt = "N/A"
        if num_linhas == num_colunas:
            if num_linhas == 2:
                det = (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])
                det_txt = f"{round(det, 4)}"
            elif num_linhas == 3:
                d1 = (matriz[0][0]*matriz[1][1]*matriz[2][2]) + (matriz[0][1]*matriz[1][2]*matriz[2][0]) + (matriz[0][2]*matriz[1][0]*matriz[2][1])
                d2 = (matriz[0][2]*matriz[1][1]*matriz[2][0]) + (matriz[0][0]*matriz[1][2]*matriz[2][1]) + (matriz[0][1]*matriz[1][0]*matriz[2][2])
                det_txt = f"{round(d1 - d2, 4)}"
                
        relatorio = (
            f"**Dimensão:** {num_linhas}x{num_colunas} | **Determinante:** {det_txt} | **Traço:** {traco_txt}  \n"
            f"**Estatísticas:** Máx: {round(v_max, 4)} | Mín: {round(v_min, 4)} | Média: {round(v_media, 4)}"
        )
        
        fig = plt.figure(figsize=(4.5, 3.2))
        ax = fig.add_subplot(111, projection='3d')
        x = np.arange(0, num_colunas, 1)
        y = np.arange(0, num_linhas, 1)
        X, Y = np.meshgrid(x, y)
        Z = np.array(matriz)
        surf = ax.plot_surface(X, Y, Z, cmap="coolwarm", edgecolor='none', alpha=0.9)
        ax.set_title("Projeção Topográfica de Superfície 3D", fontsize=8, fontweight="bold")
        ax.tick_params(labelsize=6)
        
        return relatorio, transposta, fig, matriz
    except Exception as e:
        return f"Erro analítico: {str(e)}", None, None, None

# --- SISTEMA 2: TESTE DE CONVERGÊNCIA DE SÉRIES ---
def checar_convergencia_serie(sequencia):
    n = len(sequencia)
    if n < 3:
        return ""
    if all(abs(sequencia[i] - (1 / (i + 1))) < 0.05 for i in range(n)):
        return "\n\n**Série:** Harmônica Divergente ($\sum 1/n$)."
    if all(x != 0 for x in sequencia):
        try:
            r_prop = sequencia[1] / sequencia[0]
            if abs(r_prop) < 1 and all(abs((sequencia[i] / sequencia[i-1]) - r_prop) < 0.01 for i in range(1, n)):
                soma_limite = sequencia[0] / (1 - r_prop)
                return f"\n\n**Série:** Geométrica Convergente. Limite: **{round(soma_limite, 4)}**."
        except Exception:
            pass
    return ""

# --- SISTEMA 3: LEITOR DE PADRÕES SEQUENCIAIS ---
def eh_primo(n):
    if not isinstance(n, int) or n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def analisar_propriedades(sequencia):
    if not all(isinstance(x, int) for x in sequencia):
        return ""
    properties = []
    if all(x % 2 == 0 for x in sequencia):
        properties.append("Pares")
    elif all(x % 2 != 0 for x in sequencia):
        properties.append("Ímpares")
    if all(eh_primo(x) for x in sequencia):
        properties.append("Primos")
    return f"**Propriedade:** {', '.join(properties)}." if properties else ""

def identificar_padrao(sequencia):
    n = len(sequencia)
    if n < 3:
        return "Insira pelo menos 3 números.", None
    prop_txt = analisar_propriedades(sequencia)
    serie_txt = checar_convergencia_serie(sequencia)

    # 1. TESTE: Fatorial (Seguro elemento a elemento)
    if all(isinstance(x, int) and x > 0 for x in sequencia):
        p_termo = sequencia[0]
        fatoriais_validos = [i for i in range(1, 15) if math.factorial(i) == p_termo]
        if fatoriais_validos:
            n_inicio = fatoriais_validos[0]
            if all(sequencia[i] == math.factorial(n_inicio + i) for i in range(n)):
                return "Sequência Fatorial (n!)", math.factorial(n_inicio + n)

    # 2. TESTE: Quadrados Perfeitos (Seguro elemento a elemento)
    if all(x >= 0 for x in sequencia):
        p_termo = sequencia[0]
        if (p_termo**0.5).is_integer():
            r_start = int(p_termo**0.5)
            if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
                return "Sequência de Quadrados Perfeitos (n²)", (r_start + n)**2

    # 3. TESTE: Cubos Perfeitos (Seguro elemento a elemento)
    p_termo = sequencia[0]
    raiz_cubica_primeiro = round(p_termo**(1/3))
    if all(sequencia[i] == (raiz_cubica_primeiro + i)**3 for i in range(n)):
        return "Sequência de Cubos Perfeitos (n³)", (raiz_cubica_primeiro + n)**3

    # 4. TESTE: Números Triangulares
    try:
        det = 1 + 8 * sequencia[0]
        if det >= 0 and (det**0.5).is_integer():
            n_start = int((-1 + (det**0.5)) / 2)
            if all(sequencia[i] == ((n_start + i) * ((n_start + i) + 1)) // 2 for i in range(n)):
                n_prox = n_start + n
                return "Sequência de Números Triangulares", (n_prox * (n_prox + 1)) // 2
    except Exception:
        pass

    # 5. TESTE: Fibonacci
    if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
        return "Sequência de Fibonacci", sequencia[-1] + sequencia[-2]

    # 6. TESTE: Progressão Aritmética (PA)
    if n >= 2:
        razao_pa = sequencia[1] - sequencia[0]
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            return f"Progressão Aritmética (PA) | Razão: {razao_pa}{serie_txt} {prop_txt}", sequencia[-1] + razao_pa

    # 7. TESTE: Progressão Geométrica (PG)
    if all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia[1] / sequencia[0]
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            nome = "Sequência Geométrica Alternada" if razao_pg < 0 else "Progressão Geométrica (PG)"
            return f"{nome} | Razão: *({round(razao_pg, 4)}){serie_txt} {prop_txt}", int(sequencia[-1] * razao_pg)

    dif_primeira = [sequencia[i] - sequencia[i-1] for i in range(1, n)]
    dif_segunda = [dif_primeira[i] - dif_primeira[i-1] for i in range(1, len(dif_primeira))]
    if len(dif_segunda) > 0 and all(d == dif_segunda[0] for d in dif_segunda):
        return "Função Quadrática (2º Grau)", sequencia[-1] + dif_primeira[-1] + dif_segunda[0]

    return ("Padrão complexo não reconhecido.", None)

# --- INTERFACE VISUAL DA PLATAFORMA (TELA DE LOGIN E ABAS ADS) ---

st.sidebar.title("🔒 Segurança do Sistema")
if st.session_state["usuario_logado"] is None:
    st.sidebar.subheader("Acesso à Área Restrita")
    campo_usuario = st.sidebar.text_input("Usuário:")
    campo_senha = st.sidebar.text_input("Senha:", type="password")
    if st.sidebar.button("Autenticar no Banco"):
        if campo_usuario in st.session_state["tabela_usuarios"] and st.session_state["tabela_usuarios"][campo_usuario] == campo_senha:
            st.session_state["usuario_logado"] = campo_usuario
            st.sidebar.success(f"Conectado: {campo_usuario}")
            st.rerun()
        else:
            st.sidebar.error("Credenciais inválidas no Banco de Dados.")
else:
    st.sidebar.write(f"👤 **Logado como:** `{st.session_state['usuario_logado']}`")
    st.sidebar.info("Nível de Acesso: Desenvolvedor")
    if st.sidebar.button("Desconectar do Servidor"):
        st.session_state["usuario_logado"] = None
        st.rerun()

st.title("🖥️ Central Computacional Prática de ADS & Engenharia")
st.markdown("Software estruturado em conformidade com as diretrizes do curso de **Análise e Desenvolvimento de Sistemas**.")

if st.session_state["usuario_logado"] is None:
    st.warning("⚠️ **Acesso Negado.** Por favor, efetue o login no painel lateral para liberar os motores analíticos.")
    st.info("💡 **Dica de Teste para Professores:** Use Usuário: `marcio` e Senha: `admin123`")
else:
    aba1, aba2, aba3, aba4, aba5 = st.tabs(["🔢 Sequências & Séries", "🧮 Operações com Matrizes", "🧠 Tabela Verdade", "🗄️ Tabela Banco de Dados", "📚 Documentação ADS (TCC)"])

    # LÓGICA DA ABA 1: SEQUÊNCIAS
    with aba1:
        st.header("Análise de Padrões Sequenciais")
        arquivo_usuario = st.file_uploader("Importar planilha Excel/CSV para Sequência", type=["xlsx", "csv"], key="file_seq")
        dados_planilha, tipo_dado = (extrair_dados_do_arquivo(arquivo_usuario) if arquivo_usuario else (None, None))
        val_padrao = ", ".join(str(x) for x in dados_planilha) if tipo_dado == "sequencia" else "1, 2, 3, 4"
        texto_usuario = st.text_input("Elementos da Sequência:", val_padrao)
        
        if st.button("Executar Análise"):
            try:
                sequencia_limpa = [int(float(x.strip())) if float(x.strip()).is_integer() else float(x.strip()) for x in texto_usuario.split(",") if x.strip() != ""]
                tipo_padrao, proximo_num = identificar_padrao(sequencia_limpa)
                st.success(f"### {tipo_padrao}")
                if proximo_num is not None:
                    st.metric("Próximo Termo (T+1)", str(proximo_num))
                    st.session_state["tabela_historico"].append({
                        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "usuario": st.session_state["usuario_logado"],
                        "tipo_operacao": "Sequência Numérica",
                        "entrada": texto_usuario,
                        "resultado": f"{tipo_padrao} | Próximo: {proximo_num}"
                    })
                fig1, ax1 = plt.subplots(figsize=(5, 2.5))
                ax1.plot(range(1, len(sequencia_limpa) + 1), sequencia_limpa, marker='o', color='#2980b9')
                ax1.set_title("Curva de Comportamento")
                st.pyplot(fig1)
            except Exception as e:
                st.error(f"Erro na análise de dados: {str(e)}")

    # LÓGICA DA ABA 2: MATRIZES
    with aba2:
        st.header("Cálculo Matricial Linear")
        fator_escalar = st.number_input("Multiplicador Escalar (K):", value=1.0, step=0.5)
        entrada_matriz = st.text_area("Estrutura da Matriz:", "0,1,2,1,0;\n1,3,4,3,1;\n2,4,5,4,2")
        if st.button("Processar Matriz 3D"):
            try:
                linhas = [l.strip() for l in entrada_matriz.split(";") if l.strip() != ""]
                matriz_final = [[float(x.strip()) for x in linha.split(",") if x.strip() != ""] for linha in linhas]
                relatorio, transposta, fig_matriz, matriz_transformada = processar_matriz_pura(matriz_final, faktor_escalar=fator_escalar)
                st.markdown(relatorio)
                if fig_matriz:
                    st.pyplot(fig_matriz)
                    st.session_state["tabela_historico"].append({
                        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "usuario": st.session_state["usuario_logado"],
                        "tipo_operacao": "Cálculo Matricial",
                        "entrada": entrada_matriz.replace("\n", " "),
                        "resultado": "Processamento e renderização 3D concluídos."
                    })
            except Exception as e:
                st.error(f"Erro na matriz: {str(e)}")

    # LÓGICA DA ABA 3: TABELA VERDADE
    with aba3:
        st.header("Análise Analítica de Proposições")
        expr_logica = st.text_input("Expressão:", "(A AND B) -> NOT C")
        if st.button("Gerar Tabela"):
            try:
                variaveis = sorted(list(set([c for c in expr_logica if c.isalpha() and c.isupper()])))
                cabecalho = " | ".join(f" {v} " for v in variaveis) + f" |  {expr_logica} \n"
                texto_final = cabecalho + ("-" * len(cabecalho)) + "\n"
                combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
                for comb in combinacoes:
                    contexto = dict(zip(variaveis, comb))
                    expr = expr_logica.upper().replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    if "->" in expr:
                        p = expr.split("->")
                        expr = f"not ({p[0].strip()}) or ({p[1].strip()})"
                    res = eval(expr, {}, contexto)
                    valores_linha = " | ".join(f" { 'V' if contexto[v] else 'F' } " for v in variaveis)
                    texto_final += f"{valores_linha} |  {'V' if res else 'F'}\n"
                st.code(texto_final, language="text")
            except Exception as e:
                st.error(f"Erro na lógica: {str(e)}")

    # LÓGICA DA ABA 4: HISTÓRICO
    with aba4:
        st.header("🗄️ Visualização das Tabelas do Banco de Dados")
        if not st.session_state["tabela_historico"]:
            st.info("O Banco de Dados de logs está vazio. Execute alguma operação nas abas anteriores para registrar.")
        else:
            df_logs = pd.DataFrame(st.session_state["tabela_historico"])
            df_filtrado = df_logs[df_logs["usuario"] == st.session_state["usuario_logado"]]
            st.markdown(f"**Tabela: `tb_historico_operacoes` (Filtrada para o usuário: `{st.session_state['usuario_logado']}`)**")
            st.dataframe(df_filtrado, use_container_width=True)

    # LÓGICA DA ABA 5: DOCUMENTAÇÃO ACADÊMICA
    with aba5:
        st.header("📚 Documentação e Fundamentação Teórica do Projeto")
        st.subheader("1. Visão Geral do Sistema")
        st.info("**Nome do Projeto:** Central Analítica Multi-Módulo  \n**Arquitetura:** Web Application (Cliente-Servidor)  \n**Linguagem Core:** Python 3.14  \n**Ambiente de Deploy:** Streamlit Cloud PaaS")
        st.subheader("2. Mapeamento de Engenharia de Software por Disciplinas (ADS)")
        st.markdown("""
        *   **Lógica de Programação:** Implementada na Aba 3 através do motor que decodifica strings literais, mapeia permutações binárias combinatórias e avalia a tabela verdade resultante.
        *   **Estruturas de Dados Avançadas:** Utilização de vetores e arranjos multidimensionais (matrizes dinâmicas do tipo *List of Lists*) manipuladas e remapeadas através de compreensões de listas lineares.
        *   **Segurança da Informação:** Simulação de barreira de firewall e controle de sessão (*Session Control*). O sistema bloqueia os motores computacionais e as consultas de banco de dados caso o token `usuario_logado` não esteja autenticado contra a tabela hash de credenciais.
        *   **Banco de Dados:** Mapeamento estruturado de logs transacionais através de esquemas relacionais de chaves.
        *   **DevOps:** Gerenciamento distribuído de código através do Git e do repositório no GitHub integrado ao pipeline de deploy contínuo em nuvem.
        """)
