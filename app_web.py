"""
Analisador de Sequências Numéricas, Matrizes e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro)
Versão: V11.0 (Mapas de Calor para Matrizes e Gráficos de Engenharia)
Ano: 2026
"""

import streamlit as st
import math
from fractions import Fraction
import itertools
import matplotlib.pyplot as plt

# Configuração global da página Web
st.set_page_config(
    page_title="Central Analítica de Engenharia", 
    page_icon="📊", 
    layout="wide"
)

# --- SISTEMA 1: PROCESSAMENTO E PLOTAGEM DE MATRIZES ---
def processar_matriz_textual(texto_matriz):
    try:
        # Quebra as linhas pelo ponto e vírgula
        linhas_puras = [l.strip() for l in texto_matriz.split(";") if l.strip() != ""]
        matriz = []
        
        for linha in linhas_puras:
            # Quebra os elementos de cada linha por vírgula
            valores = [float(x.strip()) for x in linha.split(",") if x.strip() != ""]
            if valores:
                matriz.append(valores)
                
        num_linhas = len(matriz)
        num_colunas = len(matriz[0]) if num_linhas > 0 else 0
        
        # Validação de consistência geométrica da matriz
        if not all(len(l) == num_colunas for l in matriz):
            return "Erro: A matriz possui linhas com comprimentos desalinhados ou diferentes.", None, None
            
        # Cálculo da Matriz Transposta (linhas viram colunas)
        transposta = [[matriz[j][i] for j in range(num_linhas)] for i in range(num_colunas)]
        
        det_txt = "N/A (Apenas matrizes quadradas 2x2 ou 3x3 possuem determinante estável)."
        if num_linhas == num_colunas:
            if num_linhas == 2:
                det = (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])
                det_txt = f"{round(det, 4)}"
            elif num_linhas == 3:
                d1 = (matriz[0][0]*matriz[1][1]*matriz[2][2]) + (matriz[0][1]*matriz[1][2]*matriz[2][0]) + (matriz[0][2]*matriz[1][0]*matriz[2][1])
                d2 = (matriz[0][2]*matriz[1][1]*matriz[2][0]) + (matriz[0][0]*matriz[1][2]*matriz[2][1]) + (matriz[0][1]*matriz[1][0]*matriz[2][2])
                det_txt = f"{round(d1 - d2, 4)}"
                
        relatorio = f"**Dimensão Identificada:** {num_linhas}x{num_colunas}  \n**Determinante Matemático:** {det_txt}"
        
        # --- GERAÇÃO DO GRÁFICO DA MATRIZ (MAPA DE CALOR) ---
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        # matshow plota os dados como uma imagem colorida de engenharia (Gradiente Viridis)
        cax = ax.matshow(matriz, cmap="viridis")
        fig.colorbar(cax, ax=ax, label="Escala de Valores")
        
        # Adiciona os valores numéricos como texto dentro de cada quadrado do gráfico
        for i in range(num_linhas):
            for j in range(num_colunas):
                ax.text(j, i, f"{round(matriz[i][j], 2)}", ha='center', va='center', 
                        color='white' if matriz[i][j] < (max(max(matriz)) / 2) else 'black', fontweight='bold')
                        
        ax.set_title("Distribuição Espacial de Intensidade (Matriz)", pad=15, fontsize=10, fontweight="bold")
        fig.tight_layout()
        
        return relatorio, transposta, fig
    except Exception:
        return "Erro analítico: Verifique se utilizou vírgulas para separar colunas e ponto e vírgula para linhas.", None, None

