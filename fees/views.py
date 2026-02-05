from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum

from .models import Fee
from .forms import FeeForm

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

import openpyxl


# ================================
# Fee List (Isolated)
# ================================
@login_required
def fee_list(request):

    fees = Fee.objects.filter(
        teacher=request.user.teacher
    ).select_related("student").order_by("-id")

    return render(
        request,
        "fees/fee_list.html",
        {"fees": fees}
    )


# ================================
# Add Fee (Auto Assign Teacher)
# ================================
@login_required
def fee_create(request):

    if request.method == "POST":

        form = FeeForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            fee = form.save(commit=False)
            fee.teacher = request.user.teacher
            fee.save()

            return redirect("fees:list")

    else:

        form = FeeForm(
            user=request.user
        )

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form,
            "title": "Add Fee"
        }
    )


# ================================
# PDF Receipt (Secure)
# ================================
@login_required
def fee_receipt(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk,
        teacher=request.user.teacher   # SECURITY
    )

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4


    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(
        width / 2,
        height - 50,
        "Tuition Fee Receipt"
    )


    # Line
    p.line(50, height - 70, width - 50, height - 70)


    # Basic Info
    p.setFont("Helvetica", 11)

    y = height - 110

    p.drawString(50, y, f"Receipt No: {fee.receipt_no}")
    p.drawString(350, y, f"Date: {fee.paid_on}")

    y -= 25

    p.drawString(50, y, f"Student Name: {fee.student.name}")
    y -= 20

    p.drawString(50, y, f"Phone: {fee.student.phone}")
    y -= 20


    p.drawString(
        50,
        y,
        f"Month: {fee.get_month_display()} {fee.year}"
    )
    y -= 20


    p.drawString(
        50,
        y,
        f"Payment Mode: {fee.payment_mode.upper()}"
    )
    y -= 20


    # Amount Box
    p.rect(50, y - 40, width - 100, 50)

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        70,
        y - 20,
        f"Amount Paid: ₹ {fee.amount}"
    )
    
    # Signature
    y -= 90
    p.setFont("Helvetica", 11)
    p.drawString(50, y, "Authorized Signature:")
    p.line(180, y - 2, 350, y - 2)

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(
        width / 2,
        50,
        "Thank you for your payment"
    )

    # Finish
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer,content_type="application/pdf")
    response["Content-Disposition"] = f'filename="receipt_{fee.receipt_no}.pdf"'
    return response

@login_required
def monthly_report(request):
    month = request.GET.get("month")
    year = request.GET.get("year")
    fees = Fee.objects.filter(
        teacher=request.user.teacher
    )
    if month and month != "None":
        fees = fees.filter(month=month)
    if year and year != "None":
        try:
            year = int(year)
            fees = fees.filter(year=year)
        except ValueError:
            pass
    total = fees.aggregate(total=Sum("amount"))["total"] or 0
    context = {
        "fees": fees,
        "total": total,
        "month": month,
        "year": year,
    }
    return render(
        request,
        "fees/monthly_report.html",
        context
    )

@login_required
def export_excel(request):

    month = request.GET.get("month")
    year = request.GET.get("year")
    fees = Fee.objects.filter(
        teacher=request.user.teacher
    )
    if month and month != "None":
        fees = fees.filter(month=month)
    if year and year != "None":
        try:
            year = int(year)
            fees = fees.filter(year=year)
        except ValueError:
            pass
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fee Report"
    # Header
    ws.append([
        "Student",
        "Month",
        "Year",
        "Amount",
        "Mode",
        "Receipt No"
    ])
    # Data
    for f in fees:
        ws.append([
            f.student.name,
            f.get_month_display(),
            f.year,
            float(f.amount),
            f.payment_mode,
            f.receipt_no,
        ])
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response[
        "Content-Disposition"
    ] = 'attachment; filename="fee_report.xlsx"'
    wb.save(response)

    return response