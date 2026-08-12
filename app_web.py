"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro)
Versão: V14.1 (Correção Definitiva do Interpretador da Tabela Verdade)
Ano: 2026
"""

import streamlit as st
import math
from fractions import Fraction
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuração global da página Web
st.set_page_config(
    page_title="Central Analítica de Engenharia", 
    page_icon="📊", 
    layout="wide"
)

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
            return [float(x) for x in dados if pd.notna(x)], "sequencia"
        if len(dados) == 1:
            return [float(linha) for linha in dados if pd.notna(linha)], "sequencia"
        
        matriz_limpa = [[float(x) for x in linha if pd.notna(x)] for linha in dados]
        return matriz_limpa, "matriz"
    except Exception:
        st.error("Erro ao ler o arquivo. Certifique-se de que a planilha possui apenas números.")
        return None, None

# --- SISTEMA 1: PROCESSAMENTO E PLOTAGEM DE MATRIZES ---
def processar_matriz_pura(matriz):
    try:
        num_linhas = len(matriz)
        num_colunas = len(matriz) if num_linhas > 0 else 0
        
        if not all(len(l) == num_colunas for l in matriz):
            return "Erro: A matriz possui linhas com comprimentos desalinhados.", None, None
            
        transposta = [[matriz[j][i] for j in range(num_linhas)] for i in range(num_colunas)]
        
        det_txt = "N/A (Apenas matrizes quadradas 2x2 ou 3x3 possuem determinante estável)."
        if num_linhas == num_colunas:
            if num_linhas == 2:
                det = (matriz * matriz) - (matriz * matriz)
                det_txt = f"{round(det, 4)}"
            elif num_linhas == 3:
                d1 = (matriz*matriz*matriz) + (matriz*matriz*matriz) + (matriz*matriz*matriz)
                d2 = (matriz*matriz*matriz) + (matriz*matriz*matriz) + (matriz*matriz*matriz)
                det_txt = f"{round(d1 - d2, 4)}"
                
        relatorio = f"**Dimensão Identificada:** {num_linhas}x{num_colunas}  \n**Determinante Matemático:** {det_txt}"
        
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111, projection='3d')
        
        x = np.arange(0, num_colunas, 1)
        y = np.arange(0, num_linhas, 1)
        X, Y = np.meshgrid(x, y)
        Z = np.array(matriz)
        
        surf = ax.plot_surface(X, Y, Z, cmap="coolwarm", edgecolor='none', alpha=0.9)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label="Escala Z")
        
        ax.set_title("Projeção Topográfica de Superfície 3D", fontsize=9, fontweight="bold", pad=10)
        ax.set_xlabel("Colunas (X)", fontsize=7)
        ax.set_ylabel("Linhas (Y)", fontsize=7)
        ax.set_zlabel("Valores (Z)", fontsize=7)
        ax.tick_params(labelsize=6)
        
        return relatorio, transposta, fig
    except Exception as e:
        return f"Erro analítico interno: {str(e)}", None, None

# --- SISTEMA 2: TESTE DE CONVERGÊNCIA DE SÉRIES ---
def checar_convergencia_serie(sequencia):
    n = len(sequencia)
    if n < 3:
        return ""
    if all(abs(sequencia[i] - (1 / (i + 1))) < 0.05 for i in range(n)):
        return "\n\n**Análise Estatística de Série:** Série Harmônica Divergente ($\sum 1/n$).  \n*Comportamento:* A soma dos infinitos termos diverge lentamente para o infinito."
    if all(x != 0 for x in sequencia):
        try:
            razao = sequencia / sequencia
            if abs(razao) < 1 and all(abs((sequencia[i] / sequencia[i-1]) - razao) < 0.01 for i in range(1, n)):
                soma_limite = sequencia / (1 - razao)
                return f"\n\n**Análise Estatística de Série:** Série Geométrica Convergente.  \n*Comportamento:* Estabiliza no limite numérico real exato de **{round(soma_limite, 4)}** se somada até o infinito."
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
        properties.append("Apenas Números Pares")
    elif all(x % 2 != 0 for x in sequencia):
        properties.append("Apenas Números Ímpares")
    if all(eh_primo(x) for x in sequencia):
        properties.append("Apenas Números Primos")
    return f"**Propriedade dos Termos:** {', '.join(properties)}." if properties else ""

def identificar_padrao(sequencia):
    n = len(sequencia)
    if n < 3:
        return "Insira pelo menos 3 números para análise.", None
        
    prop_txt = analisar_propriedades(sequencia)
    serie_txt = checar_convergencia_serie(sequencia)

    if all(isinstance(x, int) and x > 0 for x in sequencia):
        primeiro_termo = sequencia
        fatoriais_validos = [i for i in range(1, 15) if math.factorial(i) == primeiro_termo]
        if fatoriais_validos:
            n_inicio = fatoriais_validos
            if all(sequencia[i] == math.factorial(n_inicio + i) for i in range(n)):
                proximo = math.factorial(n_inicio + n)
                return "Sequência Fatorial (n!)\nRegra: Multiplicação sucessiva.", proximo

    if all(x >= 0 for x in sequencia) and (sequencia**0.5).is_integer():
        r_start = int(sequencia**0.5)
        if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
            proximo = (r_start + n)**2
            return "Sequência de Quadrados Perfeitos (n²)\nRegra: Potências quadráticas.", proximo

    raiz_cubica_primeiro = round(sequencia**(1/3))
    if all(sequencia[i] == (raiz_cubica_primeiro + i)**3 for i in range(n)):
        proximo = (raiz_cubica_primeiro + n)**3
        return "Sequência de Cubos Perfeitos (n³)\nRegra: Números elevados ao cubo.", proximo

    try:
        det = 1 + 8 * sequencia
        if det >= 0 and (det**0.5).is_integer():
            n_start = int((-1 + (det**0.5)) / 2)
            if all(sequencia[i] == ((n_start + i) * ((n_start + i) + 1)) // 2 for i in range(n)):
                n_prox = n_start + n
                proximo = (n_prox * (n_prox + 1)) // 2
                return "Sequência de Números Triangulares\nRegra: Somatório geométrico de pontos.", proximo
    except Exception:
        pass

    if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
        proximo = sequencia[-1] + sequencia[-2]
        return "Sequência de Fibonacci\nRegra: Soma dos dois termos anteriores.", proximo

    if sequencia == 2 and sequencia == 1:
        if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
            proximo = sequencia[-1] + sequencia[-2]
            return "Sequência de Lucas\nRegra: Variação de Fibonacci iniciando em 2 e 1.", proximo

    if n >= 2:
        razao_pa = sequencia - sequencia
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            proximo = sequencia[-1] + razao_pa
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
            return f"Progressão Aritmética (PA)\nRazão: {'+' if razao_pa >= 0 else ''}{razao_pa}{serie_txt}\n\n{prop_txt}", proximo

    if all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia / sequencia
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            proximo = sequencia[-1] * razao_pg
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else round(proximo, 4)
            name = "Sequência Geométrica Alternada" if razao_pg < 0 else "Progressão Geométrica (PG)"
            return f"{name}\nRazão Multiplicativa: *({round(razao_pg, 4)}){serie_txt}\n\n{prop_txt}", proximo

    dif_primeira = [sequencia[i] - sequencia[i-1] for i in range(1, n)]
    dif_segunda = [dif_primeira[i] - dif_primeira[i-1] for i in range(1, len(dif_primeira))]
    if len(dif_segunda) > 0 and all(d == dif_segunda for d in dif_segunda):
        proxima_dif = dif_primeira[-1] + dif_segunda
        proximo = sequencia[-1] + proxima_dif
        proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
        return "Função Quadrática (2º Grau)\nA variação muda de forma constante." + serie_txt, proximo

    return ("Padrão estrutural não reconhecido.\n\n" + prop_txt if prop_txt else "Padrão complexo não reconhecido.", None)

# --- INTERFACE VISUAL PRINCIPAL DA INTERNET (STREAMLIT) ---

st.sidebar.title("⚙️ Painel de Controle")
st.sidebar.markdown("---")
st.sidebar.write("**Desenvolvido por:**")
st.sidebar.info("Marcio de Andrade Neves (Engenheiro)")
st.sidebar.write("**Versão:** V14.1 (Correção Logica)")

st.title("📊 Central Computacional de Lógica e Engenharia")
st.markdown("Plataforma web avançada para avaliação de sequências lógicas, séries infinitas e matrizes lineares.")

# Componente de Upload de Planilhas
st.markdown("### 📥 Entrada por Arquivo Extrator (Opcional)")
arquivo_usuario = st.file_uploader("Arraste ou selecione uma planilha Excel (.xlsx) ou arquivo (.csv)", type=["xlsx", "csv"])

dados_planilha, tipo_dado = None, None
if arquivo_usuario is not None:
    dados_planilha, tipo_dado = extrair_dados_do_arquivo(arquivo_usuario)
    if tipo_dado == "sequencia":
        st.info(f"Planilha detectada! Uma sequência de {len(dados_planilha)} números foi importada para a Aba 1.")
    elif tipo_dado == "matriz":
        st.info(f"Planilha detectada! Uma matriz foi importada para a Aba 2.")

# Definição das Abas estruturadas
aba1, aba2, aba3 = st.tabs(["🔢 Sequências & Séries", "🧮 Operações com Matrizes", "🧠 Lógica Proposicional"])

# LÓGICA DA ABA 1: SEQUÊNCIAS E SÉRIES
with aba1:
    st.header("Análise Gráfica de Curvas e Tendências")
    valor_padrao_seq = ", ".join(str(x) for x in dados_planilha) if tipo_dado == "sequencia" else "1, 2, 3, 4"
    texto_usuario = st.text_input("Insira os termos numéricos separados por vírgula (ou use o arquivo acima):", valor_padrao_seq)
    
    if st.button("Analisar Sequência"):
        try:
            sequencia = [float(Fraction(x.strip())) if "/" in x else float(x.strip()) for x in texto_usuario.split(",") if x.strip() != ""]
            sequencia_limpa = [int(num) if num.is_integer() else num for num in sequencia]
            
            tipo_padrao, proximo_num = identificar_padrao(sequencia_limpa)
            
            st.success(f"### {tipo_padrao}")
            if proximo_num is not None:
                st.metric(label="Próximo Termo Projetado (T+1)", value=str(proximo_num))
            
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                fig1, ax1 = plt.subplots(figsize=(4.5, 3.2))
                eixo_x_original = list(range(1, len(sequencia_limpa) + 1))
                ax1.plot(eixo_x_original, sequencia_limpa, marker='o', color='#2980b9', linewidth=2, label="Dados")
                if proximo_num is not None:
                    eixo_x_proximo = len(sequencia_limpa) + 1
                    ax1.plot([eixo_x_original[-1], eixo_x_proximo], [sequencia_limpa[-1], proximo_num], linestyle='--', color='#27ae60')
                    ax1.scatter(eixo_x_proximo, proximo_num, color='#27ae60', zorder=5, s=50, label=f"Prox ({proximo_num})")
                ax1.set_title("Curva de Tendência Contínua", fontsize=9, fontweight="bold")
                ax1.grid(True, linestyle=':', alpha=0.6)
                ax1.legend(fontsize=7)
                st.pyplot(fig1)
                
            with g_col2:
                fig2, ax2 = plt.subplots(figsize=(4.5, 3.2))
                termos_labels = [f"T{i}" for i in eixo_x_original]
                valores_barras = list(sequencia_limpa)
                cores_barras = ['#3498db'] * len(valores_barras)
                if proximo_num is not None:
                    termos_labels.append("T+1")
                    valores_barras.append(proximo_num)
                    cores_barras.append('#2ecc71')
                ax2.bar(termos_labels, valores_barras, color=cores_barras, edgecolor='grey', alpha=0.85)
                ax2.set_title("Histograma Discreto de Intensidade", fontsize=9, fontweight="bold")
                ax2.grid(True, axis='y', linestyle=':', alpha=0.6)
                st.pyplot(fig2)
        except Exception:
            st.error("Erro na leitura. Verifique os valores inseridos.")

# LÓGICA DA ABA 2: OPERAÇÕES COM MATRIZES
with aba2:
    st.header("Cálculo Matricial e Topografia 3D")
    if tipo_dado == "matriz":
        valor_padrao_matriz = ";\n".join(", ".join(str(x) for x in linha) for linha in dados_planilha)
    else:
        valor_padrao_matriz = "0, 1, 2, 1, 0;\n1, 3, 4, 3, 1;\n2, 4, 5, 4, 2;\n1, 3, 4, 3, 1;\n0, 1, 2, 1, 0"
        
    entrada_matriz = st.text_area("Estrutura da Matriz (Texto ou importada da planilha):", valor_padrao_matriz, height=120)
    
    if st.button("Calcular Propriedades e Plotar 3D"):
        try:
            linhas_puras = [l.strip() for l in entrada_matriz.split(";") if l.strip() != ""]
            matriz_final = [[float(x.strip()) for x in linha.split(",") if x.strip() != ""] for linha in linhas_puras]
            
            relatorio, transposta, fig_matriz = processar_matriz_pura(matriz_final)
            if transposta is None:
                st.error(relatorio)
            else:
                col_mat1, col_mat2 = st.columns(2)
                with col_mat1:
                    st.success("### Resultados Analíticos")
                    st.markdown(relatorio)
                    txt_transposta = "".join(" | ".join(f"{x:6}" for x in linha) + "\n" for linha in transposta)
                    st.markdown("**Matriz Transposta Resultante:**")
                    st.code(txt_transposta, language="text")
                with col_mat2:
                    if fig_matriz:
                        st.pyplot(fig_matriz)
        except Exception as ex:
            st.error(f"Formatação inválida da matriz: {str(ex)}")

# LÓGICA DA ABA 3: LÓGICA PROPOSICIONAL (MOTOR INTEGRAL FORMAL DE CONDICIONAIS CORRIGIDO)
with aba3:
    st.header("Gerador Analítico de Tabela Verdade")
    expressao_original = st.text_input("Digite a proposição composto:", "(A AND B) -> NOT C", key="logica_input")
    
    if st.button("Gerar Tabela Verdade"):
        try:
            # Encontra e filtra todas as letras proposicionais maiúsculas unicas
            variaveis = sorted(list(set([c for c in expressao_original if c.isalpha() and c.isupper()])))
            if not variaveis:
                st.warning("Insira proposições com letras maiúsculas.")
            else:
                cabecalho = " | ".join(f" {v} " for v in variaveis) + f" |  {expressao_original} \n"
                texto_final = cabecalho + ("-" * len(cabecalho)) + "\n"
                combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
                
                for comb in combinacoes:
                    contexto = dict(zip(variaveis, comb))
                    
                    # Padronização léxica inicial de operadores para formato do Python
                    expr = expressao_original.upper()
                    expr = expr.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    
                    # --- NOVO MECANISMO ROBUSTO DE SUBSTITUIÇÃO ANALÍTICA ---
                    # Resolve Bicondicional de forma segura através do operador booleano de igualdade
                    if "<->" in expr:
                        partes_bicond = expr.split("<->")
                        expr = f"({partes_bicond[0].strip()}) == ({partes_bicond[1].strip()})"
                    
                    # Resolve Condicional -> sem fatiar parênteses por string.
                    # Aplica a equivalência formal universal: P -> Q  <=>  (not P) or Q
                    if "->" in expr:
                        partes_cond = expr.split("->")
                        # Emoldura matematicamente o lado esquerdo em uma negação e une ao lado direito via 'or'
                        expr = f"not ({partes_cond[0].strip()}) or ({partes_cond[1].strip()})"

                    # Executa a linha traduzida de forma isolada usando o contexto lógico mapeado
                    resultado_bool = eval(expr, {}, contexto)
                    valores_linha = " | ".join(f" { 'V' if contexto[v] else 'F' } " for v in variaveis)
                    texto_final += f"{valores_linha} |  {'V' if resultado_bool else 'F'}\n"
                
                st.code(texto_final, language="text")
                
                st.download_button(
                    label="📥 Baixar Tabela Verdade (.txt)",
                    data=texto_final,
                    file_name="tabela_verdade_engenharia.txt",
                    mime="text/plain"
                )
        except Exception:
            st.error("Erro na sintaxe proposicional. Verifique se os parênteses estão fechados corretamente.")
