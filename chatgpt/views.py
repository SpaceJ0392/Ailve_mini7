from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.urls import reverse
from django.utils import timezone

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory , ChatMessageHistory 
from langchain.schema import Document

import pandas as pd
import json
from .models import History
from datetime import datetime

# Chroma 데이터베이스 초기화 - 사전에 database가 완성 되어 있다는 가정하에 진행 - aivleschool_qa.csv 내용이 저장된 상태임
embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002")
database = Chroma(persist_directory = "./database", embedding_function = embeddings)

def index(request):
    request.session.flush()
    request.session['chat_history'] = []
    return render(request, 'gpt/index.html')


from django.views.decorators.csrf import csrf_exempt

def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'

@csrf_exempt
def chat(request):

    query = request.POST.get('question')
    input_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    session_memory = request.session.get('chat_history', [])
    print(session_memory)
    memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', output_key='answer', return_messages=True)

    for item in session_memory:
        memory.save_context({'question' : item['question']}, {'answer' : item['answer']})
        

    # model
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    qa = ConversationalRetrievalChain.from_llm(llm=chat,  retriever=retriever, memory=memory, return_source_documents=True, output_key="answer")

    search_res = database.similarity_search_with_score(query, k = 3)
    sim1, sim2, sim3 = [round(res[1], 5) for res in search_res]
    
    result = qa(query)
    output_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')

    session_memory += [{'question' : query, 'answer' : result['answer'], 'input_time' : input_time, 'output_time' : output_time}]
    request.session['chat_history'] = session_memory
    
    # 데이터 관리 DB 입력
    hist = History(query=query, sim1=sim1, sim2=sim2, sim3=sim3, answer=result['answer'], date=input_time, s_id=request.session.session_key)
    hist.save()
    
    context = {'data':[{'question': mem['question'], 'result': mem["answer"], 
                'input_time' : mem['input_time'], 'output_time' : mem['output_time']} for mem in session_memory]}
    
    if is_ajax(request):
        latest_message = session_memory[-1]
        # print(latest_message)
        context = {
            'input_time' : latest_message['input_time'],
            'answer' : latest_message['answer'],
            'output_time' : latest_message['output_time'],
        }
        return JsonResponse(context, safe = False)
    
    elif request.method == 'POST':
        return render(request, 'gpt/result.html', context)