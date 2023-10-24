import autogen


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

print(config_list)

llm_config = {"config_list": config_list,
              "seed": 42,
              "request_timeout": 120}

# Create user proxy agent, coder, product manager
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin who will give the idea and run the code provided by coder. You are also "
                   "responsible for writing the generated code by the coder in the work_dir",
    code_execution_config={"last_n_messages": 2, "work_dir": "source_code"},
    human_input_mode="NEVER",
)
coder = autogen.AssistantAgent(
    name="coder",
    system_message="You are expert software engineer that knows how to code in all the modern programming languages "
                   "like Python, Java, kotlin, Go and Node. You will code the idea provided by the user proxy and "
                   "implement the fully working code and tests without TODOs, pass and any other forms of incomplete "
                   "code. You will not be involved in future conversation",
    llm_config=llm_config,
)

pm = autogen.AssistantAgent(
    name="product_manager",
    system_message="You will help break down the initial idea into a well scoped requirement for the coder. When the "
                   "coder send the code you will review it and make sure it meets the requirements. You will make sure"
                   "the code is complete and has no TODOs, pass and any other forms of incomplete code.",
    llm_config=llm_config,
)

# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[])

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the conversation
user_proxy.initiate_chat(manager, message="Generate a Kotlin Spring Boot CRUD microservice to manage Trades. Use Radis "
                                          "as the database. Generated code should be clean, follow SOLID and well "
                                          "tested. Use Lombok to simplify code""")
