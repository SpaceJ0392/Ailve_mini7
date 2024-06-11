from multiprocessing.connection import answer_challenge
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

from selfchatgpt.models import History

embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002")
database = Chroma(persist_directory = "./database", embedding_function = embeddings)

def index(request):
    return render(request, 'selfchatgpt/index.html')

def chat(request):
    query = request.POST.get('question')
    session_memory = request.session.get('chat_history', [])
    print(session_memory)
    
    memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', output_key='answer', return_messages=True)

    for item in session_memory:
        memory.save_context({'input' : item['human']}, {'output' : item['ai']})
    
    # model
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    qa = ConversationalRetrievalChain.from_llm(llm=chat,  retriever=retriever, memory=memory, return_source_documents=True, output_key="answer")

    search_res = database.similarity_search_with_score(query, k = 3)
    sim1, sim2, sim3 = [round(res[1], 5) for res in search_res]
    
    result = qa(query)
    
    # 데이터 관리 DB 입력
    hist = History(query=query, sim1=sim1, sim2=sim2, sim3=sim3, answer=result['answer'])
    hist.save()
    
    request.session['chat_history'] = [{'human' : hm.content, 'ai' : am.content} 
                                    for hm, am in memory.load_memory_variables({})['chat_history']]
    
    context = {'question': query, 'result': result["answer"]}
    return render(request, 'selfchatgpt/result.html', context) 