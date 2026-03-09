# Trabalho 3 da disciplina de SISTEMAS INTELIGENTES E TÉCNICAS AVANÇADAS EM IA
<!-- ABOUT THE PROJECT -->
## Sobre o projeto:

Esse projeto contém o trabalho final da disciplina INF0084 - SISTEMAS INTELIGENTES E TÉCNICAS AVANÇADAS EM IA.
Ele conta com os seguintes arquivos:

*   `utils.py` - Arquivo onde são definidas as funções auxiliares para a execussão do trabalho (calculate_overall_score e fetch_restaurant_data).
*   `main.py` - Solução principal do trabalho, na qual é utilizado um parâmetro nos Agentes para limitar a conversa sequencial, mantendo apenas os turnos necessários.
*   `mainv2.py` - Solução alternativa do trabalho, na qual um turno extra de chamada de LLM é utilizado em cada conversação, sendo feito o seu tratamento através do prompt de sistema dos Agentes.
*   `restaurantes.txt` - Arquivo contendo as avaliações dos restaurantes.
*   `teste.py` - Arquivo que avalia a solução proposta no arquivo main.py.
*   `testev2.py` - Arquivo que avalia a solução alternativa proposta no arquivo mainv2.py.

<!-- USAGE EXAMPLES -->
## Utilização:

Primeiramente, para que o projeto possa ser executado, é necessária a criação de um arquivo .env com a chave da API do groc. Caso outra LLM seja utilizada, é necessário fazer os ajustes correspondentes nos arquivos main.py e mainv2.py

Por fim, apenas execute o arquivo teste.py e testev2.py para observar os resultados:
  
   ```sh
  python teste.py
   ```

<!-- CONTACT -->
## Alunos:

Daniel Ambrósio Ferreira Júnior - [danielambrosiojunior@gmail.com](danielambrosiojunior@gmail.com)

Luana Felipe de Barros - [luanafelbarros@gmail.com](luanafelbarros@gmail.com)




