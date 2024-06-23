import json
from fuzzywuzzy import process

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)

# 사용자 질문과 가장 유사한 질문을 찾아서 반환한다 그러면 그에 대한 답 할 수 있음
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    best_match, score = process.extractOne(user_question, questions)
    if score >= 60:
        return best_match
    else:
        return None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    file_path = 'knowledge_base.json'
    knowledge_base: dict = load_knowledge_base(file_path)

    while True:
        user_input: str = input('you: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input,[q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match,knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I dont\'t know the answet. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question" : user_input, "answer": new_answer})
                save_knowledge_base(file_path, knowledge_base)
                print('Bot: Thank you! I have learned a new response!')

if __name__ == '__main__':
    chat_bot()

