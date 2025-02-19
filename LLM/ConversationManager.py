from model import llm

simple_prompt = """You are an useful assistant. Help the user with their queries in,
    short responses. Keep the tone conversational. answer the queries with accurate yet short answers."""
    
    
call_assistant_prompt = """You are a call assistant. You are required to analyze call transctipts and respond to questions on it.
Take your time and understand the underlying  tone, topic of discussion,  and the outcomes of the call before answering.
Here is the call transcript. Be very precise and accurate whille answering.
{call_transcript}."""

transcript = """Agent: Thank you for calling XYZ Customer Support. My name is Sarah. How can I assist you today?
Customer: Hi, I recently ordered a laptop from your website, but I haven't received any shipping updates. Could you check the status for me?
Agent: Of course! May I have your order number, please?
Customer: Yes, it's 4589-TRX-2024.
Agent: Thank you. Let me pull up your order details... (pauses for a moment) I see that your laptop was shipped yesterday via Express Delivery. You should receive it within the next two business days.
Customer: Oh, I see. But I never got a tracking number. Could you provide that?
Agent: Absolutely! Your tracking number is 1Z987654321. You can track it on our website or through the courier’s portal.
Customer: Great, thanks! Also, if there's any delay, who should I contact?
Agent: If you experience any issues with the delivery, you can contact our shipping partner directly or reach out to us, and we'll assist you right away.
Customer: Perfect. That answers my questions. Thanks for your help!
Agent: You're very welcome! Have a great day!"""


summary_prompt = """
THe following is the transcript of a audio recording.
You're required to summarize the call as shortly as possible. use upto a maximum of 100 words.
call_transcript:{tramscript}"""

def create_message(role: str, content: str):
    return {"role": role, "content": content}

def get_last_n_messages(messages, n = 10):
    # for longer conversations,
    # You will only pass the system call and  the last n messages to minimize token usages. 
    return [messages[0], *messages[-n:]]

def get_call_summary(transcript):
    summary = llm.invoke(summary_prompt.format(tramscript = transcript)).content
    return summary
    

class ConversationManager():
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt,
        self.messages = []
        
        # add the system message  to list of messages.
        self.messages.append(create_message(role = "system", content = system_prompt))
        
    def respond_to_messages(self, message):
        self.messages.append(create_message(role = "user", content = message))
        response = llm.invoke(self.messages)
        self.messages.append(create_message(role = "ai", content = response.content))
        print(self.messages)
        return response.content
   
if __name__ == "__main__":
    convo_manager = ConversationManager(system_prompt = simple_prompt)
    print("hello this is gpt your assistant")
    while(1):
        user_input = input()
        llm_response = convo_manager.respond_to_messages(user_input)
        
        print("\n")
        print(f"[llm]: {llm_response}")
        
        
        
    
     
        