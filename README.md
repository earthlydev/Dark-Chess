# Dark Chess Engine (Python)  

A **Dark Chess** implementation in Python, developed for **CS 340: Data Structures**. This variant of chess hides the opponent's pieces (like fog-of-war), requiring probabilistic reasoning and adaptive strategies.  

## 🔍 Overview  
- **Dark Chess Rules**: Players only see their own pieces and squares attacked by their pieces. Captures reveal the opponent's piece.  
- **Project Focus**: Designed to explore **data structures** (e.g., graphs for move generation, trees for search) and **algorithms** (minimax with imperfect information).  

## ⚙️ Technical Details  
- **Core Libraries**: `python-chess` (move validation), `numpy` (board evaluation).  
- **Key Data Structures**:  
  - **Graphs**: Board represented as a graph for legal move traversal.  
  - **Search Trees**: Minimax/Alpha-Beta pruning for AI decision-making.  
  - **Bitboards**: Efficient board state storage (via `python-chess`).  
- **AI Logic**: Adapts traditional minimax to handle hidden information using probabilistic weighting.  

## 🚀 How to Run  
1. Clone the repo:  
   ```bash  
   git clone https://github.com/earthlydev/Dark-Chess  
   cd dark-chess
   ```
