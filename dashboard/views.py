from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student

# Create your views here.
@login_required
def dashboard(request):
    total_students = Student.objects.filter(teacher=request.user.teacher).count()
    return render(request,"dashboard.html",{"total_students": total_students})