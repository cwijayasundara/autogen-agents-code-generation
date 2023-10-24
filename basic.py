import autogen

from autogen import AssistantAgent, UserProxyAgent


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-3.5-turbo-16k"],
    },
)

print(config_list)


# Create assistant agent
assistant = AssistantAgent(name="assistant",
                           llm_config={"config_list": config_list})

# Create user proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"})

message = """ Whats the best performing 10 technology stocks in the last 5 years? Use Yahoo finance data"""

user_proxy.initiate_chat(assistant, message=message)