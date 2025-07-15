# Simulador de Queda com Múltiplos Paraquedas

Este projeto simula numericamente a queda de um foguete equipado com um sistema de recuperação composto por três estágios de paraquedas (drogue, reefing e main). A simulação considera modelos físicos, incluindo arrasto dependente da altitude, densidade do ar variável, e influência do vento. Além disso, o projeto gera gráficos, animações e um relatório automático da simulação.

## Estrutura do Projeto

- `main.py`: Script principal que executa a simulação e gera o relatório.
- `solver.py`: Define o modelo físico e realiza a integração numérica da trajetória.
- `visualizer.py`: Responsável pela geração de gráficos e animações da simulação.
- `config.py`: Arquivo de configurações com os parâmetros físicos e ambientais.
- `requirements.txt`: Dependências necessárias para rodar o projeto.
- `Results/`: Diretório onde são salvos os resultados (gráficos, animações e relatório).

## Funcionalidades

- Modelo físico completo com:
  - Três estágios de paraquedas com altitudes de abertura distintas.
  - Cálculo da força de arrasto com densidade variável do ar.
  - Efeitos de vento horizontal e vertical.
- Solução numérica robusta usando métodos para equações rígidas (`Radau`).
- Visualização da simulação:
  - Gráficos de trajetória, altitude, velocidade, componentes e velocidade escalar.
  - Animação da trajetória (ainda não funciona).
- Geração automática de relatório Markdown com imagens e resultados da simulação.

## Como Usar

1. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

2. **Execute o script principal**:

```bash
python main.py
```

3. **Verifique os resultados** no diretório `Results/`, incluindo:

   - `relatorio.md`: Relatório da simulação com imagens e estatísticas.
   - `trajetoria.png`, `altitude_velocidade.png`, etc.: Gráficos gerados.
   - (Opcional) `animacao_trajetoria.gif`: Animação da trajetória.

## 📊 Exemplos de Saída

![Exemplo de Gráfico de Trajetória](Results/trajetoria.png)

## ⚙️ Personalização

Você pode alterar os parâmetros do foguete, dos paraquedas e do ambiente editando diretamente o arquivo `config.py`.
---

**Desenvolvido para fins de simulação física e visualização de sistemas de recuperação de foguetes.**
