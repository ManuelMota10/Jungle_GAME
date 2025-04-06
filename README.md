# Jungle Game (Dou Shou Qi)

Implementação do jogo de tabuleiro chinês Jungle Game (Dou Shou Qi) com algoritmos de IA para o curso 
de Elementos de Inteligência Artificial e Ciência de Dados.

## Descrição

O Jungle Game é um jogo de tabuleiro estratégico para dois jogadores, onde cada jogador controla 
8 animais com diferentes poderes e valores. O objetivo é capturar a "toca" do oponente ou capturar 
todos os seus animais.

## Instalação

```bash
pip install -r requirements.txt

## Explicação

### Main

#### Overview
`main.py` implements the graphical user interface and game loop for a digital version of Jungle Chess (also known as Dou Shou Qi or Animal Chess), a traditional Chinese board game.

#### Key Components

##### Constants and Configuration
- Screen dimensions and layout settings
- Colour definitions
- Game state constants (MAIN_MENU, PLAYER_SELECTION, GAME)
- Font initialization

##### Classes
1. **JungleAnimals**: Represents animal pieces on the board
   - Properties: color, type, image
   - Methods to handle piece-specific behavior

2. **Button**: Creates interactive UI buttons
   - Properties: position, size, text, colors
   - Methods for drawing, updating, and checking clicks

##### Game Screens
The game has three main screens:
1. **Main Menu**: Simple title screen with a play button
2. **Player Selection**: Interface to choose player types (human or AI) for both sides
3. **Game Screen**: The actual game board where gameplay happens

##### Game Initialization
- `init_board()`: Sets up the initial board state with all animal pieces in their starting positions
- Configuration of player types (human, random AI, negamax AI, or alpha-beta AI)

##### Drawing Functions
- `draw_main_menu()`: Renders the title screen
- `draw_player_selection()`: Displays player type options
- `draw_game_screen()`: Renders the game board, pieces, and UI elements
- `draw_game_over_message()`: Shows winner announcement when game ends

##### Game Logic
- `handle_game_click()`: Processes player moves based on mouse clicks
- `ai_turn()`: Handles AI decision making and moves
- `update_menu_buttons()`: Updates button states based on mouse position

##### Main Game Loop
- Handles event processing (clicks, quits)
- Updates game state
- Draws the appropriate screen
- Manages timing and frame rate

#### Flow Control
The game transitions between screens based on user input and maintains the game state throughout. The main loop continuously checks for user input, updates the game state, and refreshes the display.

#### Integration with Other Files
- Uses AI player implementations from `aiPlayer.py`
- Leverages game rules and utility functions from `utils.py`
