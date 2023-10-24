from flaml import autogen
from autogen import config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")


assistant = autogen.AssistantAgent(name="assistant",
                                   llm_config={"config_list": config_list})


user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "flaml_coding"})

user_proxy.initiate_chat(assistant, message="Show me the YTD gain of 10 largest technology companies as of today.")
