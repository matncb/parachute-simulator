#solver.py

from config import * # Carrega configurações
import numpy as np
from scipy.integrate import solve_ivp # Integradores já compilados do Fortran

class Solver:
    def __init__(self):
        # Renomeando para nomes mais simples
        
        # Configurações do Foguete/Paraquedas
        self.m, self.ap, self.yd, self.yr, self.ym = (
            MASSA, 
            APOGEU, 
            ALTURA_ABERTURA_DROGUE,
            ALTURA_ABERTURA_REEFING,  
            ALTURA_ABERTURA_MAIN
        ) 

        # Parâmetros para calcular arrasto
        self.AD, self.cdD, self.AR, self.cdR, self.AM, self.cdM, self.AF, self.cdF = (
            AREA_DROGUE, 
            CD_DROGUE,
            AREA_REEFING,
            CD_REEFING,
            AREA_MAIN,
            CD_MAIN,
            AREA_BASE_FOGUETE,
            CD_FOGUETE
        )

        # Gravidade                  
        self.g =  ACELERACAO_GRAVITACIONAL

        # Vento
        self.vx, self.vy = (
            VELOCIDADE_VENTO_HORIZONTAL,
            VELOCIDADE_VENTO_VERTICAL
        )

        # Parâmetros para cálculos de densidade do ar
        self.R, self.M, self.L1, self.L2, self.T0, self.P0, self.h0 = (
            CONSTANTE_UNIVERSAL_GASES,
            MASSA_MOLAR_AR,
            GRADIENTE_TERMICO_TROPOSFERICO,
            GRADIENTE_TERMICO_ESTRATOSFERICO,
            TEMPERATURA_SOLO,
            PRESSAO_SOLO,
            ALTURA_SOLO
        )

    def rho(self,y):
        # Modelo para a densidade do ar em função da altitude
        # Não faço ideia do que tá acontendo aqui, segui o que foi feito no código antigo e fuçando na internet
        # Seria interessante olhar com mais cuidado
        
        h_abs = y + self.h0
        
        # 1. Camada troposférica (solo até 11 km de altitude absoluta)
        if h_abs <= 11000:
            T = self.T0 + self.L1 * y
            expoente = -self.g * self.M / (self.R * self.L1)
            P = self.P0 * (T / self.T0) ** expoente
        
        # 2. Baixa estratosfera (11-20 km de altitude absoluta)
        elif h_abs <= 20000:
            # Calcula condições no topo da troposfera
            y_trop = 11000 - self.h0
            T_trop = self.T0 + self.L1 * y_trop
            expoente = -self.g * self.M / (self.R * self.L1)
            P_trop = self.P0 * (T_trop / self.T0) ** expoente
            
            # Modelo estratosférico inferior (temperatura constante)
            T = T_trop
            P = P_trop * np.exp(-self.g * self.M * (h_abs - 11000) / (self.R * T_trop))
        
        # 3. Alta estratosfera (20-25 km de altitude absoluta)
        else:
            # Calcula condições no topo da troposfera
            y_trop = 11000 - self.h0
            T_trop = self.T0 + self.L1 * y_trop
            expoente = -self.g * self.M / (self.R * self.L1)
            P_trop = self.P0 * (T_trop / self.T0) ** expoente
            
            # Calcula condições a 20 km absoluto
            P_20k = P_trop * np.exp(-self.g * self.M * (20000 - 11000) / (self.R * T_trop))
            T_20k = T_trop
            
            # Aplica gradiente térmico estratosférico acima de 20 km
            T = T_20k + self.L2 * (h_abs - 20000)
            expoente_upper = -self.g * self.M / (self.R * self.L2)
            P = P_20k * (T / T_20k) ** expoente_upper
        
        # Cálculo da densidade
        return (P * self.M) / (self.R * T)
    
    def F_drag(self, S):
        # Modelo para a força de arrasto
        # Dependendo da forma que o paraquedas descer (reto, inclinado, etc) pode haver variações nos coefientes de arrasto para cada condição
        # Essas variações vão ser desprezadas e vamos considerar que o paraquedas está sempre alinhado com a velocidade
        # Efeitos como turbulência, torques sofridos, etc também são desprezados

        y, y_dot, x, x_dot = S # Recebe a matriz S

        # Caso a caso considerando o momento em que cada paraquedas está aberto

        ############### Se os paraquedas se sobrepõem ############
        k = 0 # k = cd * A

        if y > self.yd:
           cd = self.cdF
           A = self.AF
           k += cd*A  # Cd*A estimado para foguete --> Desconsiderando o foguete passaria da velocidade do som, o que seria absurdo
        
        if y <= self.yd:
            cd = self.cdD
            A  = self.AD
            k += cd*A

        if y <= self.yr:
            cd = self.cdR
            A = self.AR
            k += cd*A

        if y <= self.ym:
            cd = self.cdM
            A = self.AM
            k += cd*A

        ############### Se os paraquedas são substituídos ##############

        '''
        k = self.cdF * self.AF  # Arrasto base sempre presente

        if y <= self.yd:
            k = self.cdD * self.AD  # Drogue substitui foguete

        if y <= self.yr:
            k = self.cdR * self.AR  # Reefing substitui drogue

        if y <= self.ym:
            k = self.cdM * self.AM  # Main substitui reefing
        '''

        #######################################################

        # Calcula a desnsidade do ar
        rho_value = self.rho(y) 

        # Velocidades Relativas ao vento
        y_dot_rel = y_dot - self.vy
        x_dot_rel = x_dot - self.vx 

        # Modelo para a força de arrasto: F = (1/2)*rho*cd*A*v**2 \hat{v}
        Fx = -(1/2)* rho_value* k * (y_dot_rel**2 + x_dot_rel**2)**(1/2) * x_dot_rel
        Fy = -(1/2)* rho_value* k* (y_dot_rel**2 + x_dot_rel**2)**(1/2) * y_dot_rel

        return (Fx, Fy)

    def dSdt(self, S):
        # Modelo matemático em formato matricial
        # S = [y, y_dot, x, x_dot] --> matriz
        # dSdt = [y_dot, y_ddot, x_dot, x_ddot]
        # Precisamos escrever y_ddot e x_ddot em termos de um modelo físico
        
        y, y_dot, x, x_dot = S
        Fx, Fy = self.F_drag(S)

        y_ddot = -self.g + 1/self.m * Fy
        x_ddot = 1/self.m * Fx

        return [y_dot, y_ddot, x_dot, x_ddot]
    
    def solve(self, dt = 0.001, t_max = 1000, method = 'Radau', rtol = 1e-6, atol = 1e-8 ): 

        # O código original implementa RK45 (até quarta ordem); DOP853 vai até a oitava, mas requer mais poder computacional
        # Esses dois métodos funcionam até que bem mas geram algumas coisas bizarras
        # Como nesse modelo o paraquedas simplesmente aparace, geramos uma descontinuidade --> Equações rígidas
        # Usando o Radau os resultados parecem melhores

        #Obs: Trocar o método também resolve o problema de overflow que tinha no código anterior por algum motivo misterioso
        
        t_eval = np.arange(0, t_max, dt)

        func = lambda t,S: self.dSdt(S) 

        #Função para parar quando y = 0
        # S = [y, y_dot, x, x_dot] --> matriz
        
        ground_event = lambda t, S: S[0] # Retorna posição
        ground_event.terminal = True 
        ground_event.direction = -1 # Troca de sinal

        sol = solve_ivp(
            func,
            [0, t_max],
            [self.ap,0,0,0],
            method=method,
            events=ground_event,
            rtol=rtol,
            atol=atol
        )

        self.sol = sol
    

