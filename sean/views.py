from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os #python 모듈을 불러옴. operative system에서 파일을 읽기 위함.

class ReactAppView(View): #이는 View에서 확장된것 

    def get(self, request): #request를 받을 때마다 파일을 열려고 한다.
        try :
            with open(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')) as file: #sean/frontend/build/index.html 파일을 찾는다.
                return HttpResponse(file.read()) # 응답은 해당 파일의 내용

        except: # 해당 파일을 찾지 못하면 실행
            return HttpResponse(
                """
                index.html not found! build your React app!!
                """,
                status=501,
        )