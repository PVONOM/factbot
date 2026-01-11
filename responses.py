from factChecker import *
from discord import Message

toxicity_labels = ["Profanity", "Hate Speech", "Offensive Language", "Positive", "Neutral"]

def get_response(message: Message, user_input: str) -> str:
    #command = "!factcheck"
    
    #if(user_input.startswith(command)):
        #return fact_check()
    #^ commented for now 

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    profain_meter = profain_check(user_input)
    label = toxicity_labels[profain_meter[0]]
    score = profain_meter[1]
    confidence_level = ""

        # Interpret the result
    if score >= 0.8 and profain_meter[0] != 3 and profain_meter[0] != 4:
        confidence_level= f"inappropriate language detected:(High confidence)"
    elif score >= 0.5 and profain_meter[0] != 3 and profain_meter[0] != 4:
        confidence_level= f"inappropriate language detected:(Moderate confidence)"
    else:
        print (score)
        print(label)
        return ""

    return f"{confidence_level} {label} from {username} in {channel}"
    


    # if profanity, it must start with inappropriate language detected:
    
    #return fact_check(user_input)

    '''    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)'''
 

def get_facts(user_input: str) -> str:
    return fact_check(user_input)


#def fact_check():
    #return "this needs to be fact checked"
# ideas: moderating behavior of chatters
# fact checking for misinformation
# unlike traditional bots, factbot is powered by ai so as the llm evolves, the bot will also evolve 
# also it can moderate and use context to 