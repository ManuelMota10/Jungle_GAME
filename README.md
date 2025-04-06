## Jungle Game (Dou Shou Qi)

Implementation of the Chinese board game Jungle Game (Dou Shou Qi), enhanced with AI algorithms, developed for the course Elements of Artificial Intelligence and Data Science.

## Description

Jungle Game is a strategic two-player board game where each player commands 8 animals, each with unique strengths and movement rules. The goal is to either capture the opponent’s den or eliminate all of their animals. This project features both the core mechanics of the game and intelligent agents capable of playing competitively.

## Instalation

```bash
pip install -r requirements.txt
```

## Explained

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

### AiPlayer

#### Overview
`aiPlayer.py` defines three classes of AI players with increasing levels of intelligence:
1. RandomPlayer (simplest)
2. NegamaxPlayer (intermediate)
3. AlphaBetaPlayer (most advanced)

Each class implements the `get_ai_move()` method, which analyzes the current board state and returns a move for the AI to make.

#### Key Components

##### RandomPlayer
A basic AI that simply chooses a random valid move from all possible moves.

- **Methods**:
  - `get_ai_move()`: Collects all valid moves for the current player and randomly selects one

##### NegamaxPlayer
Implements the Negamax algorithm, which is a variant of the Minimax algorithm for zero-sum games.

- **Methods**:
  - `get_ai_move()`: Entry point that evaluates all possible moves and selects the best one
  - `negamax()`: Recursive implementation of the Negamax algorithm
  - `get_all_valid_moves()`: Collects all valid moves for a player
  - `make_temp_move()`: Creates a temporary board state after a move by manually copying piece references to avoid issues with Pygame surfaces
  - `evaluate_board()`: Scores a board position based on piece values and positions
  - `get_player_score()`: Calculates a player's score on the board

##### AlphaBetaPlayer
The most sophisticated AI, implementing Alpha-Beta pruning (an optimization of the Minimax algorithm).

- **Methods**:
  - `get_ai_move()`: Main entry point, similar to NegamaxPlayer but using alpha-beta search
  - `alpha_beta()`: Recursive alpha-beta search algorithm
  - `hash_board()`: Creates a string representation of the board state for the transposition table
  - `get_all_valid_moves()`: Similar to NegamaxPlayer
  - `make_temp_move()`: Creates a new board with moved pieces using direct assignment of references rather than deep copying to avoid Pygame surface serialization issues
  - `evaluate_board()`, `get_player_score()`: Similar to NegamaxPlayer

##### Key Features

### AIPlayer (Base Class)
- Common functionality for all AI implementations
- Methods:
  - `get_all_valid_moves()`: Collects all valid moves for a player
  - `make_temp_move()`: Creates a temporary board state after a move
  - `evaluate_board()`: Scores a board position based on piece values, position, and den threats
  - `get_player_score()`: Calculates a player's score on the board, including special cases like rat vs elephant
  - `is_den_threat()`: Evaluates how close and threatening pieces are to opponent's den

### RandomPlayer
A basic AI that simply chooses a random valid move from all possible moves.
- **Methods**:
  - `get_ai_move()`: Collects all valid moves and randomly selects one

### NegamaxPlayer
Implements the Negamax algorithm, which is a variant of the Minimax algorithm for zero-sum games.
- **Methods**:
  - `get_ai_move()`: Entry point that evaluates moves with a specified depth parameter
  - `negamax()`: Recursive implementation of the Negamax algorithm

### AlphaBetaPlayer
The most sophisticated AI, implementing Alpha-Beta pruning with move ordering and memory optimizations.
- **Methods**:
  - `__init__()`: Initializes memory_box, killer_moves, and move_hist dictionaries
  - `get_ai_move()`: Uses iterative deepening to progressively search deeper
  - `order_moves()`: Prioritizes moves based on captures, history, and proximity to opponent's den
  - `alpha_beta()`: Recursive alpha-beta search algorithm with transposition table
  - `hash_board()`: Creates a string representation of the board state for the transposition table

### Key Features

1. **Search Depth**: Both NegamaxPlayer and AlphaBetaPlayer use a search depth parameter passed from main.py, with deeper searches for fewer pieces on board

2. **Board Evaluation**: Sophisticated heuristics considering:
   - Piece ranks and adjusted values
   - Proximity to the opponent's den
   - Special case handling (e.g., Rat value increases when opponent has Elephant)

3. **Alpha-Beta Optimizations**:
   - Transposition table (memory_box) to avoid re-evaluating positions
   - Killer move heuristic to remember effective non-capture moves
   - Move ordering based on captures, history, and den proximity
   - Iterative deepening to find good moves quickly at shallow depths

