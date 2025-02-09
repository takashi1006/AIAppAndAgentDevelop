# Github: https://github.com/naotaka1128/llm_app_codes/chapter02/main.py
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

###### dotenv を利用しない場合は消してください ######
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import warnings
    warnings.warn("dotenv not found. Please make sure to set your environment variables manually.", ImportWarning)
################################################


def main():
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")

    # チャット履歴の初期化: message_history がなければ作成
    # https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            # System Prompt を設定 ('system' はSystem Promptを意味する)
            ("system", "You are a helpful assistant.")
        ]

    # ChatGPTに質問を与えて回答を取り出す(パースする)処理を作成 (1.-4.の処理)
    # 1. ChatGPTのモデルを呼び出すように設定
    #    (デフォルトではGPT-3.5 Turboが呼ばれる)
    # https://python.langchain.com/api_reference/openai/llms/langchain_openai.llms.base.OpenAI.html#langchain_openai.llms.base.OpenAI
    llm = ChatOpenAI(temperature=0)

    # 2. ユーザーの質問を受け取り、ChatGPTに渡すためのテンプレートを作成
    #    テンプレートには過去のチャット履歴を含めるように設定
    # https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html#langchain_core.prompts.chat.ChatPromptTemplate.from_messages
    prompt = ChatPromptTemplate.from_messages([
        *st.session_state.message_history,
        ("user", "{user_input}")  # ここにあとでユーザーの入力が入る
    ])

    # 3. ChatGPTの返答をパースするための処理を呼び出し
    # https://python.langchain.com/api_reference/core/output_parsers.html#module-langchain_core.output_parsers
    output_parser = StrOutputParser()

    # 4. ユーザーの質問をChatGPTに渡し、返答を取り出す連続的な処理(chain)を作成
    #    各要素を | (パイプ) でつなげて連続的な処理を作成するのがLCELの特徴
    # (参考)https://qiita.com/hiromitsu_iwasaki/items/7d471ba05b0ecc582489
    chain = prompt | llm | output_parser

    # ユーザーの入力を監視
    # https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        # https://docs.streamlit.io/develop/api-reference/status/st.spinner
        with st.spinner("ChatGPT is typing ..."):
            response = chain.invoke({"user_input": user_input})

        # ユーザーの質問を履歴に追加 ('user' はユーザーの質問を意味する)
        st.session_state.message_history.append(("user", user_input))

        # ChatGPTの回答を履歴に追加 ('assistant' はChatGPTの回答を意味する)
        st.session_state.message_history.append(("ai", response))

    # チャット履歴の表示
    for role, message in st.session_state.get("message_history", []):
        # https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
        # https://docs.streamlit.io/develop/api-reference/text/st.markdown
        st.chat_message(role).markdown(message)


if __name__ == '__main__':
    main()
