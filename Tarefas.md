# Jungle_GAME
Projeto da cadeira de Elementos de Inteligência Artificial e Ciência de Dados
# Tarefas Detalhadas para Desenvolvimento do Jungle Game

Vou dividir o projeto em fases com tarefas bem específicas para você implementar de forma progressiva.

## FASE 1: Estrutura Base e Regras do Jogo

### Tarefa 1: Representação do Tabuleiro
1. Crie uma classe `Board` que represente o tabuleiro 7x9
2. Implemente uma matriz para representar o tabuleiro
3. Defina constantes para os diferentes tipos de casas:
   - Terreno normal (0)
   - Rio (1)
   - Armadilha do jogador 1 (2)
   - Armadilha do jogador 2 (3)
   - Toca do jogador 1 (4)
   - Toca do jogador 2 (5)
4. Implemente a função `initialize_board()` que configura o tabuleiro inicial

### Tarefa 2: Representação dos Animais
1. Crie uma classe `Animal` com os seguintes atributos:
   - Tipo (rato, gato, cão, etc.)
   - Força (valor de 1 a 8)
   - Jogador (1 ou 2)
   - Posição (linha, coluna)
   - Pode nadar (boolean)
   - Pode pular rio (boolean)
2. Crie subclasses para cada animal específico com suas habilidades:
   - `Rat` (rato): força 1, pode nadar
   - `Cat` (gato): força 2
   - `Dog` (cão): força 3
   - `Wolf` (lobo): força 4
   - `Leopard` (leopardo): força 5
   - `Tiger` (tigre): força 6, pode pular rio
   - `Lion` (leão): força 7, pode pular rio
   - `Elephant` (elefante): força 8

### Tarefa 3: Configuração Inicial do Jogo
1. Crie uma classe `Game` que gerencie o estado do jogo
2. Implemente um método `setup_game()` que posicione todos os animais no tabuleiro inicial
3. Crie uma função para verificar se o jogo acabou (cheque se um jogador ganhou)

### Tarefa 4: Implementação das Regras de Movimento
1. Implemente uma função `get_valid_moves(animal)` que retorne todos os movimentos possíveis para um animal
2. Implemente as regras específicas de movimento para cada tipo de animal:
   - Movimento básico (uma casa em qualquer direção ortogonal)
   - Regras para atravessar o rio (dependendo do animal)
   - Regras para captura (baseadas na força dos animais)
   - Regra especial: rato pode capturar elefante
3. Adicione restrições para entrar em tocas (só pode entrar na toca do oponente)
4. Adicione o efeito das armadilhas (animal perde sua força quando está na armadilha do oponente)

### Tarefa 5: Interface de Texto Básica
1. Crie uma função `print_board()` que mostre o estado atual do tabuleiro e peças
2. Implemente uma interface de texto simples para jogar (humano vs humano)
3. Permita que os jogadores selecionem peças e façam movimentos via entrada de texto

## FASE 2: Simplificações e Versões Reduzidas

### Tarefa 6: Criar uma Versão Simplificada do Jogo
1. Implemente uma versão com tabuleiro 5x7 ou 4x6
2. Reduza o número de animais (ex: 4 por jogador)
3. Mantenha as regras essenciais do jogo
4. Teste essa versão simplificada para garantir que funciona corretamente

## FASE 3: Algoritmos de IA Básicos

### Tarefa 7: Implementação do Minimax
1. Crie uma classe `MinimaxPlayer` que implementa o algoritmo Minimax básico
2. Implemente a função `minimax(state, depth, maximizing_player)`
3. Crie uma função de avaliação simples para o estado do jogo:
   - Conte os pontos por peças presentes (soma da força dos animais)
   - Adicione pontos por proximidade à toca do oponente
4. Limite a profundidade da busca para não sobrecarregar o processamento
5. Teste o algoritmo na versão simplificada do jogo

### Tarefa 8: Poda Alfa-Beta
1. Estenda seu algoritmo Minimax com poda alfa-beta
2. Crie uma função `minimax_alpha_beta(state, depth, alpha, beta, maximizing_player)`
3. Compare o desempenho com o Minimax básico (contagem de nós explorados)
4. Teste diferentes profundidades de busca

## FASE 4: Melhorias na IA e Interface

### Tarefa 9: Função de Avaliação Avançada
1. Crie uma função de avaliação mais sofisticada:
   - Material (soma ponderada da força das peças)
   - Posição (pontos por proximidade à toca do oponente)
   - Controle territorial (pontos por peças em posições estratégicas)
   - Mobilidade (pontos pelo número de movimentos disponíveis)
2. Teste diferentes pesos para cada fator da avaliação

### Tarefa 10: Níveis de Dificuldade
1. Implemente três níveis de dificuldade para a IA:
   - Fácil: profundidade baixa, função de avaliação simples, movimentos aleatórios ocasionais
   - Médio: profundidade média, função de avaliação completa
   - Difícil: profundidade maior, função de avaliação completa, ordenação de movimentos
2. Teste cada nível contra os outros e contra jogadores humanos

### Tarefa 11: Interface Gráfica Básica
1. Instale e importe uma biblioteca gráfica simples (como Pygame)
2. Crie sprites ou representações visuais para o tabuleiro e animais
3. Implemente a lógica para renderizar o tabuleiro na tela
4. Adicione interatividade para selecionar e mover peças com o mouse
5. Adicione indicadores visuais para movimentos válidos

## FASE 5: Avançada e Experimental

### Tarefa 12: Técnicas Avançadas do Minimax
1. Implemente ordenação de movimentos para melhorar a poda alfa-beta
2. Adicione memória para posições já analisadas (tabela de transposição)
3. Implemente a busca com aprofundamento iterativo

### Tarefa 13: Monte Carlo Tree Search (MCTS)
1. Implemente uma versão básica do algoritmo MCTS
2. Crie as funções de seleção, expansão, simulação e retropropagação
3. Compare o desempenho do MCTS com o Minimax com alfa-beta

### Tarefa 14: Análise e Comparação
1. Crie métricas para avaliar as diferentes IAs:
   - Taxa de vitória
   - Tempo médio por jogada
   - Número de nós explorados
   - Profundidade média atingida
2. Compare diferentes configurações e algoritmos
3. Documente os resultados em gráficos e tabelas

### Tarefa 15: Finalização e Documentação
1. Refatore o código para melhorar organização e legibilidade
2. Adicione comentários explicativos em todo o código
3. Crie um arquivo README detalhado explicando como executar e usar o programa
4. Prepare a apresentação final com os resultados da análise comparativa

## Dicas para Iniciar:

1. Comece pela Fase 1 e implemente o jogo básico funcional antes de avançar
2. Teste cada componente individualmente após implementação
3. Use a versão simplificada para implementar e testar os algoritmos de IA
4. Mantenha uma estrutura de código modular para facilitar testes e expansões
5. Use um sistema de controle de versão como Git para acompanhar o progresso e permitir retornar a versões anteriores se necessário
