from typing import Dict, List
from autogen import ConversableAgent, AssistantAgent
import sys
import os
from utils import calculate_overall_score, fetch_restaurant_data
from dotenv import load_dotenv
from autogen import register_function

# Caminho para o arquivo .env
load_dotenv()

llm_config = {"config_list": [{"model": "llama3-70b-8192", "api_key": os.environ.get("GROQ_API_KEY"), "api_type": "groq"}]}

# Não modifique a assinatura da função "main".
def main(user_query: str):

    # Agente que indica a função a ser executada para obter dados
    data_fetch_agent = ConversableAgent(
        name="DataFetcher",
        system_message="You are a helpful AI assistant. "
        "You can help with retrieving restaurants reviews.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1, # Usada para impedir a última chamada de LLM (DataFetcher -> Executor), que não é necessária
    )

    # Agente que analisa as avaliações em linguagem natural e converte para numéricas
    review_analysis_agent = ConversableAgent(
        name="Review Analysis Agent",
        system_message="""Você é responsável por transformar avaliações de restaurantes em scores numéricos. Considere o seu padrão de conversão da seguinte forma:
    a. 1/5: horrível, nojento, terrível.
    b. 2/5: ruim, desagradável, ofensivo.
    c. 3/5: mediano, sem graça, irrelevante.
    d. 4/5: bom, agradável, satisfatório.
    e. 5/5: incrível, impressionante, surpreendente.
    f. None: Caso não tenha avaliação

    Seu resultado final deve ser duas listas em python, de mesmo tamanho, uma com os scores de comida e outra com os scores de atendimento ao cliente.
    Ao final da sua avaliação, caso as listas de avaliações não tenham o mesmo tamanho devido a avaliações ausentes, preencha-os com o inteiro mais próximo da média da lista, para que as duas listas tenham o mesmo tamanho.
    Explique sua lógica passo a passo.
    Ao final, escreva o resultado final no seguinte formato:
    {"customer_service_scores":[...],"food_scores":[...],"restaurant_name":"..."}
    """,
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )

    # agente responsável por indicar a função para calcular scores geral de um restaurante
    score_agent = ConversableAgent(
        name="ScoreCalculator",
        system_message="You are a helpful AI assistant. "
        "Your only job is to compute overall reviews scores for a given restaurant.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1, # Usada para impedir a última chamada de LLM (ScoreCalculator -> Executor), que não é necessária
    )

    # agente responsável por executar as funções indicadas por outros agentes
    executor_agent = ConversableAgent(
        name="Executor Agent",
        llm_config=False,
        human_input_mode="NEVER",
    )

    register_function(
        fetch_restaurant_data,
        caller=data_fetch_agent, 
        executor=executor_agent,  
        name="get_restaurant_reviews", 
        description="Get reviews for a given restaurant",  
    )

    register_function(
        calculate_overall_score,
        caller=score_agent,
        executor=executor_agent,  
        name="calculate_overall_score", 
        description="Computes the overall score of reviews for a given restaurant. ",
    )

    # Inicia o fluxo sequencial de chamada de agentes para que a resposta final seja obtida.
    chat_results = executor_agent.initiate_chats(
        [
            {
                "recipient": data_fetch_agent,
                "message": user_query,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": review_analysis_agent,
                "message": "Analise as avaliações do restaurante a seguir e converta-as para avaliações numéricas.",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": score_agent,
                "message": "Converta esses scores numéricos em uma única avaliação do restaurante.",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
        ]
    )
    
# NÃO modifique o código abaixo.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Certifique-se de incluir uma consulta para algum restaurante ao executar a função main."
    main(sys.argv[1])