#config.py
#Arquivo de Configurações do simulador

#Tudo no SI

#Pasta dos Resultados
PATH_RESULTADOS = 'Results'

################# Foguete ##################

#Configurações do Foguete/Paraquedas
MASSA = 5 
APOGEU = 20650 
ALTURA_ABERTURA_DROGUE = 10000 
ALTURA_ABERTURA_REEFING = 1000 
ALTURA_ABERTURA_MAIN = 500 

#Parâmetros para calcular arrasto
AREA_DROGUE = 0.3
CD_DROGUE = 0.75
AREA_REEFING = 1
CD_REEFING = 0.75
AREA_MAIN = 3
CD_MAIN = 0.75
AREA_BASE_FOGUETE = 0.1
CD_FOGUETE = 0.5


################## Simulador ####################

#Gravidade
ACELERACAO_GRAVITACIONAL = 9.8

#Vento
VELOCIDADE_VENTO_HORIZONTAL = 13/3.6
VELOCIDADE_VENTO_VERTICAL = 0

#Parâmetros para cálculos de densidade do ar
CONSTANTE_UNIVERSAL_GASES = 8.3144598       # Constante universal dos gases [J/(mol·K)]
MASSA_MOLAR_AR = 0.0289644                  # Massa molar do ar [kg/mol]
GRADIENTE_TERMICO_TROPOSFERICO = -0.0065    # Gradiente térmico troposférico [K/m]
GRADIENTE_TERMICO_ESTRATOSFERICO = 0.001    # Gradiente térmico estratosférico [K/m]
TEMPERATURA_SOLO = 295.15                   # Temperatura no solo (y = 0) [K]                           (NÃO É NO NÍVEL DO MAR !!!)
PRESSAO_SOLO = 92000                        # Pressão no solo (y = 0) [Pa]                               (NÃO É NO NÍVEL DO MAR !!!)
ALTURA_SOLO = 856                           # Altitude do solo (y = 0) em relação ao nível do mar       (É NO NÍVEL DO MAR !!!)
     