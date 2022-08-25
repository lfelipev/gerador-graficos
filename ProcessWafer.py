import pandas as pd
import numpy as np
import os
from PIL import Image
import webcolors
import time
from collections import Counter
import xml.etree.cElementTree as ET
from lxml import etree
from datetime import datetime
from textwrap import wrap
from pathlib import Path
import mysql.connector

class ProcessWafer:
    def __init__(self, path) -> None:
        self.colors_dict = {'PASS': 'green', 'SKIPDIE':'red', 'REF':'black', 'FAIL':'yellow', 'OUTSIDE':'gray','UGLYDIE':'brown','EDGEDIE':'orange','FIRST_FAIL':'purple'}
        self.path = path

    ### Converte cada caracter de uma string em um elemento de uma lista
    ## Parâmetros
    # string -> uma string a ser convertida
    ## Retorno
    # Uma lista contendo
    def convert(self, string):
        default_list = []
        default_list[:0] = string

        return default_list

    ### Percorre o arquivo xml/map e extrai suas informações
    ## Retorno
    # image_vector -> um array multidimensional contendo a representação do wafer map por meio de caracteres
    # variables_list -> um vetor contendo as informações básicas do wafer em análise
    # bin_code_dict -> um dicionário com o mapeamento dos caracteres no arquivo xml/map
    def parse_xml(self):
        parser = etree.XMLParser(recover=True)
        mytree = ET.parse(self.path, parser=parser)
        myroot = mytree.getroot()
        header = myroot[0]
        tag_dict = {k.tag: v for v, k in enumerate(header)}
        bin_code_dict = {name:value for name, value in header[tag_dict['BIN_CODE']].attrib.items()}
        bin_code_dict['PASS'] = '1'

        WAFER_OCR_ID = header[tag_dict['WAFER_OCR_ID']]
        try:
            WAFER_UNITS = header[tag_dict['WAFER_UNITS']]
        except: 
            WAFER_UNITS = 'UNDEFINED'
        try:
            WAFER_SIZE = header[tag_dict['WAFER_SIZE']]
        except:
            WAFER_SIZE = 'UNDEFINED'
        try:
            XSTEP = header[tag_dict['XSTEP']]
            YSTEP = header[tag_dict['YSTEP']]
        except:
            XSTEP = 'UNDEFINED'
            YSTEP = 'UNDEFINED'
        ROW_COUNT = header[tag_dict['ROW_COUNT']]
        COLUMN_COUNT = header[tag_dict['COLUMN_COUNT']]
        FLAT_LOCATION = header[tag_dict['FLAT_LOCATION']]
        FLAT_TYPE = header[tag_dict['FLAT_TYPE']]
        BIN_COUNT_PASS = header[tag_dict['BIN_COUNT_PASS']]
        
        variables_list = [WAFER_OCR_ID, WAFER_UNITS, WAFER_SIZE, XSTEP, YSTEP, ROW_COUNT, COLUMN_COUNT, FLAT_LOCATION, FLAT_TYPE, BIN_COUNT_PASS]
        wafer = myroot[1].text
        wafer2 = wrap(wafer,int(COLUMN_COUNT.text))
        wafer_split = list(map(self.convert,wafer2))
        image_vector = np.array(wafer_split)
        counter = Counter(wafer)    

        self.generate_csv(counter, variables_list, bin_code_dict)
        
        return image_vector, variables_list, bin_code_dict

    ### Cria a imagem final do wafer a partir das informações do xml/map
    ## Parâmetros
    # image_vector -> um array multidimensional contendo a representação do wafer map por meio de caracteres
    # bin_code_dict -> um dicionário com o mapeamento dos caracteres no arquivo xml/map
    # variables_list -> um vetor contendo as informações básicas do wafer em análise
    ## Retorno
    # Uma imagem png salva no caminho contido na classe ProcessWafer
    def create_color_matrix(self, image_vector, bin_code_dict, variables_list):
        wafer_map = image_vector[...,np.newaxis]

        bin_code_dict_keys = bin_code_dict.keys()
        bin_code_dict_keys = [key for key in bin_code_dict_keys if key in self.colors_dict]

        conditions = [wafer_map == bin_code_dict[key] for key in bin_code_dict_keys]
        outputs = [np.array(webcolors.name_to_rgb(self.colors_dict[key])) for key in bin_code_dict_keys] 

        wafer_map = np.select(conditions,outputs)

        wafer_map = wafer_map.astype(np.uint8)
        img = Image.fromarray(wafer_map,'RGB')
        img.save(os.path.join(self.path + variables_list[0].text + '.png'))

    ### Cria uma imagem para simular o uso do wafer ao longo do tempo
    ## Parâmetros
    # image_vector -> um array multidimensional contendo a representação do wafer map por meio de caracteres
    # bin_code_dict -> um dicionário com o mapeamento dos caracteres no arquivo xml/map
    ## Retorno
    # Uma imagem png com o resultado da simulação salva no caminho contido na classe ProcessWafer
    def create_wafer_timeline(self, image_vector, bin_code_dict):
        wafer_map = image_vector[...,np.newaxis]
        wafer_map_test = np.copy(wafer_map)

        bin_code_dict_keys = bin_code_dict.keys()
        bin_code_dict_keys = [key for key in bin_code_dict_keys if key in self.colors_dict]

        conditions = [wafer_map == bin_code_dict[key] for key in bin_code_dict_keys]
        outputs = [np.array(webcolors.name_to_rgb(self.colors_dict[key])) for key in bin_code_dict_keys]

        wafer_map_test = np.select([(wafer_map_test == bin_code_dict['PASS']) & (np.random.rand(*wafer_map_test.shape) < 0.1)],  [bin_code_dict['SKIPDIE']],wafer_map_test)
        
        conditions2 = [wafer_map_test == bin_code_dict[key] for key in bin_code_dict_keys]

        wafer_map = np.select(conditions,outputs)
        wafer_map_test = np.select(conditions2,outputs)

        wafer_map_test = wafer_map_test.astype(np.uint8)
        img2 = Image.fromarray(wafer_map_test,'RGB')
        img2.save('wafer_test' + '.png')

    ### Obtém a quantidade de chips do tipo especificado
    ## Parâmetros
    # counter -> um dicionário com a contagem das informações do wafer
    # str -> string contendo o tipo do chip
    # bin_code_dict -> um dicionário com o mapeamento dos caracteres no arquivo xml/map
    ## Retorno
    # Um inteiro contendo a quantidade de chips daquele tipo presente no wafer map
    def get_wafer_atribute(self, counter, str, bin_code_dict):
        try:
            return counter[bin_code_dict[str]]
        except:
           return 'NaN'
    ### Remove os espaços extras do conteúdo de cada atributo do xml
    ## Parâmetros
    # atribute -> uma tag de um elemento do xml
    ## Retorno
    # O texto da tag sem espaços extras
    def get_wafer_text(self, atribute):
        try:
            return atribute.text.strip(' ')
        except AttributeError:
            return 'NaN'

    ### Gera o csv pronto para algum banco de dados
    ## Parâmetros
    # counter -> um dicionário com a contagem das informações do wafer
    # variables_list -> um vetor contendo as informações básicas do wafer em análise
    # bin_code_dict -> um dicionário com o mapeamento dos caracteres no arquivo xml/map
    ## Retorno
    # Um csv para a tabela DIM contendo as informações básicas do wafer em análise
    # Um csv para a tabela FATO contendo as informações atuais do wafer em análise
    def generate_csv(self, counter, variables_list, bin_code_dict):
        PASS = self.get_wafer_atribute(counter, 'PASS', bin_code_dict)
        FAIL = self.get_wafer_atribute(counter, 'FAIL', bin_code_dict)
        OUTSIDE = self.get_wafer_atribute(counter, 'OUTSIDE', bin_code_dict)
        SKIPDIE =  self.get_wafer_atribute(counter, 'SKIPDIE', bin_code_dict)
        PICKED = self.get_wafer_atribute(counter, 'PICKED', bin_code_dict)

        variables = []
        for x in variables_list:
            variables.append(self.get_wafer_text(x))
        
        variables_list = variables

        WAFER_OCR_ID = variables_list[0]
        WAFER_UNITS = variables_list[1]
        WAFER_SIZE = variables_list[2]
        XSTEP = variables_list[3]
        YSTEP = variables_list[4]
        ROW_COUNT = variables_list[5]
        COLUMN_COUNT = variables_list[6]
        FLAT_LOCATION = variables_list[7]
        FLAT_TYPE = variables_list[8]
        BIN_COUNT_PASS = variables_list[9]

        data_list = [WAFER_OCR_ID, WAFER_UNITS, WAFER_SIZE, XSTEP, YSTEP, ROW_COUNT, COLUMN_COUNT, FLAT_LOCATION, FLAT_TYPE, BIN_COUNT_PASS]
        
        # Tabela DIM
        data_dim = [{'WAFER_OCR_ID': WAFER_OCR_ID,
                'WAFER_UNITS': WAFER_UNITS,
                'WAFER_SIZE': WAFER_SIZE,
                'XSTEP': XSTEP,
                'YSTEP': YSTEP,
                'ROW_COUNT': ROW_COUNT,
                'COLUMN_COUNT': COLUMN_COUNT,
                'FLAT_LOCATION': FLAT_LOCATION,
                'FLAT_TYPE': FLAT_TYPE,
                'BIN_COUNT_PASS': BIN_COUNT_PASS,
                'CREATION_DATA': datetime.now()}]

        df_dim = pd.DataFrame(data_dim)
        df_dim.to_csv('tables/'+WAFER_OCR_ID+'_DIM.csv', index=False)

        print('\nDados - Tabela Dim')
        print(df_dim.head())

        wafermaps_db = mysql.connector.connect(
            host='mysql_db',
            user='user',
            password='password',
            database='wafer-maps'
        )

        cursor = wafermaps_db.cursor()

        query_dim = f"""INSERT IGNORE INTO dim_wafermap
                            (WAFER_OCR_ID,
                            WAFER_UNITS,
                            WAFER_SIZE,
                            XSTEP,
                            YSTEP,
                            ROW_COUNT,
                            COLUMN_COUNT,
                            FLAT_LOCATION,
                            FLAT_TYPE,
                            BIN_COUNT_PASS,
                            CREATION_DATA)

                            VALUES
                            ('{WAFER_OCR_ID}',
                            '{WAFER_UNITS}',
                            {WAFER_SIZE},
                            {XSTEP},
                            {YSTEP},
                            {ROW_COUNT},
                            {COLUMN_COUNT},
                            {FLAT_LOCATION},
                            '{FLAT_TYPE}',
                            {BIN_COUNT_PASS},
                            now())"""

        cursor.execute(query_dim)
                            
        wafermaps_db.commit()

        print(cursor.rowcount, "Dados inseridos no banco.")
        
        # Tabela FATO
        data_fato = [{'WAFER_OCR_ID': WAFER_OCR_ID,
                    'PASS': PASS,
                    'FAIL': FAIL,
                    'OUTSIDE': OUTSIDE,
                    'SKIPDIE': SKIPDIE,
                    'PICKED': PICKED,
                    'CREATION_DATA': datetime.now()}]

        df_fato = pd.DataFrame(data_fato)
        df_fato.to_csv('tables/'+WAFER_OCR_ID+'_FATO.csv', index=False)
        
        print('\nDados - Tabela Fato')
        print(df_fato.head())

        query_fato = f"""INSERT INTO fato_wafermap
                            (WAFER_OCR_ID,
                            PASS,
                            FAIL,
                            OUTSIDE,
                            SKIPDIE,
                            PICKED,
                            CREATION_DATA)

                            VALUES
                            ('{WAFER_OCR_ID}',
                            '{PASS}',
                            {FAIL},
                            {OUTSIDE},
                            {SKIPDIE},
                            {PICKED},
                            now())"""

        cursor.execute(query_fato)
                            
        wafermaps_db.commit()

        print(cursor.rowcount, "Dados inseridos no banco.")

