import json
import random


def get_recent_message():
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
