import streamlit as st
import pandas as pd
import os
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)
#visual
st.sidebar.image("Logo LEM.jpeg", width=300)
def main():
    ARQUIVOS = []
    DATASETS = []
    CURVAS = []
    st.title("Dashboard de tratamento de dados")

    opcao = st.sidebar.selectbox("Selecione uma opção:", ["Início", "Visualização de Dados", "Configurações"])

    if opcao == "Início":
        st.write("Bem-vindo ao Dashboard de Ensaios EMIC. Selecione uma opção no painel à esquerda.")

    elif opcao == "Visualização de Dados":
        st.header("Visualização de Dados")

        #Introduz o arquivo no sistema
        st.write("Carregue os dados dos corpos de prova:")
        uploaded_files = st.file_uploader("Carregar Arquivos TXT", type=['txt'],accept_multiple_files=True)
        for uploaded_file in uploaded_files:
           conteudo = uploaded_file.read()
           ARQUIVOS_info = {'nome': (uploaded_file.name).split(".")[0],'conteudo': conteudo}
           ARQUIVOS.append(ARQUIVOS_info)

        pasta_destino = 'csv'
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        AREA = []  # Lista para armazenar áreas por amostra
        COMPRIMENTO = []  # Lista para armazenar comprimentos por amostra
        # ---------------- Recebe os arquivos e transforma em bytes----------------#
        for uploaded_file in uploaded_files:
            stringio = StringIO(uploaded_file.getvalue().decode('latin-1'))
            string = stringio.read()
            lines = string.splitlines()
            # ---------------- Adquire os dados referentes a cada amostra--------------#
            comprimento = st.sidebar.number_input(f'Digite o comprimento da amostra {uploaded_file.name}')
            COMPRIMENTO.append(comprimento)
            area = st.sidebar.number_input(f'Digite a base da amostra {uploaded_file.name}')
            AREA.append(area)
        # ---------------- Trata para transformar em csv --------------------------#
            if lines:
                lines[0] = 'tempo[s],deformacao[mm],forca[N]'
                for i in range(1, len(lines)):
                    lines[i] = lines[i].replace('\t', ',')
                data = '\n'.join(lines)

                # Nome do arquivo
                nome_arquivo = uploaded_file.name.replace('.txt', '')

                # Caminho do arquivo CSV de destino
                caminho_arquivo_csv = os.path.join(pasta_destino, f'{nome_arquivo}.csv')

                # Salvar os dados no arquivo CSV
                with open(caminho_arquivo_csv, 'w', encoding='latin-1') as f:
                    f.write(data)

                # Lê o CSV e adiciona ao DataFrame
                df = pd.read_csv(caminho_arquivo_csv, encoding='latin-1')
                DATASETS.append(df)

                for dataset in DATASETS:
                    dataset['forca[kN]'] = dataset['forca[N]'] / 1000
                    dataset.reset_index(drop=True)

                for arquivo_info in ARQUIVOS:
                    nome_do_arquivo = arquivo_info['nome']
                    # Now you can work with the "nome_do_arquivo" value


        #----------------Plota os graficos referente ----------------------------#

        if ARQUIVOS:


            for i in range(len(DATASETS)):
                fig, ax = plt.subplots(figsize=(16, 6))

                # plt.suptitle('Ensaio de Tração')
                plt.title('Carga x Deslocamento', fontsize=10)
                plt.grid(linestyle='--')

                plt.xlabel('Deslocamento [mm]')
                plt.ylabel('Força [kN]')

                x = DATASETS[i]['deformacao[mm]'].tolist()
                y = DATASETS[i]['forca[N]'].tolist()

                artist = ax.plot(x, y, label='Amostra ' + str(i + 1))
                CURVAS.append(artist)

                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))

                ax.set_ylim(bottom=0)
                ax.set_xlim(left=0)

                st.pyplot()

            # --------------- Carga x Deformaçao ( JUNTAS ) ---

            fig, ax = plt.subplots(figsize=(16, 6))

            # plt.suptitle('Ensaio de Tração')
            plt.title('Carga x Deslocamento', fontsize=10)
            plt.grid(linestyle='--')

            plt.xlabel('Deslocamento [mm]')
            plt.ylabel('Força [kN]')

            for i in range(len(DATASETS)):
                 x = DATASETS[i]['deformacao[mm]'].tolist()
                y = DATASETS[i]['forca[N]'].tolist()

                artist = ax.plot(x, y, label='Amostra ' + str(i + 1))
                CURVAS.append(artist)

            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))

            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)

            st.pyplot()

            # --------------- Tensao  x Deformaçao ( SEPARADAS ) ------------------------------

            # --------------- Tensao  x Deformaçao ( SEPARADAS ) ------------------------------

            for i in range(len(DATASETS)):
                tensao_mpa = DATASETS[i]['forca[N]'] / float(AREA[i])
                deformacao = 100 * (DATASETS[i]['deformacao[mm]'] / float(COMPRIMENTO[i]))

                DATASETS[i]['tensao[MPa]'] = tensao_mpa
                DATASETS[i]['deformacao[%]'] = deformacao

            for i in range(len(DATASETS)):
                fig, ax = plt.subplots(figsize=(16, 6))
                # plt.suptitle('Ensaio de Tração')
                plt.title('Tensão x Deformação', fontsize=10)
                plt.grid(linestyle='--')

                plt.xlabel('Deformação [%]')
                plt.ylabel('Tensão [MPa]')
                x = DATASETS[i]['deformacao[%]']
                y = DATASETS[i]['tensao[MPa]']

                artist = ax.plot(x, y, label='Amostra ' + str(i + 1))
                CURVAS.append(artist)
                # plt.yticks(range(0, 600, 60))
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))

                ax.set_ylim(bottom=0)
                ax.set_xlim(left=0)

                st.pyplot()
            # --------------- Tensao  x Deformaçao ( JUNTAS ) ------------------------------

            fig, ax = plt.subplots(figsize=(16, 6))
            # plt.suptitle('Ensaio de Tração')
            plt.title('Tensão x Deformação', fontsize=10)
            plt.grid(linestyle='--')

            plt.xlabel('Deformação [%]')
            plt.ylabel('Tensão [MPa]')

            for i in range(len(DATASETS)):
                x = DATASETS[i]['deformacao[%]']
                y = DATASETS[i]['tensao[MPa]']

                artist = ax.plot(x, y, label= nome_do_arquivo.split('-')[1])
                CURVAS.append(artist)

            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))

            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)

            st.pyplot()

    elif opcao == "Configurações":
        st.header("Configurações")
        # Adicione aqui as configurações e opções do usuário, se necessário.


if __name__ == "__main__":

    main()
