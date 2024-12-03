
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    
    for question in PYTHON_QUESTION_LIST:
        if question["id"] == current_question_id:
            session["answers"][current_question_id] = {
                "question": question["question"],
                "user_answer": answer,
                "is_correct": answer.strip().lower() == question["correct_answer"].strip().lower(),
            }
            return True, ""
    return False, "Invalid question ID."


def get_next_question(current_question_id):
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        if question["id"] == current_question_id:
            if i + 1 < len(PYTHON_QUESTION_LIST):
                next_question = PYTHON_QUESTION_LIST[i + 1]
                return next_question["question"], next_question["id"]
            else:
                return None, -1  # No more questions left
    return PYTHON_QUESTION_LIST[0]["question"], PYTHON_QUESTION_LIST[0]["id"]  # Start with the first question


def generate_final_response(session):
    correct_count = sum(1 for answer in session["answers"].values() if answer["is_correct"])
    total_questions = len(PYTHON_QUESTION_LIST)
    result_message = f"You answered {correct_count} out of {total_questions} questions correctly.\n\n"
    
    for question_id, answer_data in session["answers"].items():
        result_message += (
            f"Q: {answer_data['question']}\n"
            f"Your Answer: {answer_data['user_answer']}\n"
            f"{'Correct!' if answer_data['is_correct'] else 'Incorrect!'}\n\n"
        )
    
    return result_message
