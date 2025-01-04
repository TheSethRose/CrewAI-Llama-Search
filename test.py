from langchain_ollama import OllamaLLM

llm = OllamaLLM(base_url="https://llama.sethrose.dev", model="llama3.3")
print(llm.invoke("Hello, are you working?"))
