from langchain_openai import ChatOpenAI

###### dotenv を利用しない場合は消してください ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################

llm = ChatOpenAI(temperature=0)
result = llm.invoke("こんにちわ!ChatGPT!")
print(result)
