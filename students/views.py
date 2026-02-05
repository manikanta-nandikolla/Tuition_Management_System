from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def student_list(request):
    students = Student.objects.filter(teacher=request.user.teacher).order_by('-id')
    return render(request,'students/student_list.html',{'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user.teacher
            student.save()
            return redirect('students:list')
    else:
        form = StudentForm()
    return render(request,'students/student_form.html',{'form': form,'title': 'Add Student'})

@login_required
def student_update(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user.teacher
            student.save()
            return redirect('students:list')

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {'form': form, 'title': 'Edit Student'}
    )

@login_required
def student_delete(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        return redirect('students:list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'student': student}
    )