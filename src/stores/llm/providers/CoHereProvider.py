from ..LLMinterface import LLMInterface
import logging
import cohere
from ..LLMnums import CoHereEnums, DocumentTypeEnum
class CoHereProvider(LLMInterface):
    def __init__(self, api_key:str,
                    default_input_max_chars:int=1000,
                    default_generation_max_output_tokens: int=1000,
                    default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.default_input_max_chars = default_input_max_chars
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_max_temperature = default_generation_temperature

        self.gerneration_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key)
        self.logger = logging.getLoggerClass(__name__)

    def set_generation_models(self, mode_id: str):
        self.gerneration_model_id=mode_id
    
    def set_embedding_model(self, model_id: str,embedding_size: int):
        self.set_embedding_model = model_id
        self.embedding_size = embedding_size
    def process_text(self, text:str):
        return text[:self.default_input_max_chars].strip()
    def generate_text(self, prompt: str, max_output_tokens: int, chat_history: list = [], temperature: float = None):
        if not self.gerneration_model_id:
            self.logger.error("OpenAI model was not set")
            return None

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_max_temperature
        
        response  = self.client.chat(message=self.process_text(prompt),
                                    model=self.gerneration_model_id,
                                    chat_history=chat_history,
                                    temperature=temperature,
                                    max_tokens=max_output_tokens)

        if not response or response.text:
            self.logger.error('Error with gernerating text')
            return None
        return response.text
    def embed_text(self, text: str, document_type: str = None):
        if not self.embedding_model_id:
            self.logger.error("OpenAI embeded model was not set")
            return None

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnums.QUERY.value
        
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=['float']
        )
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error('Error with embeding text generation')
            return None
        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role" : role,
            "text": self.process_text(prompt)
        }
        
    
        