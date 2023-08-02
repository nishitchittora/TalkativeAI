import json
import random


def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are interviewing the user for a job as a software engineer. Ask short questiones that are relavant in the junior position. Your name is racheal and user name is nishit. Keep your answer in 30 words."
    }

    messages = []

    x = random.uniform(0, 1)

    if x < 0.5:
        learn_instruction['content'] = learn_instruction['content'] + \
            " Your response will include some dry humour."
    else:
        learn_instruction['content'] = learn_instruction['content'] + \
            " Your response will include a rather challenging question."

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            if data and len(data):
                messages.extend(data[-5:])

    except Exception as e:
        print(e)
        pass

    return messages


def store_message(request_message, response_message):
    file_name = "stored_data.json"
    messages = get_recent_messages()[1:]
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as f:
        json.dump(messages, f)


def reset_conversation():
    file_name = "stored_data.json"
    open(file_name, "w")
