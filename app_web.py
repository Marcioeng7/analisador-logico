"""
Analisador de Sequências Numéricas e Padrões Lógicos
Autor: Marcio de Andrade Neves (Engenheiro)
Versão: V9.0 (Inclusão de Cubos, Triangulares e Números de Lucas)
Ano: 2026
"""

import streamlit as st
import math
from fractions import Fraction
import itertools
import matplotlib.pyplot as plt

# Configuração da página Web
st.set_page_config(
    page_title="Analisador de Padrões Lógicos", 
    page_icon="📊", 
    layout="wide"
)

# Funções Auxiliares Matemáticas de Engenharia
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
    propriedades = []
    if all(x % 2 == 0 for x in sequencia):
        propriedades.append("Apenas Números Pares")
    elif all(x % 2 != 0 for x in sequencia):
        propriedades.append("Apenas Números Ímpares")
    if all(eh_primo(x) for x in sequencia):
        propriedades.append("Apenas Números Primos")
    return f"**Propriedade dos Termos:** {', '.join(propriedades)}." if propriedades else ""

def identificar_padrao(sequencia):
    n = len(sequencia)
    if n < 3:
        return "Insira pelo menos 3 números para análise.", None
        
    prop_txt = analisar_propriedades(sequencia)

    # 1. TESTE: Fatorial
    if all(isinstance(x, int) and x > 0 for x in sequencia):
        primeiro_termo = sequencia[0]
        fatoriais_validos = [i for i in range(1, 15) if math.factorial(i) == primeiro_termo]
        if fatoriais_validos:
            n_inicio = fatoriais_validos[0]
            if all(sequencia[i] == math.factorial(n_inicio + i) for i in range(n)):
                proximo = math.factorial(n_inicio + n)
                return "Sequência Fatorial (n!)\nRegra: Multiplicação sucessiva.", proximo

    # 2. TESTE: Quadrados Perfeitos (n²)
    if all(x >= 0 for x in sequencia) and (sequencia[0]**0.5).is_integer():
        r_start = int(sequencia[0]**0.5)
        if all(sequencia[i] == (r_start + i)**2 for i in range(n)):
            proximo = (r_start + n)**2
            return "Sequência de Quadrados Perfeitos (n²)\nRegra: Potências quadráticas.", proximo

    # 3. NOVO TESTE: Cubos Perfeitos (n³)
    raiz_cubica_primeiro = round(sequencia[0]**(1/3))
    if all(sequencia[i] == (raiz_cubica_primeiro + i)**3 for i in range(n)):
        proximo = (raiz_cubica_primeiro + n)**3
        return "Sequência de Cubos Perfeitos (n³)\nRegra: Números elevados ao cubo.", proximo

    # 4. NOVO TESTE: Números Triangulares [n*(n+1)/2]
    try:
        det = 1 + 8 * sequencia[0]
        if det >= 0 and (det**0.5).is_integer():
            n_start = int((-1 + (det**0.5)) / 2)
            if all(sequencia[i] == ((n_start + i) * ((n_start + i) + 1)) // 2 for i in range(n)):
                n_prox = n_start + n
                proximo = (n_prox * (n_prox + 1)) // 2
                return "Sequência de Números Triangulares\nRegra: Somatório de pontos geométricos.", proximo
    except Exception:
        pass

    # 5. TESTE: Sequência de Fibonacci
    if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
        proximo = sequencia[-1] + sequencia[-2]
        return "Sequência de Fibonacci\nRegra: Soma dos dois termos anteriores.", proximo

    # 6. NOVO TESTE: Sequência de Lucas (Começa com 2 e 1)
    if sequencia[0] == 2 and sequencia[1] == 1:
        if all(sequencia[i] == sequencia[i-1] + sequencia[i-2] for i in range(2, n)):
            proximo = sequencia[-1] + sequencia[-2]
            return "Sequência de Lucas\nRegra: Variação de Fibonacci iniciando em 2 e 1.", proximo

    # 7. TESTE: Progressão Aritmética (PA)
    if n >= 2:
        razao_pa = sequencia[1] - sequencia[0]
        if all(sequencia[i] - sequencia[i-1] == razao_pa for i in range(1, n)):
            proximo = sequencia[-1] + razao_pa
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
            return f"Progressão Aritmética (PA)\nRazão: {'+' if razao_pa >= 0 else ''}{razao_pa}\n\n{prop_txt}", proximo

    # 8. TESTE: Progressão Geométrica (PG)
    if all(x != 0 for x in sequencia) and n >= 2:
        razao_pg = sequencia[1] / sequencia[0]
        if all(sequencia[i] / sequencia[i-1] == razao_pg for i in range(1, n)):
            proximo = sequencia[-1] * razao_pg
            proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else round(proximo, 4)
            nome = "Sequência Geométrica Alternada" if razao_pg < 0 else "Progressão Geométrica (PG)"
            return f"{nome}\nRazão Multiplicativa: *({round(razao_pg, 4)})\n\n{prop_txt}", proximo

    # 9. TESTE: Função Quadrática (2º Grau)
    dif_primeira = [sequencia[i] - sequencia[i-1] for i in range(1, n)]
    dif_segunda = [dif_primeira[i] - dif_primeira[i-1] for i in range(1, len(dif_primeira))]
    if len(dif_segunda) > 0 and all(d == dif_segunda[0] for d in dif_segunda):
        proxima_dif = dif_primeira[-1] + dif_segunda[0]
        proximo = sequencia[-1] + proxima_dif
        proximo = int(proximo) if isinstance(proximo, float) and proximo.is_integer() else proximo
        return "Função Quadrática (2º Grau)\nA variação muda de forma constante.", proximo

    return ("Padrão estrutural não reconhecido.\n\n" + prop_txt if prop_txt else "Padrão complexo não reconhecido.", None)
# --- INTERFACE VISUAL DA PÁGINA WEB ---

# Barra lateral com créditos do autor de engenharia
st.sidebar.title("Informações Técnicas")
st.sidebar.markdown("---")
st.sidebar.write("**Desenvolvido por:**")
st.sidebar.info("Marcio de Andrade Neves (Engenheiro)")
st.sidebar.write("**Versão:** V9.0 (Nuvem / Novas Fórmulas)")

# Título principal da página web
st.title("📊 Analisador de Padrões Lógicos")
st.markdown("Bem-vindo ao software de predição numérica e tabelas verdade.")

# Criação das Abas de navegação Web
aba1, aba2 = st.tabs(["🔢 Sequências Numéricas", "🧠 Lógica Proposicional"])

# --- LÓGICA DA ABA 1: SEQUÊNCIAS ---
with aba1:
    st.header("Análise de Tendência e Curvas Numéricas")
    
    texto_usuario = st.text_input("Digite inteiros, decimais ou frações separados por vírgula:", "1, 8, 27, 64")
    
    if st.button("Descobrir Padrão Numérico"):
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
                    st.metric(label="Próximo Termo Estimado (T+1)", value=str(proximo_num))
            
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
            st.error("Erro na leitura da sequência. Verifique os separadores.")

# --- LÓGICA DA ABA 2: LÓGICA PROPOSICIONAL ---
with aba2:
    st.header("Gerador Analítico de Tabela Verdade")
    
    expressao_original = st.text_input("Digite a expressão lógica:", "(P AND Q) -> NOT R")
    
    if st.button("Gerar Tabela Verdade Web"):
        try:
            variaveis = sorted(list(set([c for c in expressao_original if c.isalpha() and c.isupper()])))
            
            if not variaveis:
                st.warning("Nenhuma variável lógica encontrada (Use letras maiúsculas).")
            else:
                cabecalho = " | ".join(f" {v} " for v in variaveis) + f" |  {expressao_original} \n"
                divisor = "-" * len(cabecalho) + "\n"
                
                texto_final = cabecalho + divisor
                combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
                
                for comb in combinacoes:
                    contexto = dict(zip(variaveis, comb))
                    expr = expressao_original.upper()
                    expr = expr.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
                    
                    if "<->" in expr:
                        partes = expr.split("<->")
                        expr = f"({partes[0].strip()}) == ({partes[1].strip()})"
                    elif "->" in expr:
                        partes = expr.split("->")
                        expr = f"not ({partes[0].strip()}) or ({partes[1].strip()})"

                    resultado_bool = eval(expr, {}, contexto)
                    valores_linha = " | ".join(f" { 'V' if contexto[v] else 'F' } " for v in variaveis)
                    res_linha = "V" if resultado_bool else "F"
                    
                    texto_final += f"{valores_linha} |  {res_linha}\n"
                
                st.code(texto_final, language="text")
                
        except Exception:
            st.error("Erro na sintaxe proposicional. Verifique os parênteses.")
