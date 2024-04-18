from django.shortcuts import render
from django.http import HttpResponse
from product import Product
import pandas as pd
from io import BytesIO
import time

def index(request):
    return render(request, 'scrap.html')

def scrape_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name', '')
        if product_name == '':
            return HttpResponse("Please enter a valid product name")
        product = Product(product_name)
        product_details = product.get_product_details()
        if product_details["data"]:
            # Prepare the data for export
            data = product_details["data"]
            df = pd.DataFrame(data, index=range(len(data)))  # Specify index explicitly
            # Create an in-memory Excel file
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            # Set response headers to force file download
            response = HttpResponse(excel_file.getvalue(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=' + product_name + '_' + str(int(time.time())) + '.xlsx'
            response['Content-Length'] = len(excel_file.getvalue())
            return response
        else:
            return HttpResponse("Failed to fetch product details")
    else:
        return HttpResponse("Method not allowed")
