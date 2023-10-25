import autogen
from autogen.retrieve_utils import TEXT_FORMATS
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    file_location=".",
    filter_dict={
        "model": {
            "gpt-3.5-turbo-16k"
        }
    },
)

assert len(config_list) > 0
print("models to use: ", [config_list[i]["model"] for i in range(len(config_list))])

print("Accepted file formats for `docs_path`:")
print(TEXT_FORMATS)

autogen.ChatCompletion.start_logging()

# 1. create an RetrieveAssistantAgent instance named "assistant"
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
    },
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "qa",
        "docs_path": "/Users/chamindawijayasundara/Documents/research/multiagent/autogen-research/rag/docs/llava.pdf",
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "embedding_model": "all-mpnet-base-v2",
        "get_or_create": False,  # set to True if you want to recreate the collection
    },
)

# reset the assistant. Always reset the assistant before starting a new conversation.
assistant.reset()
message = """I'm writing a blog to introduce LLaVA. Find answers to the 3 questions 
    below and write a summery.
    1. What is LLaVA?
    2. Why do you need it?
    3. How to use? """

qa_problem = message
ragproxyagent.initiate_chat(assistant, problem=qa_problem, search_string="llava")