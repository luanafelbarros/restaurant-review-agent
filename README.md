# Assignment 3 for the Intelligent Systems and Advanced AI Techniques Course

<!-- ABOUT THE PROJECT -->
## About the project:

This project contains the final assignment for the course INF0084 - INTELLIGENT SYSTEMS AND ADVANCED AI TECHNIQUES.
It includes the following files:

*   `utils.py` - File where auxiliary functions for the assignment are defined (calculate_overall_score and fetch_restaurant_data).
*   `main.py` - Main solution for the assignment, which uses a parameter in the Agents to limit sequential conversation, keeping only the necessary turns.
*   `mainv2.py` - Alternative solution for the assignment, which uses an extra LLM call turn in each conversation, with its handling done through the system prompt of the Agents.
*   `restaurantes.txt` - File containing the restaurant reviews.
*   `teste.py` - File that evaluates the solution proposed in main.py.
*   `testev2.py` - File that evaluates the alternative solution proposed in mainv2.py.

<!-- USAGE EXAMPLES -->
## Usage:

First, to run the project, you need to create a .env file with the Groq API key. If another LLM is used, you need to make the corresponding adjustments in the main.py and mainv2.py files.

Finally, just run the teste.py and testev2.py files to observe the results:
  
   ```sh
  python teste.py
   ```

<!-- CONTACT -->
## Students:

Daniel Ambrósio Ferreira Júnior - [danielambrosiojunior@gmail.com](danielambrosiojunior@gmail.com)

Luana Felipe de Barros - [luanafelbarros@gmail.com](luanafelbarros@gmail.com)