###Função para executar o processamento do Wafer para apenas um arquivo
def run_single():
    wafer = ProcessWafer('AYF657-02-G7.map')
    image_vector, variables_list, bin_code_dict = wafer.parse_xml()
    wafer.create_color_matrix(image_vector,bin_code_dict,variables_list)

###Função para executar o processamento do Wafer para diversos arquivos
def run_all():
    start = time.perf_counter()

    rootPath = r'G:\Meu Drive\Beontag\beontag-machine-learning\wafer_maps_data\Wafer Maps_XML ADIVANIDE-20220530T191135Z-001'
    #rootPath = Path(__file__).resolve().parent
    
    for root, dirs, files in os.walk(rootPath):
        for filename in files:
            if filename.endswith(('.xml','.map')):
                try:
                    print(os.path.join(root, filename))
                    wafer = ProcessWafer(os.path.join(root, filename))
                    image_vector, variables_list, bin_code_dict = wafer.parse_xml()
                    wafer.create_color_matrix(image_vector,bin_code_dict,variables_list)
                except Exception as ex:
                    print('Erro no arquivo: {}'.format(os.path.join(root, filename)))
                    print(ex)
                    continue
    
    end = time.perf_counter()
    print('\nEllapsed time: ' + str(end-start))

def main(single=1):
    if single:
        run_single()
    else:
        run_all()

if __name__ == '__main__':
    main(1)