# --- SISTEMA 2: TESTE DE CONVERGÊNCIA DE SÉRIES ---
def checar_convergencia_serie(sequencia):
    n = len(sequencia)
    if n < 3:
        return ""
        
    if all(abs(sequencia[i] - (1 / (i + 1))) < 0.05 for i in range(n)):
        return "\n\n**Análise Estatística de Série:** Série Harmônica Divergente ($\sum 1/n$).  \n*Comportamento:* A soma dos infinitos termos diverge lentamente para o infinito."
        
    if all(x != 0 for x in sequencia):
        razao = sequencia[1] / sequencia[0]
        if abs(razao) < 1 and all(abs((sequencia[i] / sequencia[i-1]) - razao) < 0.01 for i in range(1, n)):
            soma_limite = sequencia[0] / (1 - razao)
            return f"\n\n**Análise Estatística de Série:** Série Geométrica Convergente.  \n*Comportamento:* Estabiliza no limite numérico real exato de **{round(soma_limite, 4)}** se somada até o infinito."
            
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
        primeiro_termo = sequencia[0]
        fatoriais_validos = [i for i in range(1, 15) if math.factorial(i) == primeiro_termo]
        if fatoriais_validos:
            n_inicio = fatoriais_validos[0]
            if all(sequencia[i] == math.factorial(n_inicio + i) for i in range(n)):
                proximo = math.factorial(n_inicio + n)
                return "Sequência Fatorial (n!)\nRegra: Multiplicação sucessiva.", proximo

    if all(x >= 0 for x in sequencia) and (sequencia[0]**0.5).is_integer():
        r_start = int(sequencia[0]**0.5)
        if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
            proximo = (r_start + n)**2
            return "Sequência de Quadrados Perfeitos (n²)\nRegra: Potências quadráticas.", proximo

    raiz_cubica_primeiro = round(sequencia[0]**(1/3))
    if all(sequencia[i] == (raiz_cubica_primeiro + i)**3 for i in range(n)):
        proximo = (raiz_cubica_primeiro + n)**3
        return "Sequência de Cubos Perfeitos (n³)\nRegra: Números elevados ao cubo.", proximo

    try:
        det = 1 + 8 * sequencia[0]
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

    if sequencia[0] == 2 and sequencia[1] == 1:
        if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
            proximo = sequencia[-1] + sequencia[-2]
            return "Sequência de Lucas\nRegra: Variação de Fibonacci iniciando em 2 e 1.", proximo

    if n >= 2:
        razao_pa = sequencia[1] - sequencia[0]
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            proximo = sequencia[-1] + razao_pa
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
            return f"Progressão Aritmética (PA)\nRazão: {'+' if razao_pa >= 0 else ''}{razao_pa}{serie_txt}\n\n{prop_txt}", proximo

    if all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia[1] / sequencia[0]
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            proximo = sequencia[-1] * razao_pg
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else round(proximo, 4)
            nome = "Sequência Geométrica Alternada" if razao_pg < 0 else "Progressão Geométrica (PG)"
            return f"{nome}\nRazão Multiplicativa: *({round(razao_pg, 4)}){serie_txt}\n\n{prop_txt}", proximo

    dif_primeira = [sequencia[i] - sequencia[i-1] for i in range(1, n)]
    dif_segunda = [dif_primeira[i] - dif_primeira[i-1] for i in range(1, len(dif_primeira))]
    if len(dif_segunda) > 0 and all(d == dif_segunda[0] for d in dif_segunda):
        proxima_dif = dif_primeira[-1] + dif_segunda[0]
        proximo = sequencia[-1] + proxima_dif
        proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
        return "Função Quadrática (2º Grau)\nA variação muda de forma constante." + serie_txt, proximo

    return ("Padrão estrutural não reconhecido.\n\n" + prop_txt if prop_txt else "Padrão complexo não reconhecido.", None)

# --- INTERFACE VISUAL PRINCIPAL DA INTERNET (STREAMLIT) ---

# Barra lateral corporativa com informações de autoria
st.sidebar.title("⚙️ Painel de Controle")
st.sidebar.markdown("---")
st.sidebar.write("**Desenvolvido por:**")
st.sidebar.info("Marcio de Andrade Neves (Engenheiro)")
st.sidebar.write("**Versão:** V11.0 (Mapas de Matrizes)")

st.title("📊 Central Computacional de Lógica e Engenharia")
st.markdown("Plataforma web avançada para avaliação de sequências lógicas, séries infinitas e matrizes lineares.")

# Definição das Abas estruturadas
aba1, aba2, aba3 = st.tabs(["🔢 Sequências & Séries", "🧮 Operações com Matrizes", "🧠 Lógica Proposicional"])

