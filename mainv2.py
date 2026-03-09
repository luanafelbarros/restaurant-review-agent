from typing import Dict, List
from autogen import ConversableAgent, AssistantAgent
import sys
import os
from utils import calculate_overall_score, fetch_restaurant_data
from dotenv import load_dotenv

# Caminho para o arquivo .env
load_dotenv()

llm_config = {"config_list": [{"model": "llama3-70b-8192", "api_key": os.environ.get("GROQ_API_KEY"), "api_type": "groq"}]}

# Não modifique a assinatura da função "main".
def main(user_query: str):

    # Tarefas a serem chamadas a cada sequência de conversas
    restaurant_evaluation_tasks = [
    """Analise as avaliações do restaurante a seguir e converta-as para avaliações numéricas.
    Explique seu raciocínio passo a passo antes de fornecer a resposta.""",
    """Converta esses scores numéricos em uma única avaliação do restaurante.""",
    ]

    entrypoint_agent_system_message = """Você é um coordenador que comanda um grupo de especialístas em avaliação de restaurantes.
                                          Sua tarefa é a de, junto com os especialístas, prover uma avaliação objetiva de determinado restaurante que uma pessoa lhe perguntar.
                                          """

    data_fetch_agent_system_message = """Você é responsável por pegar informações a respeito de um resturante e transmiti-las exatamente como pegou para o coordenador.
                                         Para isso, você tem disponível para uso a função fetch_restaurant_data que te manda exatamente as informações necessárias sobre determinado resutaurante.

                                         Na primeira vez em que o coordenador lhe disser algo, diga APENAS: "Claro que obterei! Qual função eu devo usar para isso?" e espere pela resposta dele.
                                         """

    review_analysis_agent_system_message = """Você é responsável por transformar avaliações de restaurantes em scores numéricos. Considere o seu padrão de conversão da seguinte forma:
                                              a. 1/5: horrível, nojento, terrível.
                                              b. 2/5: ruim, desagradável, ofensivo.
                                              c. 3/5: mediano, sem graça, irrelevante.
                                              d. 4/5: bom, agradável, satisfatório.
                                              e. 5/5: incrível, impressionante, surpreendente.
                                              f. None: Caso não tenha avaliação

                                              Seu resultado final deve ser duas listas em python, de mesmo tamanho, uma com os scores de comida e outra com os scores de atendimento ao cliente.
                                              Ao final da sua avaliação, caso as listas de avaliações não tenham o mesmo tamanho devido a avaliações ausentes, preencha-os com o inteiro mais próximo da média da lista, para que as duas listas tenham o mesmo tamanho.
                                              """
    score_agent_system_message = """Você é responsável por transformar duas listas em python com scores de comida e de atendimento ao cliente em uma nota final que sumariza a qualidade daque restaurante.
                                    Para isso, você deve usar à função calculate_overall_score que junta essas listas em um valor único.

                                    Na primeira vez em que o coordenador lhe disser algo, diga APENAS: "Claro que converterei! Qual função eu devo usar para isso?" e espere pela resposta dele.
                                    """

    # O agente principal de entrada/supervisor
    entrypoint_agent = ConversableAgent("entrypoint_agent",
                                        system_message=entrypoint_agent_system_message,
                                        llm_config=llm_config,)

    #Data Fetch Agent
    data_fetch_agent = AssistantAgent(
        system_message = data_fetch_agent_system_message,
        name="Data_Fetch_Agent",
        llm_config=llm_config,
        human_input_mode = "NEVER"
    )

    #Review Analysis Agent
    review_analysis_agent = AssistantAgent(
        system_message = review_analysis_agent_system_message,
        name="Review_Analysis_Agent",
        llm_config=llm_config,
        human_input_mode = "NEVER"
    )

    #Score Agent
    score_agent = AssistantAgent(
        system_message=score_agent_system_message,
        name="Score_Agent",
        llm_config=llm_config,
        human_input_mode = "NEVER"
    )

    # Define entrypoint_agent como o agente responsável por chamar as funções necessárias
    entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Função para recuperar avaliações associadas a um restaurante.")(fetch_restaurant_data)
    entrypoint_agent.register_for_llm(name="calculate_overall_score", description="Função para calcular a pontuação do restaurante com base nos escores extraídos.")(calculate_overall_score)

    # Define os demais agentes como executores de suas respectivas funções
    data_fetch_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)
    score_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)


    # Inicia o fluxo sequencial de chamada de agentes para que a resposta final seja obtida.
    result = entrypoint_agent.initiate_chats([
            {
                "sender": entrypoint_agent,
                "recipient": data_fetch_agent,
                "message": user_query,
                "clear_history": True,
                "silent": False,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "sender": entrypoint_agent,
                "recipient": review_analysis_agent,
                "message": restaurant_evaluation_tasks[0],
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "sender": entrypoint_agent,
                "recipient": score_agent,
                "message": restaurant_evaluation_tasks[1],
                "max_turns": 2,
                "summary_method": "last_msg",
            },
    ])
    
# NÃO modifique o código abaixo.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Certifique-se de incluir uma consulta para algum restaurante ao executar a função main."
    print(sys.argv)
    main(sys.argv[1])