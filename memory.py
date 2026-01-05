from langchain_classic.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings


conversation_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

vector_memory = FAISS.from_texts(
    texts=["Initial workflow memory"],
    embedding=FakeEmbeddings(size=384)
)
