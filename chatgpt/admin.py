from django.contrib import admin
from django.urls import path
from . import models
from .models import QaList
from django.shortcuts import redirect, render
from chatgpt.forms import CSVUploadForm
import sqlite3
import csv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)


# Register your models here.
@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "query", "date"]
    list_display_links = ["id", "query", "date"]
    list_filter = ["date"]


@admin.register(models.QaList)
class QA_ListAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "qa"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-csv/",
                self.admin_site.admin_view(self.upload_csv),
                name="upload_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        form = CSVUploadForm()
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8").splitlines()
                reader = csv.reader(decoded_file)
                cnt = 0
                for row in reader:
                    type, qa = row
                    self.message_user(request, qa)
                    self.message_user(
                        request, database.similarity_search_with_score(qa, 3)
                    )
                    if qa is None:
                        continue
                    score = database.similarity_search_with_score(qa, 1)[0][1]
                    self.message_user(request, score)
                    if score > 0.2:
                        # 크로마db 저장
                        doc = [Document(page_content=qa)]
                        database.add_documents(doc)
                        # sqlite db 저장
                        QaList.objects.create(type=type, qa=qa)
                        cnt += 1

                self.message_user(request, f"{cnt}건의 문서가 저장되었습니다")
                return redirect("..")

        return render(request, "admin/upload_csv.html", {"form": form})
