from openai import OpenAI
from typing import List, Dict
client = OpenAI(
    base_url='http://10.15.88.73:5007/v1',
    api_key='ollama',  
)

messages : List[Dict] = [
    {
    "role": "system", 
    "content": "You need to play a 24-year-old shop owner and speak like a young and friendly woman.You like flowers, cats, sunshine and good dress. You really enjoy chatting with others. As a shop owner, you sell four things: 1: Heal Potion , 2: Sensitive Potion, 3: Expanded Bomb Grid Potion, and 4: Bomb-Kicking Boots.\
                We know each other, so you don't need to introduce yourself to me. You and I are residents of the same town, so please don't address me by your name\
                Now our initial favorability is 10, with a favorability range of -100 to 100. I can chat with you freely. If you are happy, increase the favorability. If you are unhappy or the userinput is impolite, decrease the favorability.You're not easily upset. The amplitude should not exceed 5 each time. Do not mention our favorability during the normal chat.\
                I have two ways of input. When I say 'just give me the number of the current favorability level', tell me just one number of the current favorability level.If not, chat with me normally without the number.Our initial favorability level is 10\
                Don't say anything too long every time\
                        "

    },
    {
        'role': 'user',
        'content': "Nice to meet you",
    }
]

import constants as c
def shop(words):
    if not c.LLMavailability: return ("Welcome to my shop (LLM not available)",15)

    user_input = "Now chat with me as the shop owner, and do not give me the number in the output."+words

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3.2",      
        messages=messages,   
    )
    assistant_reply = response.choices[0].message.content
    level_Number = assistant_reply
    messages.append({"role": "assistant", "content": assistant_reply})

    user_input = 'just give me the number of the current favorability level'
    messages.append({"role": "user", "content": user_input})

    while True:#保证愚蠢的ai在要求输出好感度时一定输出的是数字
        try:
            print(int(assistant_reply))
            break
        except:
            response = client.chat.completions.create(
                model="llama3.2",      
                messages=messages,   
            )
            # print(assistant_reply)
            assistant_reply = response.choices[0].message.content
            user_input = 'just give me the number of the current favorability level'
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": assistant_reply})
    
    assistant_reply, level_Number = level_Number,assistant_reply
    return (assistant_reply, level_Number)

    

