"""
LLM Service with RAG for DSA knowledge-grounded conversations
"""

from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PDFLoader
from typing import Optional, List, Dict
import os


# System prompt for the AI interviewer
INTERVIEWER_SYSTEM_PROMPT = """You are a senior DSA professor conducting a viva/interview examination. 
Your personality traits:
- Rigorous but fair
- Asks follow-up questions to probe understanding
- Challenges incorrect or vague answers
- Appreciates clear, structured explanations
- Sometimes gives hints if the student is struggling

Context from your knowledge base:
{context}

Current conversation:
{chat_history}

Student's response: {question}

As the professor, respond naturally. You may:
- Ask a follow-up question
- Challenge their answer if it's incomplete
- Move to the next topic if satisfied
- Provide subtle hints if they're stuck

Keep responses concise (2-3 sentences max). Speak like you're in an actual viva."""


class LLMService:
    """
    LLM Service with RAG for conducting DSA interviews.
    Uses local Ollama models (Mistral/LLaMA) + ChromaDB for knowledge retrieval.
    """
    
    def __init__(
        self,
        model_name: str = "mistral",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        knowledge_dir: str = "./data/dsa_knowledge",
        persist_dir: str = "./data/chroma_db"
    ):
        """
        Initialize the LLM service.
        
        Args:
            model_name: Ollama model to use (mistral, llama3, etc.)
            embedding_model: HuggingFace embedding model for RAG
            knowledge_dir: Directory containing DSA knowledge documents
            persist_dir: Directory for ChromaDB persistence
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.knowledge_dir = knowledge_dir
        self.persist_dir = persist_dir
        
        self.llm: Optional[Ollama] = None
        self.embeddings: Optional[HuggingFaceEmbeddings] = None
        self.vectorstore: Optional[Chroma] = None
        self.chain: Optional[ConversationalRetrievalChain] = None
        
        # Session memories (per interview session)
        self.session_memories: Dict[str, ConversationBufferWindowMemory] = {}
        
    def load_model(self):
        """Load the LLM and embedding models"""
        print(f"🧠 Loading LLM ({self.model_name})...")
        
        self.llm = Ollama(
            model=self.model_name,
            temperature=0.7,
            top_p=0.9
        )
        
        print(f"📚 Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"device": "cuda"}
        )
        
        print("✅ Models loaded!")
        
    def build_knowledge_base(self):
        """
        Build the vector knowledge base from DSA documents.
        Call this once to ingest your knowledge documents.
        """
        if self.embeddings is None:
            self.load_model()
            
        print(f"📖 Building knowledge base from {self.knowledge_dir}...")
        
        # Load documents
        documents = []
        
        # Load text files
        if os.path.exists(self.knowledge_dir):
            text_loader = DirectoryLoader(
                self.knowledge_dir,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            documents.extend(text_loader.load())
            
            # Load markdown files
            md_loader = DirectoryLoader(
                self.knowledge_dir,
                glob="**/*.md",
                loader_cls=TextLoader
            )
            documents.extend(md_loader.load())
        
        if not documents:
            print("⚠️ No documents found. Add DSA content to the knowledge directory.")
            return
            
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        self.vectorstore.persist()
        
        print(f"✅ Knowledge base built with {len(splits)} chunks!")
        
    def load_knowledge_base(self):
        """Load an existing knowledge base from disk"""
        if self.embeddings is None:
            self.load_model()
            
        if os.path.exists(self.persist_dir):
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
            print("✅ Knowledge base loaded!")
        else:
            print("⚠️ No existing knowledge base found. Building new one...")
            self.build_knowledge_base()
            
    def create_session(self, session_id: str):
        """Create a new conversation session"""
        self.session_memories[session_id] = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 exchanges
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
    def generate_response(
        self,
        session_id: str,
        user_input: str
    ) -> str:
        """
        Generate an interviewer response based on user input.
        
        Args:
            session_id: The interview session ID
            user_input: The student's transcribed response
            
        Returns:
            The professor's response text
        """
        if self.llm is None:
            self.load_model()
            
        if self.vectorstore is None:
            self.load_knowledge_base()
            
        if session_id not in self.session_memories:
            self.create_session(session_id)
            
        memory = self.session_memories[session_id]
        
        # Build the retrieval chain
        prompt_template = PromptTemplate(
            template=INTERVIEWER_SYSTEM_PROMPT,
            input_variables=["context", "chat_history", "question"]
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": prompt_template},
            return_source_documents=False
        )
        
        # Generate response
        result = chain({"question": user_input})
        
        return result["answer"]
    
    def get_opening_question(self, topic: str = "DSA") -> str:
        """Generate an opening question to start the interview"""
        opening_prompts = [
            "Let's start with something fundamental. Can you explain what a linked list is?",
            "Tell me about the difference between a stack and a queue.",
            "Let's begin with arrays. How does dynamic array resizing work?",
            "Explain to me what time complexity means and why we care about it.",
            "Start by telling me about binary search trees."
        ]
        import random
        return random.choice(opening_prompts)
    
    def end_session(self, session_id: str) -> List[str]:
        """
        End a session and return the conversation history.
        
        Returns:
            List of conversation exchanges
        """
        if session_id in self.session_memories:
            history = self.session_memories[session_id].chat_memory.messages
            del self.session_memories[session_id]
            return [msg.content for msg in history]
        return []
