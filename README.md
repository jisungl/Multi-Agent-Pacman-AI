# Multi-Agent Pacman AI
Implementation of agents for Pacman and ghosts

**Note:** This project was part of the coursework for CSE 473 at the University of Washington.
The majority of the framework was provided by the instructors. My contributions were in:
- multiAgents.py

## Overview
The game environment simulates a Pacman Game here Pacman attempts to maximize its score. The implemented agents make decisions based on current and future states of the game using search strategies.

### Implemented Agents:
**ReflexAgent**
- Evaluates each possible move in each current state using an evaluation function
- Balances distance to nearest food and ghost avoidance
- Computes heuristic score using Manhattan Distances

**MinimaxAgent**
- Implements a minimax algorithm for search with Pacman and multiple ghosts
- Recursively simulates moves for Pacman and ghosts to a fixed depth
- Returns move that maximizes Pacman's outcome

**AlphaBetaAgent**
- Improves minimax by skipping steps that don't influence the final decision

**Expectimax**
- Assumes ghosts move randomly, as opposed to optimally
- Returns actions that maximize expected values

**betterEvaluationFunction**
- A heuristic that aims to reward states closer to food, penalize states with uneaten food, and encourage seeking food without getting too close to ghosts

## Run commands:
**Reflex Agent**
python autograder.py -q q1

**Minimax Agent**
python autograder.py -q q2

**Alpha-beta Agent**
python autograder.py -q q3

**Expectimax Agent**
python autograder.py -q q4