4. **Early Termination**: Alpha-Beta search can terminate early when finding a winning move

### Algorithm Details

- **Negamax**: A variation of minimax that uses the property that max(a,b) = -min(-a,-b) to simplify the implementation

- **Alpha-Beta Pruning**: An optimization technique that reduces the number of nodes evaluated in the search tree

- **Move Ordering**: Prioritizing likely good moves to improve pruning efficiency

#### Integration
The AI players use utility functions from `utils.py` to understand valid moves and implement game rules.

### utils

#### Overview
`utils.py` implements the rule set of Jungle Chess, including piece movement patterns, capturing rules, and victory conditions. It serves as the foundation of the game's logic without being tied to any specific UI or AI implementation.

#### Key Components

##### Game Constants
- **RED_TRAPS**, **GREEN_TRAPS**: Coordinates of trap squares for each player
- **RED_DEN**, **GREEN_DEN**: Coordinates of each player's den
- **WATER_CELLS**: Coordinates of river/water squares
- **ANIMAL_RANKS**: Dictionary mapping animal types to their power rankings
- **DIRECTIONS**: Common movement directions (up, down, left, right)

##### Helper Functions
- **get_rank()**: Returns the numerical rank of an animal type
- **get_adjusted_rank()**: Modifies a piece's rank based on special conditions (e.g., being in a trap)
- **is_water_cell()**: Checks if a position is in the river
- **is_valid_position()**: Determines if a move destination is valid (in bounds, not own den)

##### Movement Logic
The file implements specific movement rules for each animal type:

1. **regular_moves()**: Standard movement for most animals (Cat, Dog, Wolf, Leopard)
   - Can move one space orthogonally
   - Cannot enter water
   - Can capture lower or equal rank pieces

2. **rat_moves()**: Special movement for the Rat
   - Can enter water
   - Can capture elephants (special rule)
   - Can only capture when not in water

3. **elephant_moves()**: Special movement for the Elephant
   - Cannot enter water
   - Cannot capture Rats (special rule)

4. **jumping_moves()**: Special movement for Tiger and Lion
   - Can jump across river in straight lines
   - Cannot jump if a Rat is in the water between start and destination

##### Game State Evaluation
- **get_valid_moves()**: Master function that returns all valid moves for a specific piece
- **is_game_over()**: Checks win conditions:
  1. Den occupation (a player's piece enters the opponent's den)
  2. Elimination (all of one player's animals are captured)

#### Game Rules Implemented
1. **Piece Hierarchy**: Each animal has a rank, and can generally capture lower or equal rank pieces
2. **Special Cases**: 
   - Rat can capture Elephant despite being lowest rank
   - Elephant cannot capture Rat
3. **Trap Mechanics**: Any animal in an opponent's trap has its rank reduced to 0
4. **River Crossings**: Only Rat can swim, while Tiger and Lion can jump across
5. **Victory Conditions**: Enter opponent's den or eliminate all opponent's pieces

#### Integration
This file provides the rule foundation that both the main game loop and the AI decision-making rely on. It ensures game rules are applied consistently throughout the application.

## Resources

### GitHub Repositories

- [Jungle Chess Implementation](https://github.com/yoavamitai/Jungle-Chess/blob/minimax/MVC/minimax/minimax.py) - Minimax algorithm applied to Jungle Chess
- [Adversarial Search Library](https://github.com/leonardoazzi/adversarial-search/blob/master/advsearch/headkicker/minimax.py) - example adversarial search (minimax)
- [Custom Game Player](https://github.com/elinorwahl/adversarial-search-game-players/blob/master/my_custom_player.py) - example adversarial search (minimax)

### Other Resources

#### Video Tutorial
- [Chess Game Tutorial](https://www.youtube.com/watch?v=OpL0Gcfn4B4) - Adaption to Jungle Chess

#### Documentation & Articles
- [Intoduction to Pygame](https://pygame.readthedocs.io/en/latest/1_intro/intro.html) - Pygame basic tutorial
- [Pygame Documentation](https://www.pygame.org/docs/) - Pygame examples and uses
- [Negamax - Chess Programming Wiki](https://www.chessprogramming.org/Negamax) - Alternative formulation of minimax
- [Alpha-Beta Pruning - Chess Programming Wiki](https://www.chessprogramming.org/Alpha-Beta) - Optimization technique for minimax/negamax
- [Alpha-Beta Pruning - Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) - Comprehensive explanation with examples
