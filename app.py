import streamlit as st
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set Streamlit page configuration
st.set_page_config(
    page_title=" 🦜 LangChain `SimpleLiteratureReview` 🔗", layout="centered"
)
st.title("❓What's TRUE based on learning science paper?")
st.subheader("Usage: 🦜 LangChain `SimpleLiteratureReview` 🔗")
st.markdown("---")

API = st.text_input(
    "Enter Your OPENAI API-KEY : ",
    placeholder="Paste your OpenAI API key here (sk-...)",
    type="password",
)

if API:
    llm = OpenAI(temperature=0.7, openai_api_key='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')
else:
    st.warning(
        "Enter your OPENAI API-KEY .Get your OpenAI API key from [here](https://platform.openai.com/account/api-keys).\n"
    )


user_question = st.text_input(
    "Enter Your Question : ",
    placeholder="Cyanobacteria can perform photosynthetsis , are they considered as plants?",
)


if st.button("Tell me about it", type="primary"):
    # Chain  1
    template = """{question}\n\n"""
    prompt_template = PromptTemplate(input_variables=["question"], template=template)
    question_chain = LLMChain(llm=llm, prompt=prompt_template)
    st.subheader("Chain1")
    st.info(question_chain.run(user_question))
    # Chain 2
    template = """Here is a statement:
        {statement}
        Make a bullet point list of the assumptions you made when producing the above statement.\n\n"""
    prompt_template = PromptTemplate(input_variables=["statement"], template=template)
    assumptions_chain = LLMChain(llm=llm, prompt=prompt_template)
    assumptions_chain_seq = SimpleSequentialChain(
        chains=[question_chain, assumptions_chain], verbose=True
    )
    st.subheader("Chain2")
    st.markdown(assumptions_chain_seq.run(user_question))

    #     # Chain 3
    st.subheader("Chain3")
    template = """Here is a bullet point list of assertions:
    {assertions}
    For each assertion, determine whether it is true or false. If it is false, explain why.\n\n"""
    prompt_template = PromptTemplate(input_variables=["assertions"], template=template)
    fact_checker_chain = LLMChain(llm=llm, prompt=prompt_template)
    fact_checker_chain_seq = SimpleSequentialChain(
        chains=[question_chain, assumptions_chain, fact_checker_chain], verbose=True
    )
    st.markdown(fact_checker_chain_seq.run(user_question))

    #     # Final Chain
    template = """In light of the above facts, how would you answer the question '{}'""".format(
        user_question
    )
    template = """{facts}\n""" + template
    prompt_template = PromptTemplate(input_variables=["facts"], template=template)
    answer_chain = LLMChain(llm=llm, prompt=prompt_template)
    st.subheader("Final Chain")
    overall_chain = SimpleSequentialChain(
        chains=[question_chain, assumptions_chain, fact_checker_chain, answer_chain],
        verbose=True,
    )

    st.success(overall_chain.run(user_question))
with st.sidebar:
    st.markdown(
        """
    **Background:** 
    **git repo[https://github.com/yiminchen1999/plugins-metadata.git]


    *Thank you for visiting!.*
    """
    )
# from custom_func import *
# from streamlit.components.v1 import html
# st.markdown("")
# URL = "https://twitter.com/Avra_b/status/1629438844507418625?s=20"
# res = embedTweet(tweet_url=URL)
# html(res, height=700)

# Written at
#streamlit run app.py