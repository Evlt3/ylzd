import streamlit as st
from openai import OpenAI
from common import get_llm_response


def get_answer(question: str):
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        stream = get_llm_response(client, model=model_name,user_prompt=question,stream=True)
        for chunk in stream:
            yield chunk.choices[0].delta.content or ''
    except Exception as e:
        yield from '暂时无法提供回复，请检查你的配置是否正确。'


with st.sidebar:
    api_vendor = st.radio(label='请选择服务提供商：',options=['OpenAI','DeepSeek'])
    if api_vendor =='OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_option = ['gpt-4o-mini','gpt-3.5-turbo','gpt-4o','gpt-4.1-mini','gpt-4.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https//api.deepseek.com'
        model_option = ['deepseek-chat','deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：', options=model_option)
    api_key = st.text_input(label='请输入你的KEY：',type='password')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai','你好，我是你的大佐。')]

st.write('## 我是大佐')

if not api_key:
    st.error('请提供API KEY')
    st.stop()

for role, content in st.session_state['messages']:
    st.chat_message(role).write(content)

user_input = st.chat_input(placeholder='请输入')
if user_input:
    _, history = st.session_state['messages'][-1]
    st.session_state['messages'].append(('human',user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('大佐正在思考。'):
        answer = get_answer(f'{history},{user_input}')
        result = st.chat_message('ai').write_stream(answer)
        st.session_state['messages'].append(('ai',result))