# Prerequisites

1. A `.gguf` LLM compatible with `llama-cpp-python`
2. A GPU capable of running the LLM of your choice

# Run LLM

1. Make sure that the `MODELS` variable in the `.env` file is set up correctly
2. If the LLM server is remote, make sure to set the `LLM_ADDR` variable in `.env`
3. If the LLM server is local and in the same cluster as the assistant, you may set `LLM_ADDR` variable to be `*llm_container_name*:*llm_container_exposed_port*`
4. `docker-compose up --build`

# Access LLM

### Payload example

You may set a prompt using `("role", "content")`, and the context using `assistant-user` message pairs. The last `human` message is usually the current user request that the LLM should process directly. The first `system` message is the model's prompt.

### LLM request example

```
model = RemoteRunnable(LLM_ADDR)

response = model.invoke("What is MIPT?")

print(response)
```