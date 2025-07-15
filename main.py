#main.py

from solver import Solver
from visualizer import Visualizer

if __name__ == "__main__":
   # Criar e resolver o modelo
    solver = Solver()
    solver.solve()

    # Carregar no visualizador e gerar relatório
    visualizer = Visualizer()
    visualizer.load_solution(solver)
    report_path = visualizer.generate_report()

    print(f"Relatório gerado em: {report_path}")