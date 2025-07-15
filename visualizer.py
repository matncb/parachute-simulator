# visualizer.py

#Visualizar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Estilo
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

#Salvar
import os
import pathlib
from config import PATH_RESULTADOS

class Visualizer:
    def __init__(self):
        # Variáveis a serem usadas
        self.solver = None
        self.sol = None
        self.fig = None
        self.ax = None
        self.results_dir = PATH_RESULTADOS
        
    def _save_figure(self, filename):
        # Salvar figura no diretório
        os.makedirs(self.results_dir, exist_ok=True)
        path = os.path.join(self.results_dir, filename)
        plt.savefig(path)
        plt.close()
        return path
        
    def load_solution(self, solver):
        # Carregar solução
        self.solver = solver
        self.sol = solver.sol

        # S = [y, y_dot, x, x_dot] --> Pra lembrar
        
    def plot_trajectory(self, save=False):
        # Plot da trajetória y(x)

        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
            
        plt.figure(figsize=(10, 6))
        plt.plot(self.sol.y[2], self.sol.y[0])
        plt.title('Trajetória do Paraquedas')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        
        # Marcar abertura de cada paraquedas
        if self.solver.yd < self.solver.ap:
            plt.axhline(y=self.solver.yd, color='r', linestyle='--', label='Abertura Drogue')
        if self.solver.yr < self.solver.ap:
            plt.axhline(y=self.solver.yr, color='g', linestyle='--', label='Abertura Reefing')
        if self.solver.ym < self.solver.ap:
            plt.axhline(y=self.solver.ym, color='b', linestyle='--', label='Abertura Main')
        
        plt.legend()
        
        if save:
            return self._save_figure("trajetoria.png")
        else:
            return plt.gcf()

    def plot_y_y_dot(self, save=False):
        # Plot da altitude (y) e velocidade (y_dot)

        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
            
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Altitude (eixo esquerdo)
        color = 'tab:blue'
        ax1.set_xlabel('t (s)')
        ax1.set_ylabel('y (m)', color=color)
        ax1.plot(self.sol.t, self.sol.y[0], color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)
        
        # Velocidade vertical (eixo direito)
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel(r'$\dot{y}$ (m/s)', color=color)
        ax2.plot(self.sol.t, self.sol.y[1], color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Altitude e Velocidade Vertical')
        fig.tight_layout()
        
        if save:
            return self._save_figure("altitude_velocidade.png")
        else:
            return fig

    def plot_velocity_components(self, save=False):
        # Plot da velocidade horizontal e vertical

        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
            
        plt.figure(figsize=(10, 6))
        plt.plot(self.sol.t, self.sol.y[1], label=r'$\dot{y}$ (m/s)')
        plt.plot(self.sol.t, self.sol.y[3], label=r'$\dot{x}$ (m/s)')
        plt.title('Componentes de Velocidade')
        plt.xlabel('t (s)')
        plt.ylabel('Velocidade (m/s)')
        plt.legend()
        plt.grid(True)
        
        if save:
            return self._save_figure("componentes_velocidade.png")
        else:
            return plt.gcf()

    def plot_speed(self, save=False):
        # Plot da normal da velocidade

        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
            
        speed = np.sqrt(self.sol.y[1]**2 + self.sol.y[3]**2)
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.sol.t, speed)
        plt.title('Velocidade Escalar')
        plt.xlabel('t (s)')
        plt.ylabel('Velocidade (m/s)')
        plt.grid(True)
        
        if save:
            return self._save_figure("velocidade_escalar.png")
        else:
            return plt.gcf()

    def animate_trajectory(self, interval=50, save = False):
        #Cria uma animação da trajetória do paraquedas.
        #interval (int): Intervalo entre frames em milissegundos
        
        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
            
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlim(min(self.sol.y[2]), max(self.sol.y[2]) + 1)
        self.ax.set_ylim(0, max(self.sol.y[0]) + 100)
        self.ax.set_xlabel('Posição Horizontal (m)')
        self.ax.set_ylabel('Altitude (m)')
        self.ax.set_title('Trajetória do Paraquedas')
        self.ax.grid(True)
        
        # Linha completa da trajetória
        line, = self.ax.plot([], [], 'b-', alpha=0.5)
        # Ponto atual da simulação
        point, = self.ax.plot([], [], 'ro')
        # Texto com informações
        time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)
        info_text = self.ax.text(0.02, 0.90, '', transform=self.ax.transAxes)
        
        # Marca abertura de cada paraquedas
        if self.solver.yd < self.solver.ap:
            self.ax.axhline(y=self.solver.yd, color='r', linestyle='--', alpha=0.5)
        if self.solver.yr < self.solver.ap:
            self.ax.axhline(y=self.solver.yr, color='g', linestyle='--', alpha=0.5)
        if self.solver.ym < self.solver.ap:
            self.ax.axhline(y=self.solver.ym, color='b', linestyle='--', alpha=0.5)
        
        def init():
            line.set_data([], [])
            point.set_data([], [])
            time_text.set_text('')
            info_text.set_text('')
            return line, point, time_text, info_text
        
        def update(frame):
            # Atualiza trajetória
            x_data = self.sol.y[2, :frame]
            y_data = self.sol.y[0, :frame]
            line.set_data(x_data, y_data)
            
            # Atualiza ponto atual
            point.set_data(self.sol.y[2, frame], self.sol.y[0, frame])
            
            # Atualiza informações
            time_text.set_text(f'Tempo: {self.sol.t[frame]:.2f}s')
            info = (f'Altitude: {self.sol.y[0, frame]:.2f}m\n'
                    f'Vel. Vertical: {self.sol.y[1, frame]:.2f}m/s\n'
                    f'Vel. Horizontal: {self.sol.y[3, frame]:.2f}m/s')
            info_text.set_text(info)
            
            return line, point, time_text, info_text
        
        ani = FuncAnimation(
            self.fig, 
            update, 
            frames=len(self.sol.t),
            init_func=init,
            blit=True,
            interval=interval
        )
        
        # Salva a animação
        if save:
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(self.results_dir), exist_ok=True)
            ani.save(self.results_dir, writer='pillow', fps=1000/interval)
            plt.close()
            return self.results_dir
        else:
            return ani

    def generate_report(self, report_path=None, generate_animation=False):
        #Gera um relatório markdown com resumo e links para as figuras

        if self.sol is None:
            raise ValueError("Solução não carregada. Use load_solution() primeiro.")
        
        # Cria diretório de resultados se não existir
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Define caminho padrão para o relatório
        if report_path is None:
            report_path = os.path.join(self.results_dir, "relatorio.md")
        
        # Define caminhos para os arquivos
        traj_path = os.path.join(self.results_dir, "trajetoria.png")
        alt_vel_path = os.path.join(self.results_dir, "altitude_velocidade.png")
        vel_comp_path = os.path.join(self.results_dir, "componentes_velocidade.png")
        speed_path = os.path.join(self.results_dir, "velocidade_escalar.png")
        anim_path = os.path.join(self.results_dir, "animacao_trajetoria.gif")
        
        # Calcula resultados
        t_total = self.sol.t[-1]
        speed = np.sqrt(self.sol.y[1]**2 + self.sol.y[3]**2)
        v_max = np.max(speed)
        x_final = self.sol.y[2, -1]
        y_max = np.max(self.sol.y[0])
        vx_final = self.sol.y[3, -1]
        vy_final = self.sol.y[1, -1]
        v_final = np.sqrt(vx_final**2 + vy_final**2)
        impact_angle = np.degrees(np.arctan2(vy_final, vx_final))
        
        # Coleta eventos (abertura de cada paraquedas)
        events = []
        if self.solver.yd < self.solver.ap:
            idx_yd = np.argmax(self.sol.y[0] <= self.solver.yd)
            t_yd = self.sol.t[idx_yd]
            vy_yd = self.sol.y[1, idx_yd]
            events.append(f"- Abertura Drogue: {t_yd:.2f}s (vy = {vy_yd:.2f} m/s)")
            
        if self.solver.yr < self.solver.ap:
            idx_yr = np.argmax(self.sol.y[0] <= self.solver.yr)
            t_yr = self.sol.t[idx_yr]
            vy_yr = self.sol.y[1, idx_yr]
            events.append(f"- Abertura Reefing: {t_yr:.2f}s (vy = {vy_yr:.2f} m/s)")
            
        if self.solver.ym < self.solver.ap:
            idx_ym = np.argmax(self.sol.y[0] <= self.solver.ym)
            t_ym = self.sol.t[idx_ym]
            vy_ym = self.sol.y[1, idx_ym]
            events.append(f"- Abertura Main: {t_ym:.2f}s (vy = {vy_ym:.2f} m/s)")
        
        # Gera conteúdo Markdown
        md_content = f"""
# Relatório da Simulação de Queda de Paraquedas

## Parâmetros da Simulação
- **Massa total**: {self.solver.m:.2f} kg
- **Apogeu inicial**: {self.solver.ap:.2f} m
- **Altura abertura drogue**: {self.solver.yd:.2f} m
- **Altura abertura reefing**: {self.solver.yr:.2f} m
- **Altura abertura main**: {self.solver.ym:.2f} m

## Resultados Principais
- **Tempo total de queda**: {t_total:.2f} s
- **Altitude máxima alcançada**: {y_max:.2f} m
- **Velocidade máxima**: {v_max:.2f} m/s
- **Deslocamento horizontal**: {x_final:.2f} m

### Velocidade de Impacto
- **Magnitude**: {v_final:.2f} m/s
- **Componente vertical**: {vy_final:.2f} m/s
- **Componente horizontal**: {vx_final:.2f} m/s
- **Direção**: {impact_angle:.1f}° da horizontal

## Eventos de Abertura
{os.linesep.join(events) if events else "Nenhum evento de abertura registrado"}

## Visualizações

### Trajetória Completa
![Trajetória do Paraquedas]({os.path.basename(traj_path)})

### Altitude e Velocidade Vertical
![Altitude e Velocidade Vertical]({os.path.basename(alt_vel_path)})

### Componentes de Velocidade
![Componentes de Velocidade]({os.path.basename(vel_comp_path)})

### Velocidade Escalar
![Velocidade Escalar]({os.path.basename(speed_path)})
"""
        
        # Adiciona animação ao relatório se for gerada
        if generate_animation:
            md_content += f"""

### Animação da Trajetória
![Animação da Trajetória]({os.path.basename(anim_path)})
"""
        
        # Salva o relatório
        with open(report_path, 'w') as f:
            f.write(md_content)
        
        # Gera as figuras
        self.plot_trajectory(save=True)
        self.plot_y_y_dot(save=True)
        self.plot_velocity_components(save=True)
        self.plot_speed(save=True)
        
        # Gera animação se solicitado (Beeeeem mais demorado)
        if generate_animation:
            self.animate_trajectory(save = True)
        
        return report_path