# LÓGICA DA ABA 1: SEQUÊNCIAS E SÉRIES
with aba1:
    st.header("Análise Gráfica de Curvas e Convergência")
    texto_usuario = st.text_input("Insira os termos numéricos separados por vírgula:", "1, 2, 3, 4")
    
    if st.button("Analisar Sequência"):
        try:
            sequencia = []
            for x in texto_usuario.split(","):
                if x.strip() != "":
                    termo = x.strip()
                    if "/" in termo:
                        sequencia.append(float(Fraction(termo)))
                    else:
                        num = float(termo)
                        sequencia.append(int(num) if num.is_integer() else num)
                        
            tipo_padrao, proximo_num = identificar_padrao(sequencia)
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"### {tipo_padrao}")
                if proximo_num is not None:
                    st.metric(label="Próximo Termo Projetado (T+1)", value=str(proximo_num))
            
            with col2:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                eixo_x_original = list(range(1, len(sequencia) + 1))
                ax.plot(eixo_x_original, sequencia, marker='o', color='#2980b9', linewidth=2, label="Dados")
                if proximo_num is not None:
                    eixo_x_proximo = len(sequencia) + 1
                    ax.plot([eixo_x_original[-1], eixo_x_proximo], [sequencia[-1], proximo_num], linestyle='--', color='#27ae60')
                    ax.scatter(eixo_x_proximo, proximo_num, color='#27ae60', zorder=5, s=60, label=f"Proximo ({proximo_num})")
                ax.set_title("Curva do Comportamento Numérico")
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.legend()
                st.pyplot(fig)
        except Exception:
            st.error("Erro na leitura. Verifique se utilizou apenas números, pontos ou frações.")

# LÓGICA DA ABA 2: OPERAÇÕES COM MATRIZES (COMPLEMENTADA COM COLUNAS E GRÁFICOS)
with aba2:
    st.header("Cálculo Matricial e Mapas de Intensidade")
    st.markdown("Insira os elementos da matriz. Use **vírgulas** para colunas e **ponto e vírgula** para quebrar as linhas.")
    
    # Exemplo padrão: malha de gradiente numérico para o gráfico ficar bonito
    entrada_matriz = st.text_area("Estrutura da Matriz:", "1, 2, 3;\n4, 5, 6;\n7, 8, 9")
    
    if st.button("Calcular Propriedades e Plotar Matriz"):
        relatorio, transposta, fig_matriz = processar_matriz_textual(entrada_matriz)
        
        if transposta is None:
            st.error(relatorio)
        else:
            col_mat1, col_mat2 = st.columns(2)
            
            with col_mat1:
                st.success("### Resultados Analíticos")
                st.markdown(relatorio)
                
                txt_transposta = ""
                for linha in transposta:
                    txt_transposta += " | ".join(f"{x:6}" for x in linha) + "\n"
                    
                st.markdown("**Matriz Transposta Resultante:**")
                st.code(txt_transposta, language="text")
                
            with col_mat2:
                # Exibe o gráfico bidimensional da matriz no site
                if fig_matriz:
                    st.pyplot(fig_matriz)

# LÓGICA DA ABA 3: LÓGICA PROPOSICIONAL
with aba3:
    st.header("Gerador Analítico de Tabela Verdade")
    expressao_original = st.text_input("Digite a proposição composto:", "(A AND B) -> NOT C")
    
    if st.button("Gerar Tabela Verdade"):
        try:
            variaveis = sorted(list(set([c for c in expressao_original if c.isalpha() and c.isupper()])))
            if not variaveis:
                st.warning("Insira proposições com letras maiúsculas (A, B, C...).")
            else:
                cabecalho = " | ".join(f" {v} " for v in variaveis) + f" |  {expressao_original} \n"
                texto_final = cabecalho + ("-" * len(cabecalho)) + "\n"
                combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
                
                for comb in combinacoes:
                    contexto = dict(zip(variaveis, comb))
                    expr = expressao_original.upper()
                    expr = expr.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    
                    if "<->" in expr:
                        partes = expr.split("<->")
                        expr = f"({partes.strip()}) == ({partes.strip()})"
                    elif "->" in expr:
                        partes = expr.split("->")
                        expr = f"not ({partes.strip()}) or ({partes.strip()})"

                    resultado_bool = eval(expr, {}, contexto)
                    valores_linha = " | ".join(f" { 'V' if contexto[v] else 'F' } " for v in variaveis)
                    texto_final += f"{valores_linha} |  {'V' if resultado_bool else 'F'}\n"
                
                st.code(texto_final, language="text")
        except Exception:
            st.error("Erro na sintaxe proposicional. Revise os conectivos lógicos e parênteses.")
