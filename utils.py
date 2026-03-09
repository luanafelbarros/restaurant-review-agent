from typing import Dict, List
import math

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    """Esta função recebe o nome de um restaurante e retorna as avaliações desse restaurante.
    A saída deve ser um dicionário, onde a chave é o nome do restaurante e o valor é uma lista de avaliações desse restaurante.
    O "agente de busca de dados" deve ter acesso à assinatura desta função e deve ser capaz de sugeri-la como uma chamada de função.
    Exemplo:
    > fetch_restaurant_data("Estação Barão")
    {"Estação Barão's": ["A comida do Estação Barão foi mediana, sem nada particularmente marcante.", ...]}"""

    file_path = "./restaurantes.txt"
    search_string = f"{restaurant_name}"
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if search_string in line:
                    start_index = line.find(search_string) + len(search_string+". ")
                    end_index = line.find('\n')
                    if end_index == -1:
                        end_index = len(line)
                    return {restaurant_name: line[start_index:end_index].strip().split('. ')}
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    

def calculate_overall_score(restaurant_name: str,
                            food_scores: List[int],
                            customer_service_scores: List[int]) -> Dict[str, float]:
    """Esta função recebe o nome de um restaurante, uma lista de notas da comida (de 1 a 5) e uma lista de notas do atendimento ao cliente (de 1 a 5).
    A saída deve ser uma pontuação entre 0 e 10, calculada da seguinte forma:
    SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    A fórmula acima é uma média geométrica das notas, que penaliza mais a qualidade da comida do que o atendimento ao cliente.
    Exemplo:
    > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    {"Applebee's": 5.048}"""

    if len(food_scores) != len(customer_service_scores):
        raise ValueError("As listas de notas da comida e do atendimento ao cliente devem ter o mesmo tamanho")

    n = len(food_scores)

    sum_scores = sum(math.sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(n * math.sqrt(125))* 10 for i in range(n))
    return {restaurant_name: round(sum_scores, 3)}