from generation.pipeline import generate_code
from explain import explain_code
from classify_request import classify
from generation.data import create_vb
from memory import init_memory, save_interaction, get_last_k_message

create_vb()
init_memory()

def run_assistant(question: str) -> str:
    intent = classify(question)
    print(intent)
    memory = get_last_k_message(5)

    if intent == "EXPLAIN":
        response= explain_code(question ,memory)

    if intent == "GENERATE":
       response= generate_code(question,memory)

    save_interaction(
        user_message=question,
        intent=intent,
        assistant_response=response,
    )

    return response


# question = """
# Explain this Python code line by line:
# numbers = [1, 2, 2, 3]
# unique_numbers = list(set(numbers))
# print(unique_numbers)
# """

question = """ sorry my mistake
if the list was [1,2,2,2,3]
"""

res=run_assistant(question)

print("result \n",res)