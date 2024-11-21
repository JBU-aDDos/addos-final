from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailForm
from pathlib import Path
from django.conf import settings

# 이메일 전송에 사용될 상수 정의
SUBJECT = "Thank you for your subscription"
MESSAGE = "HOW To USE THIS SCRIPT \n addos_config.sh [your mail]"
SENDER_EMAIL = 'aDDOSalarm@gmail.com'
SCRIPT_FILENAME = 'addos_config.sh'

def create_email(recipient, subject, message, sender):
    email = EmailMessage(subject, message, sender, [recipient])
    script_path = Path(settings.BASE_DIR) / 'home' / 'scripts' / SCRIPT_FILENAME
    email.attach(SCRIPT_FILENAME, script_path.read_bytes(), 'application/x-sh')
    return email

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            
            try:
                email = create_email(recipient, SUBJECT, MESSAGE, SENDER_EMAIL)
                email.send()
                
                messages.success(request, '이메일이 성공적으로 전송되었습니다.')
                form = EmailForm()  # 폼 초기화
            except Exception as e:
                messages.error(request, f'이메일 전송 중 오류가 발생했습니다: {str(e)}')
    else:
        # GET 요청 시 빈 폼 생성
        form = EmailForm()
    
    return render(request, 'home/about.html', {'form': form})

def index(request):
    return render(request, 'home/index.html')