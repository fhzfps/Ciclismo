from tcxparser.tcxparser import TCXParser
import pandas as pd
import numpy as np
import matplotlib as mpl
import seaborn
import plotly.express as px
class BikeAnalyze():
  """
  Define Ferramentas de Analise de treinos de ciclismo.
  Tipos de Arquivos Disponíveis:
  .tcx

  """
  def __init__(self,file,file_type,ftp=150):
    '''
    Limpa e extrai informações relevantes do arquivo para análise.
    Parâmetros:
    file= Diretório no qual está armazenado o arquivo.(str)
    file_type= Tipo do arquivo que se deseja analisar.(str)
    ftp= Functional Threshold Power do Ciclista. (float,int)
    '''
    def Zonas(watts):
      if watts<=0.55*self.ftp:
        return 1
      elif watts<=0.75*self.ftp:
        return 2
      elif watts<=0.9*self.ftp:
        return 3
      elif watts<=1.05*self.ftp:
        return 4
      elif watts<=1.2*self.ftp:
        return 5
      elif watts<=1.5*self.ftp:
        return 6
      else:
        return 7

    self.file=file
    self.file_type=file_type
    self.ftp=ftp
    if file_type=='.tcx':
      #Utilizando Biblioteca Disponibilizada no GitHub 'https://github.com/vkurup/python-tcxparser'
      self.data=TCXParser(file)
      self.distancia_t=self.data.distance
      self.tempo_t=self.data.duration
      self.calorias=self.data.calories
      tempos=pd.Series(self.data.time_objects())
      tempos_interval=pd.Series(self.data.time_durations())
      cadencias=pd.Series(self.data.cadence_values())
      distancias=pd.Series(self.data.distance_values())
      potencias=pd.Series(self.data.power_values())
      self.tabela=pd.DataFrame(data={'Tempo':tempos,'Intervalos':tempos_interval,
                                     'Cadencia':cadencias,'Distancia':distancias,
                                     'Potencia':potencias})
      self.tabela['Distancia']=self.tabela['Distancia'].apply(lambda x: float(x))
      self.tabela=self.tabela.dropna()
      self.tabela=self.tabela.set_index('Tempo')
      self.potencia_media=round(self.tabela['Potencia'].mean(),1)
      self.potencia_maxima=round(self.tabela['Potencia'].max(),1)
      self.potencia_minima=round(self.tabela['Potencia'].min(),1)
      self.cadencia_media=round(self.tabela['Cadencia'].mean(),1)
      self.cadencia_maxima=round(self.tabela['Cadencia'].max(),1)
      self.cadencia_minima=round(self.tabela['Cadencia'].min(),1)

      #Medindo Zonas para cada Ponto de Medida
      self.tabela['Zona']=self.tabela['Potencia'].apply(Zonas)
      #Porcentagem do Tempo Passado em Cada Zona
      self.zonas_pct={f'Z{i}':self.tabela[self.tabela['Zona']==i]['Intervalos'].sum().total_seconds()/self.tempo_t for i in range(1,8) if self.tabela[self.tabela['Zona']==i]['Intervalos'].sum().total_seconds()>0}

      #Calculando Potência Normalizada
      Windows=self.tabela['Potencia'].rolling(30)
      Power_30s=Windows.mean().dropna()
      PowerAvg=round(Power_30s.mean(),0)
      self.NP=round((((Power_30s**4).mean())**0.25),0)

      #Calculando Fator de Intensidade
      self.IF=self.NP/self.ftp

      #Calculando TTS
      self.TTS=(self.tempo_t*self.NP*self.IF)/(self.ftp*36)

    else:
      raise ValueError('Tipo de Arquivo Não Implementado')



  def grafico_potencia(self):
    '''
    Plota um gráfico de Potência por Tempo Decorrrido do Treino.
    '''
    fig = px.line(x=self.tabela.index, y=self.tabela['Potencia'])
    fig.update_layout(title='Gráfico de Potência',
                   xaxis_title='Tempo',
                   yaxis_title='Watts')

    return fig.to_html()

  def grafico_cadencia(self):
    '''
    Plota um gráfico de Cadência por Tempo Decorrrido do Treino.
    '''
    fig = px.line(x=self.tabela.index, y=self.tabela['Cadencia'])
    fig.update_layout(title='Gráfico de Cadência',
                   xaxis_title='Tempo',
                   yaxis_title='RPM')
    return fig.to_html()

  def grafico_zonas(self):
    '''
    Plota um gráfico de Pizza do tempo passado em cada Zona.
    '''
    colors = ['grey','blue','green','yellow','red','red','red']

    fig = px.pie(values=self.zonas_pct.values(),names=self.zonas_pct.keys(),title='Zonas De Intensidade',
                 labels=['Pct do Tempo'])
    fig.update_traces(textposition='inside', textinfo='percent+label',hoverinfo='label+percent',
                     marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    return fig.to_html()

  def gerar_relatorio(self):

    return {'ftp':self.ftp,'duracao_s':self.tempo_t,
            'NP':self.NP,'IF':self.IF,
            'PM':self.potencia_media,'TTS':self.TTS,
            'CM':self.cadencia_media,'PMax':self.potencia_maxima,'PMin':self.potencia_minima,
            'CMax':self.cadencia_maxima,'CMin':self.cadencia_minima,'Calorias':self.calorias,
            'Distancia':self.distancia_t,
            'GraficoPot':self.grafico_potencia(),
            'GraficoCad':self.grafico_cadencia(),
            'GraficoZonas':self.grafico_zonas()}
