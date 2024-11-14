from langchain_openai import ChatOpenAI  
from langchain_core.messages import HumanMessage, AIMessage

class ChatManager:
    def __init__(self, config):
        self.config = config
        self.chat_model = ChatOpenAI(
            model_name=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            api_key=config.OPENAI_API_KEY 
        )
        self.conversation_history = []
    
    def generate_response(self, query: str, context: str) -> str:
        # Create messages list
        messages = [
            {"role": "system", "content": "You are a helpful customer support assistant. Use the following context to answer questions:"},
            {"role": "system", "content": f"Context: {context}"}
        ]
        
        # Add conversation history
        for msg in self.conversation_history[-5:]:  # Keep last 5 messages for context
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            else:
                messages.append({"role": "assistant", "content": msg.content})
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Generate response
        response = self.chat_model.generate([messages])
        
        # Extract the response text
        response_text = response.generations[0][0].text
        
        # Update conversation history
        self.conversation_history.append(HumanMessage(content=query))
        self.conversation_history.append(AIMessage(content=response_text))
        
        return response_text