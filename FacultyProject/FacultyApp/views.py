from django.shortcuts import render

from .models import *

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


from django.contrib import messages

# Create your views here.




# home page logic  ****************************************************************************************
def home(request):
    return render(request, 'index.html')


# Register page logic ****************************************************************************************

def register(request):
    return render(request, 'register.html')

def insertdata(request):
    if request.method == 'POST':
       
        fId = request.POST.get('fid')
        fName = request.POST.get('fname')
        fDept = request.POST.get('fdept')
        fSal = request.POST.get('fsal')
        
        
        foundData=Faculty.objects.filter(fId=fId)
        
        if foundData.exists():
            msg = "Id Already Exist in DataBase !!!"
            return render(request, 'fail.html', {'msg': msg, 'Exception':Exception})
        
        else:
            faculty = Faculty(fId=fId, fName=fName.title(), fDept=fDept.title(), fSal=fSal)
        
            try:
            
                faculty.save()
            
                msg = "Data Saved Successfully ..."
                return render(request, 'success.html', {'msg': msg})
            
            except Exception :
                msg = "Data not Saved !!!!"
                return render(request, 'fail.html', {'msg': msg, 'Exception':Exception})
            
    

    return render(request, 'register.html')

# Display page logic ****************************************************************************************


def display(request):
    data=Faculty.objects.all()
    
    return render(request, 'display.html', {'data':data})



def searchdata(request):
    
    option=request.POST.get('flopt')
    datainp = request.POST.get('data')
    
    # this is for balnk search box
    if (not option or not datainp):
        data=Faculty.objects.all()
        messages.error(request, "Select category and enter valid data !!!!")
        return render(request, 'display.html', {'data':data})

    else:
        try:
            # this is for searching the data for id only
            if option=='None' and datainp:
                data=Faculty.objects.all()
                messages.error(request, "Select category and enter valid data !!!!")
                return render(request, 'display.html', {'data':data})
            
            # this is for searching the data for id only
            if option=='fId' and datainp:
                searchData = Faculty.objects.filter(fId=datainp)
                if searchData.exists():
                    return render(request, 'display.html', {'searchData':searchData})
                else:
                    msg = "Data is not present in the database."
                    return render(request, 'fail.html', {'msg': msg})
            
            # this is for searching the data for Name only only
            elif option == 'fName' and datainp:
                searchData = Faculty.objects.filter(fName__iexact=str(datainp))
                if searchData.exists():
                    print("Data found!")
                    return render(request, 'display.html', {'searchData': searchData})
                else:
                    print("No data found")
                    msg = "Data is not present in the database."
                    return render(request, 'fail.html', {'msg': msg})
                
            #search by department *************************************  
            elif option == 'fDept' and datainp:
                searchData = Faculty.objects.filter(fDept__iexact=str(datainp))
                if searchData.exists():
                    print("Data found!")
                    return render(request, 'display.html', {'searchData': searchData})
                else:
                    print("No data found")
                    msg = "Data is not present in the database."
                    return render(request, 'fail.html', {'msg': msg})

                
            #search by salary ***********************************************
            elif option=='fSal' and datainp:
                searchData = Faculty.objects.filter(fSal=datainp)
                if searchData.exists():
                    return render(request, 'display.html', {'searchData':searchData})
                else:
                    msg = "Data is not present in the database."
                    return render(request, 'fail.html', {'msg': msg})
        
        except Exception:
            msg = Exception
            return render(request, 'fail.html', {'msg': msg}) 



# Delete Page logic ****************************************************************************************

def delete(request):
    
    return render(request, 'delete.html')
 
def deletedata(request):
    
    data=request.POST.get('fid')
    
    try:
        
        product = Faculty.objects.filter(fId=data)
        
        if product.exists():
            product.delete()  
            
            msg="Data Deleted Successfully ..."
            return render(request, 'success.html', {'msg':msg})
        else:
            msg = "Data is not present in the database."
            return render(request, 'fail.html', {'msg': msg})
    
    except Exception:
        msg = Exception
        return render(request, 'delete.html', {'msg': msg})
    
    
    
    
    
# updata page logic ****************************************************************************************
    
    
def update(request):
    return render(request, 'update.html')



def updatedate(request):
    
    fId = request.POST.get('fid')
    fName = request.POST.get('fname')
    fDept = request.POST.get('fdept')
    fSal = request.POST.get('fsal')
    
    print(fDept)

    try:
        data = Faculty.objects.filter(fId=fId).get()
        print("**********************", data)
        
    except Faculty.DoesNotExist:
        msg="Faculty Id is not present in the DATABASE !!!"
        return render(request, 'fail.html', {'msg':msg})
    if fName:
        data.fName = fName.title()
    if fDept !='None' :
        data.fDept = fDept.title()
    if fSal:
        data.fSal = fSal
    data.save()
    
    msg="Data Updated Successfully ......"
    return render(request, 'success.html', {'msg':msg})



# print in pdf format 

def printpdf(request):
    
        searchData=Faculty.objects.all()

        # Render the data to an HTML template first
        template_path = 'pdf.html'  # Create this template
        context = {'searchData': searchData}  # Pass search data to the template

        # Convert the HTML to PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Faculty Data.pdf"'

        # Render the HTML
        html = render_to_string(template_path, context)

        # Create the PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Return the PDF if generation is successful
        if pisa_status.err:
            return HttpResponse("Error: Unable to generate PDF", status=500)
        return response






    

