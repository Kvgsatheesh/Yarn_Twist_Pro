from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from django.db.models import Sum
from django.db.models import Q
from datetime import date,timedelta
from django.contrib import messages
from .forms import *


# Create your views here.

def homeview(request):
    current_year = date.today().year
    form=dateform()
    From=date(current_year, 1, 1)
    To=date.today()
    if request.method=='POST':
        form=dateform(request.POST)
       
        if form.is_valid():
           
            From=form.cleaned_data['From']
            To=form.cleaned_data['To']

    
    company=Company.objects.all()


    custom=Stocks.objects.values('Company').filter(~Q(Inward=0)).filter(Date__range=(From,To)).annotate(
         inward=Sum('Inward'),
         amount=Sum('Amount'),

    ).exclude(inward=0,amount=0)

    total=Stocks.objects.filter(~Q(Inward=0)).filter(Date__range=(From,To)).aggregate(
         bag=Sum('Inward'),
         amount=Sum('Amount')
    )


    exp=Expense.objects.filter(Date__range=(From,To)).aggregate(
         expense=Sum('Amount')
    )
    if(exp['expense'] == None):
         exp['expense']=0
      
    anb=Others.objects.filter(Date__range=(From,To)).aggregate(
         bonus=Sum('Bonus') )
    
    if(anb['bonus'] == None):
         anb['bonus']=0
    
    ad=Others.objects.filter(Date__range=(From,To)).aggregate(
         advance=Sum('Advance') )
    
    if(ad['advance'] == None):
         ad['advance']=0
    
    salary=Production.objects.filter(Date__range=(From,To)).aggregate(
         tot_salary=Sum('Total_salary')
    )

    if(salary['tot_salary'] == None):
         salary['tot_salary']=0

    otherincome=Otherincome.objects.filter(Date__range=(From,To)).aggregate(
         tot_income=Sum('Paper_cone') + Sum('Bag')
    )

    if(otherincome['tot_income'] == None):
         otherincome['tot_income']=0


    try:
               salary['tot_salary']=float(salary['tot_salary']) + int(anb['bonus'] )+ int(ad['advance'])

               net=( float(total['amount']) + int(otherincome['tot_income']) ) - ( float(salary['tot_salary']) + float(exp['expense']) )
               
    except:
            net=0

    context={
         'exp':exp,
         'total':total,
         'salary':salary,
         'company':company,
         'custom':custom,
         'net':net,
         'From':From,
         'To':To,
         'form':form,
         'otherincome':otherincome

    }
   
     
    return render(request,'myapp/home.html',context)


def addcolour(request):
    form=Addcolourform()
    if request.method=='POST':
         form=Addcolourform(request.POST)
         if form.is_valid():
            
            form.save()
            return redirect('myapp:home')
    return render(request,'myapp/additem.html',{'form':form})


def updatecolour(request):
     q=request.GET.get('q')
     colour=Colour.objects.get(id=q)
     form=Addcolourform(instance=colour)
     if request.method == 'POST':
          form=Addcolourform(request.POST,instance=colour)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def addcompany(request):
    form=Addcompanyform()
    if request.method=='POST':
        form=Addcompanyform(request.POST)
        if form.is_valid():
            
            form.save()

            return redirect('myapp:home')
    return render(request,'myapp/additem.html',{'form':form})


def updatecompany(request):
     q=request.GET.get('q')
     company=Company.objects.get(id=q)
     form=Addcompanyform(instance=company)
     if request.method == 'POST':
          form=Addcompanyform(request.POST,instance=company)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def addcount(request):
    form=addcountform()
    if request.method=='POST':
        form=addcountform(request.POST)
        if form.is_valid():
            
            form.save()

            return redirect('myapp:home')
    return render(request,'myapp/additem.html',{'form':form})


def updatecount(request):
     q=request.GET.get('q')
     count=Count.objects.get(id=q)
     form=addcountform(instance=count)
     if request.method == 'POST':
          form=addcountform(request.POST,instance=count)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def addtp(request):
    form=addtpform()
    if request.method=='POST':
        form=addtpform(request.POST)
        if form.is_valid():
            
            form.save()

            return redirect('myapp:home')
    return render(request,'myapp/additem.html',{'form':form})


def updatetp(request):
     q=request.GET.get('q')
     tp=Tp.objects.get(id=q)
     form=addtpform(instance=tp)
     if request.method == 'POST':
          form=addtpform(request.POST,instance=tp)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def addstaff(request):
     form=addstaffform()
     if request.method=='POST':
        form=addstaffform(request.POST)
        if form.is_valid():
            
            form.save()

            return redirect('myapp:home')
     return render(request,'myapp/additem.html',{'form':form})


def updatestaff(request):
     q=request.GET.get('q')
     staff=Staffprofile.objects.get(id=q)
     form=addstaffform(instance=staff)
     if request.method == 'POST':
          form=addstaffform(request.POST,instance=staff)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def addprice(request):
     form=addpriceform()
     if request.method == "POST":
          form=addpriceform(request.POST)
          if form.is_valid :
               form.save()
               return redirect('myapp:home')

     return render(request,'myapp/additem.html',{'form':form})


def updateprice(request):
     q=request.GET.get('q')
     price=Price.objects.get(id=q)
     form=addpriceform(instance=price)
     if request.method == 'POST':
          form=addpriceform(request.POST,instance=price)
          if form.is_valid :
               form.save()
               return redirect('myapp:edit')
     return render(request,'myapp/additem.html',{'form':form})


def edit(request):
     colour=Colour.objects.all()
     company=Company.objects.all()
     staff=Staffprofile.objects.all()
     tp=Tp.objects.all()
     count=Count.objects.all()
     price=Price.objects.all()
     context = {
          'colour':colour,
          'company':company,
          'staff':staff,
          'tp':tp,
          'count':count,
          'price':price,
     }
     return render(request,'myapp/edit.html',context)
     
     
def inward(request):
    pro=Production.objects.all()
    form=addinventryform()
    if request.method=='POST':
        form=addinventryform(request.POST)
        if form.is_valid():
            Com_id=request.POST['Company']
            inward=float(request.POST['Inward'])
           
            count_id=request.POST['Count']
            tp_id=request.POST['Tp']
           
            if( inward  > 0):
                beforesave=form.save(commit=False)
                price=Price.objects.filter(
                     Company_id=Com_id,
                     Count_id=count_id,
                     Tp_id=tp_id,
                     ).aggregate(
                          bagprice=Sum('Per_bag')
                          
                     )
               
                beforesave.Amount=(float(price['bagprice']) * inward)
               
                beforesave.save()
                
                pro.create(
                     Stocks_id=beforesave.id,
                     Company_id= request.POST['Company'],
                     Colour_id=request.POST['Colour'],
                     Count_id= request.POST['Count'],
                     Tp_id= request.POST['Tp'],
                     Inward=int(request.POST['Inward']),
                     )
                
                redirect_url=reverse('myapp:statement') + f'?q={Com_id}'
                return redirect(redirect_url)
            else:
                 messages.error(request,'Enter valid data')


            
        
    return render(request,'myapp/additem.html',{'form':form})


def updateinward(request,id):
     pid=int(id)
    
     pro=Production.objects.get(Stocks_id=pid)
     
     item=Stocks.objects.get(id=id)
     company_id=item.Company.id
     colour_id=item.Colour.id
     form=addinventryform(instance=item)
     if request.method=='POST':
        form=addinventryform(request.POST,instance=item)

        if form.is_valid():
                out=request.POST['Inward']
                if(int(out) < 0):
                      messages.error(request,'enter valid data')
                      return render(request,'myapp/additem.html',{'form':form})
                     
                beforeupdate=form.save(commit=False)

                currentin=Production.objects.exclude(Stocks_id=id).filter(Company_id=company_id).filter(Colour_id=colour_id).aggregate(Sum('Inward'))
                
                totalin=(int(currentin['Inward__sum']) + int( beforeupdate.Inward))

                Totalout=Production.objects.filter(Company_id=company_id).filter(Colour_id=colour_id).aggregate(Sum('Cheese_bag'))


                if((int(Totalout['Cheese_bag__sum'])) <= totalin):
                    

                    price=Price.objects.filter(
                     Company_id=request.POST['Company'],
                     Count_id=request.POST['Count'],
                     Tp_id=request.POST['Tp'],
                     ).aggregate(
                          bagprice=Sum('Per_bag')
                          
                     )
                    beforeupdate.Amount=(
                         float(price['bagprice']) * 
                         float(int(request.POST['Inward'])))

                    beforeupdate.save()
               


                    pro.Company_id= request.POST['Company']
                    pro.Colour_id=request.POST['Colour']
                    pro.Count_id= request.POST['Count']
                    pro.Tp_id= request.POST['Tp']
                    pro.Inward=int(request.POST['Inward'])
                   
                    pro.save()
                    
                    redirect_url=reverse('myapp:inventry') + f'?q={company_id}'
        
                    return redirect(redirect_url)
                else:
                    messages.error(request,'already processed')


     return render(request,'myapp/additem.html',{'form':form})


def returnview(request):
     pro=Production.objects.all()
     stock=Stocks.objects.all()
     colour=Colour.objects.all()
     company=Company.objects.all()
     tp=Tp.objects.all()
     count=Count.objects.all()
    

    
     if request.method=='POST':
            
            
            currentin=Production.objects.filter(
                 Company_id=request.POST['Company'],
                 Colour_id=request.POST['Colour'],
                 Count_id=request.POST['Count'],
                 Tp_id=request.POST['TP'],
                 ).aggregate(Sum('Inward'))
                
            totalin=(int(currentin['Inward__sum']) + int( request.POST['return']))

            Totalout=Production.objects.filter(
                 Company_id=request.POST['Company'],
                 Colour_id=request.POST['Colour'],
                 Count_id=request.POST['Count'],
                 Tp_id=request.POST['TP'],
                 ).aggregate(Sum('Cheese_bag'))
            
            com=int(request.POST['Company'])

            if((int(Totalout['Cheese_bag__sum'])) <= totalin):
                   
                price=Price.objects.filter(
                     Company_id= request.POST['Company'],
                     
                     Count_id= request.POST['Count'],
                     Tp_id= request.POST['TP'],
                     
                ).aggregate( bagprice=Sum('Per_bag'))  

                stock.create(
                     Company_id= request.POST['Company'],
                     Colour_id=request.POST['Colour'],
                     Count_id= request.POST['Count'],
                     Tp_id= request.POST['TP'],
                     Inward=(int(request.POST['return']) * -1),
                     Amount=(float(price['bagprice']) * float((int(request.POST['return']) * -1)))
                     )
            
                pro.create(
                     
                     Company_id= request.POST['Company'],
                     Colour_id=request.POST['Colour'],
                     Count_id= request.POST['Count'],
                     Tp_id= request.POST['TP'],
                     Inward=(int(request.POST['return']) * -1),
                     )
            
                redirect_url=reverse('myapp:statement') + f'?q={com}'
                return redirect(redirect_url)
            else:
                    messages.error(request,'already processed')
        
     return render(request,'myapp/return.html',{'colour':colour,'company':company,
                                                'TP':tp,'count':count})


def Outward(request):
    pro=Production.objects.all()
    form=outwardform()
    if request.method=='POST':
        form=outwardform(request.POST)
       
        if form.is_valid():
             out=request.POST['Outward']
             if(int(out) <= 0):
                  messages.error(request,'Enter valid data')
                  return render(request,'myapp/additem.html',{'form':form})
                    

             Com_id=request.POST['Company']
             Col_id=request.POST['Colour']
             count_id= request.POST['Count'] 
             tp_id=request.POST['Tp'] 
                
             stocks=Production.objects.filter(
                  Company_id=Com_id,
                  Colour_id=Col_id,
                  Count_id=count_id,
                  Tp_id=tp_id,
                  
                  ).aggregate(st=(Sum('Doubled_bag')))
            
        
        
        if(int(stocks['st']) >= int(out)):
                avaliable=int(stocks['st'])
                instance=form.save()
                pro.create(
                     Stocks_id=instance.id,
                     Company_id= request.POST['Company'],
                     Colour_id=request.POST['Colour'],
                     Count_id= request.POST['Count'],
                     Tp_id= request.POST['Tp'],
                     Outward=int(request.POST['Outward']),
                     )
                
                redirect_url=reverse('myapp:statement') + f'?q={Com_id}'
                return redirect(redirect_url)
           
        else:
            avaliable=int(stocks['st'])
            if(avaliable==0):
                    messages.error(request,'Goods are not avaliable for delivery')


            return render(request,'myapp/additem.html',{'form':form,'avaliable':avaliable})
          
            
           
    return render(request,'myapp/additem.html',{'form':form})


def updateoutward(request,id):
     pro=Production.objects.get(Stocks_id=id)
     item=Stocks.objects.get(id=id)
     company_id=item.Company.id
     colour_id=item.Colour.id
     form=outwardform(instance=item)
     if request.method=='POST':
        form=outwardform(request.POST,instance=item)
        if form.is_valid():
               
                beforeupdate=form.save(commit=False)
                if(int( beforeupdate.Outward) <=0):
                      return render(request,'myapp/additem.html',{'form':form})

                currentout=Production.objects.exclude(Stocks_id=id).filter(Company_id=company_id).filter(Colour_id=colour_id).aggregate(Sum('Outward'))
                
                totalout=(int(currentout['Outward__sum']) + int( beforeupdate.Outward))

                Totaldouble=Production.objects.filter(Company_id=company_id).filter(Colour_id=colour_id).aggregate(Sum('Doubled_bag'))


                if((int(Totaldouble['Doubled_bag__sum'])) >= totalout):
                    beforeupdate.save()
                    pro.Company_id= request.POST['Company']
                    pro.Colour_id=request.POST['Colour']
                    pro.Count_id= request.POST['Count']
                    pro.Tp_id= request.POST['Tp']
                    pro.Outward=int(request.POST['Outward'])
                    pro.save()
                    
                    
                    redirect_url=reverse('myapp:inventry') + f'?q={company_id}'
        
                    return redirect(redirect_url)
                else:
                    messages.error(request,'not available')


     return render(request,'myapp/additem.html',{'form':form})


def inventory(request):
     page='normal'
     q=request.GET.get('q')
     colour=Colour.objects.all()
 
     company=Company.objects.all()
     tp=Tp.objects.all()
     count=Count.objects.all()
     
     list=Stocks.objects.filter(Company_id=q).exclude(Bag__gt=0).order_by('-Date')

     #avoid negative
     inward=Stocks.objects.values('Colour').filter(Company_id=q).exclude(Bag__gt=0).annotate(inw=Sum('Inward')- Sum('Bag'))
     outward=Stocks.objects.values('Colour').filter(Company_id=q).exclude(Bag__gt=0).annotate(out=Sum('Outward')- Sum('Bag'))

     stock=Stocks.objects.values('Colour').filter(Company_id=q).exclude(Bag__gt=0).annotate(total=Sum('Inward') - Sum('Outward') )
    

     form=dateform
     if request.method=='POST':
        form=dateform(request.POST)
       
    
        if form.is_valid():
           
            page='customdate'
            From=request.POST['From']
            To=request.POST['To']
            selcolour=request.POST['chooseColour']
            seltp=request.POST['TP']
            selcount=request.POST['count']
         
            
            if(selcolour=='all' and selcount=='all' and seltp=='all'):

                custom=Stocks.objects.filter(Company_id=q).exclude(Bag__gt=0).filter(Date__range=(From,To)).order_by('-Date')

                ti=custom.aggregate(i=Sum('Inward'))
                totalin=ti['i']

                to=custom.aggregate(o=Sum('Outward'))
                toatlout=to['o']
            else:

                filter_conditions={}

                if (selcount != 'all'):
                        filter_conditions['Count_id'] = int(selcount)

                if (selcolour != 'all'):
                        filter_conditions['Colour_id'] = int(selcolour)

                if (seltp != 'all'):
                        filter_conditions['Tp_id'] = int(seltp)

                        

                custom=Stocks.objects.filter(Company_id=q).exclude(Bag__gt=0).filter(Date__range=(From,To)).filter(**filter_conditions).order_by('-Date')
                
                ti=custom.aggregate(i=Sum('Inward'))
                totalin=ti['i']

                to=custom.aggregate(o=Sum('Outward'))
                toatlout=to['o']

            return render(request,'myapp/inventory.html',{'list':list,'company':company,'form':form,'custom':custom,'page':page,'from':From,'to':To,'totalin':totalin,'toatlout':toatlout,'colour':colour,'inward':inward,'outward':outward,'stock':stock,'count':count,'TP':tp})
           
        
     return render(request,'myapp/inventory.html',{'list':list,'company':company,'form':form,'page':page,'colour':colour,'inward':inward,'outward':outward,'stock':stock,'count':count,'TP':tp})


def updateinventory(request,id):
    item=Stocks.objects.get(id=id)
    company_id=item.Company.id
    form=updateform(instance=item)
    if request.method=='POST':
        form=updateform(request.POST,instance=item)
        if form.is_valid():
            form.save()
            redirect_url=reverse('myapp:inventory') + f'?q={company_id}'
       
            return redirect(redirect_url)
        
    return render(request,'myapp/additem.html',{'form':form})


def deleteinventory(request,id):
    page='inventry'
    item=Stocks.objects.get(id=id)
    company_id=item.Company.id
    pro=Production.objects.get(Stocks_id=id)
   
    if request.method=='POST':
        item.delete()
        pro.delete()
        redirect_url=reverse('myapp:inventory') + f'?q={company_id}'
       
        return redirect(redirect_url)
    return render(request,'myapp/deleteinventory.html',{'form':item,'page':page})


def statementview(request):
        page=''
        q=request.GET.get('q')
        company=Company.objects.all()
        tp=Tp.objects.all()
        count=Count.objects.all()
        col=Colour.objects.all()
        list=Stocks.objects.filter(Company_id=q)
        comname=Company.objects.get(id=q)

    #total summary for a company
        item=Stocks.objects.filter(Company_id=q)
        totalstocks=item.aggregate(a=Sum('Inward')-Sum('Outward'))
        
        totalin=item.aggregate(tin=Sum('Inward')- Sum('Bag'))
        
        totalout=item.aggregate(tout=Sum('Outward')- Sum('Bag'))
        totalamount=item.aggregate(t=Sum('Amount'))
        
        #to avoid error in abs fn for none
        if((totalout['tout']) != None):
            abstotalout=abs(totalout['tout'])
        else:
             abstotalout=''
        

    # summary for a company group by colour
        result = Stocks.objects.values('Colour').filter(Company_id=q).annotate(
         total_in=Sum('Inward')-Sum('Bag'),
        total_out=Sum('Outward')-Sum('Bag'),
        total_stock=Sum('Inward')-Sum('Outward'),
        total_amount=Sum('Amount')
         ).exclude(total_in=0, total_out=0, total_stock=0)
      

        if request.method=='POST':
                page='custom'
                selcolour=request.POST['chooseColour']
                seltp=request.POST['TP']
                selcount=request.POST['count']
            
                
                if(selcolour=='all' and selcount=='all' and seltp=='all'):

                    selcolour=='All' 
                    selcount=='All'
                    seltp=='All'

                else:

                    filter_conditions={}

                    if (selcount != 'all'):
                            filter_conditions['Count_id'] = int(selcount)

                    if (selcolour != 'all'):
                            filter_conditions['Colour_id'] = int(selcolour)

                    if (seltp != 'all'):
                            filter_conditions['Tp_id'] = int(seltp)

                            
                    totalstocks=item.filter(**filter_conditions).aggregate(a=Sum('Inward')-Sum('Outward'))
        
                    totalin=item.filter(**filter_conditions).aggregate(tin=Sum('Inward')- Sum('Bag'))
                    
                    totalout=item.filter(**filter_conditions).aggregate(tout=Sum('Outward')- Sum('Bag'))

                    totalamount=item.filter(**filter_conditions).aggregate(t=Sum('Amount'))

                    print(totalamount['t'])
                    print(totalin['tin'])
                    

                    filter_withoutcolour={}

                    if (selcount != 'all'):
                             filter_withoutcolour['Count_id'] = int(selcount)

                    if (seltp != 'all'):
                         filter_withoutcolour['Tp_id'] = int(seltp)


                    result = Stocks.objects.filter(**filter_withoutcolour).values('Colour').filter(Company_id=q).annotate(
                                 total_in=Sum('Inward')-Sum('Bag'),
                                 total_out=Sum('Outward')-Sum('Bag'),
                                 total_stock=Sum('Inward')-Sum('Outward'),
                                 total_amount=Sum('Amount')
                                 ).exclude(total_in=0, total_out=0, total_stock=0)
                    print(result)
                    
                   
                    if(selcolour != 'all'):
                        selcolour=col.get(id=selcolour)
                    else:
                         selcolour='All'

                    if(seltp != 'all'):
                        seltp=tp.get(id=seltp)
                    else:
                         seltp='All'

                    if(selcount != 'all'):
                       selcount=count.get(id=selcount)
                    else:
                         selcount='All'
                 
                return render(request,'myapp/statement.html',{'col':col,'colour':col,'TP':tp, 'count':count,'company':company,'selcolour':selcolour,'page':page,'result':result,
               'seltp':seltp,'selcount':selcount, 'comname':comname,'totalstocks':totalstocks,'list':list,'totalin':totalin,'totalout':totalout,' abstotalout': abstotalout,'totalamount':totalamount})
        
        return render(request,'myapp/statement.html',{'col':col,'colour':col,'TP':tp,'count':count,'company':company, 'page':page,'result':result,  'comname':comname,'totalstocks':totalstocks,'list':list,'totalin':totalin,'totalout':totalout, 'abstotalout': abstotalout,'totalamount':totalamount,})       


def paymentview(request):
    
    form=paymentform()
    com=Company.objects.all()
    if request.method=='POST':
        form=paymentform(request.POST)
        if form.is_valid():
            
            temp=form.save(commit=False)
            
            check=Stocks.objects.filter(Company_id=temp.Company).filter(Colour_id=temp.Colour).aggregate(che=Sum('Inward'))

            pay=Stocks.objects.filter(Company_id=temp.Company).filter(Colour_id=temp.Colour).aggregate(pa=Sum('Bag'))
          
            current=int(pay['pa']) +int( temp.Bag)
            if( int(check['che']) >=  current):
                temp.Amount=float(temp.Amount * (-1))
                temp.save()
                messages.error(request,'done')
            else:
                messages.error(request,'exceeds the inward')
           
    return render(request,'myapp/additem.html',{'form':form,'com':com})


def updatepayment(request,id):
     item=Stocks.objects.get(id=id)
     company_id=item.Company.id
     form=paymentform(instance=item)

     if request.method=='POST':
        form=paymentform(request.POST,instance=item)
        if form.is_valid():
            form.save()
            redirect_url=reverse('myapp:inventry') + f'?q={company_id}'
       
            return redirect(redirect_url)
        
     return render(request,'myapp/additem.html',{'form':form})


def paymentlist(request):
     page='normal'
     q=request.GET.get('q')
     colour=Colour.objects.all()
  
     company=Company.objects.all()
     
     list=Stocks.objects.filter(Company_id=q).filter(Bag__gt=0).order_by('-Date')

     #avoid negative
     inward=Stocks.objects.values('Colour').filter(Company_id=q).filter(Bag__gt=0).annotate(inw=Sum('Inward')- Sum('Bag'))
    #  outward=Payment.objects.values('Colour').filter(Company_id=q).filter(Bag__gt=0).annotate(out=Sum('Outward')- Sum('Bag'))

    #  stock=Payment.objects.values('Colour').filter(Company_id=q).filter(Bag__gt=0).annotate(total=Sum('Inward') - Sum('Outward') )
    

     form=dateform
     if request.method=='POST':
        form=dateform(request.POST)
       
    
        if form.is_valid():
           
            page='customdate'
            From=request.POST['From']
            To=request.POST['To']
            selcolour=request.POST['chooseColour']
            
            if(selcolour=='all'):

                custom=Stocks.objects.filter(Company_id=q).filter(Bag__gt=0).filter(Date__range=(From,To)).order_by('-Date')
                ti=custom.aggregate(i=Sum('Inward'))
                totalin=ti['i']

                to=custom.aggregate(o=Sum('Bag'))
                toatlout=to['o']
            else:
                 selcolour=int(selcolour)
                 custom=Stocks.objects.filter(Company_id=q).filter(Colour_id=selcolour).filter(Bag__gt=0).filter(Date__range=(From,To)).order_by('-Date')
                 ti=custom.aggregate(i=Sum('Inward'))
                 totalin=ti['i']

                 to=custom.aggregate(o=Sum('Bag'))
                 toatlout=to['o']


            return render(request,'myapp/paymentlist.html',{'list':list,'company':company,'form':form,'custom':custom,'page':page,'from':From,'to':To,'totalin':totalin,'toatlout':toatlout,'colour':colour,'inward':inward,})
           
        
     return render(request,'myapp/paymentlist.html',{'list':list,'company':company,'form':form,'page':page,'colour':colour,'inward':inward,})


def addproductionview(request):
    
     form=addproductionform()
     if(request.method=='POST'):
          form=addproductionform(request.POST)
          if (form.is_valid):
            beforesave=form.save(commit=False)
            total=Production.objects.filter(
                 Company_id=beforesave.Company,
                 Colour_id=beforesave.Colour,
                 Count_id=beforesave.Count,
                 Tp_id=beforesave.Tp,
            ).aggregate(
                 inw=Sum('Inward'),
                  cheese=Sum('Cheese_bag'),
                  double=Sum('Doubled_bag'),
                 )
            totalcheese=int(total['cheese']) + int(beforesave.Cheese_bag)
            totaldouble=int(total['double']) + int(beforesave.Doubled_bag)
           
 #pricing
            price=Price.objects.filter(
                 Company_id=beforesave.Company,
                
                 Count_id=beforesave.Count,
                 Tp_id=beforesave.Tp,
            ).aggregate(
                Tfo_price=Sum('Tfo_price'), 
                Cheese_price=Sum('Cheese_price'),
                Doubled_price=Sum('Doubled_price'),
            )  
            

            totaltfoprice=float(price['Tfo_price']) * float(beforesave.Tfo_shift) 
            totalcheeseprice= float(price['Cheese_price']) * float(beforesave.Cheese_bag)
            totaldoubleprice= float(price['Doubled_price']) * float(beforesave. Doubled_bag) 
            totalwasteprice=float(float(price['Cheese_price'])/62) * float(beforesave.Waste)   





            if(int(total['inw']) >= totalcheese):
                 if(int(total['cheese']) >= totaldouble):
                      beforesave.Total_salary=float(totaltfoprice + totalcheeseprice + totaldoubleprice + totalwasteprice)
                      beforesave.save()
                      
                      messages.error(request,'added successfully')
                      
                 else:
                    messages.error(request,'Error in double bag')
                    return render(request,'myapp/additem.html',{'form':form})
            else:
              messages.error(request,'error in cheese bag')
           
     return render(request,'myapp/additem.html',{'form':form})


def productionlistview(request):
     pro=Production.objects.exclude(Cheese_bag=0,Doubled_bag=0,Tfo_shift=0)
    
     return render(request,'myapp/productionlist.html',{'pro':pro})
     

def productioneditview(request):
    q=request.GET.get('q')
    pro=Production.objects.get(id=q)
    form=addproductionform(instance=pro)
    if request.method == "POST":
     form=addproductionform(request.POST,instance=pro)
     if (form.is_valid):
          beforesave=form.save(commit=False)
          total=Production.objects.exclude(id=q).filter(
                 Company_id=beforesave.Company,
                 Colour_id=beforesave.Colour,
                 Count_id=beforesave.Count,
                 Tp_id=beforesave.Tp,
            ).aggregate(
                 inw=Sum('Inward'),
                  cheese=Sum('Cheese_bag'),
                  double=Sum('Doubled_bag'),
                 )
          totalcheese=int(total['cheese']) + int(beforesave.Cheese_bag)
          totaldouble=int(total['double']) + int(beforesave.Doubled_bag)


          price=Price.objects.filter(
                 Company_id=beforesave.Company,
                
                 Count_id=beforesave.Count,
                 Tp_id=beforesave.Tp,
            ).aggregate(
                Tfo_price=Sum('Tfo_price'), 
                Cheese_price=Sum('Cheese_price'),
                Doubled_price=Sum('Doubled_price'),
            )  
            

          totaltfoprice=float(price['Tfo_price']) * float(beforesave.Tfo_shift) 
          totalcheeseprice= float(price['Cheese_price']) * float(beforesave.Cheese_bag)
          totaldoubleprice= float(price['Doubled_price']) * float(beforesave. Doubled_bag) 
          totalwasteprice=float(float(price['Cheese_price'])/62) * float(beforesave.Waste)   


           
          if(int(total['inw']) >= totalcheese):
                 if(int(total['cheese']) >= totaldouble):
                      beforesave.Total_salary=float(totaltfoprice + totalcheeseprice + totaldoubleprice + totalwasteprice)
                      beforesave.save()
                      messages.error(request,'added successfully')
                 else:
                    messages.error(request,'Error in double bag')
                    return render(request,'myapp/production.html',{'form':form})
          
          else:         
            messages.error(request,'error in cheese bag')
            return render(request,'myapp/additem.html',{'form':form})
      
    return render(request,'myapp/additem.html',{'form':form})


def productiondeleteview(request):
     page=''
     q=request.GET.get('q')
     pro=Production.objects.get(id=q)
     if (request.method=='POST'):
          pro.delete()
          return redirect('myapp:productionlist')
     return render(request,'myapp/deleteinventry.html',{'form':pro,'page':page})


def productionreportview(request):
    
    q=request.GET.get('q')
    count=Count.objects.all()
    tp=Tp.objects.all()

    colour=Colour.objects.all()
    company=Company.objects.all()
    com_id=company.get(id=q)
   
    report=Production.objects.filter(Company_id=q).values('Colour','Count','Tp').annotate(
         input=Sum('Inward'),
         cheese_bal=Sum('Cheese_bag')-Sum('Doubled_bag'),
         single_bal=Sum('Inward')-Sum('Cheese_bag'),
         double_bal=Sum('Doubled_bag')-Sum('Outward'),
         
    ).exclude(cheese_bal=0,single_bal=0,double_bal=0)
    
    context = {
         'count':count,
         'tp':tp,
        'report':report,
        'colour':colour,
        'company':company,
        'com_id':com_id,
       
        
    }

    return render(request,'myapp/productionreport.html', context)


#daily report and weekly report
def productionweeklyview(request):
     colour=Colour.objects.all()
     company=Company.objects.all()
     staff=Staffprofile.objects.all()
     count=Count.objects.all()
     tp=Tp.objects.all()
     form=dateform()

     today = date.today() 
     start_of_week = today - timedelta(days=today.weekday())

     salary_day=start_of_week + timedelta(days=6)
      
     if request.method=='POST':
          form=dateform(request.POST)
          if form.is_valid():

               start_of_week = form.cleaned_data['From']

               today = form.cleaned_data['To']
 
               salary_day=''
      #daily report
               dreport=Production.objects.values('Date','Company','Colour','Count','Tp').filter(Date__range=(start_of_week, today)).annotate(
               
               cheese_bal=Sum('Cheese_bag'),
               
               double_bal=Sum('Doubled_bag'),
                    
                    ).exclude(cheese_bal=0,double_bal=0)
          
      #weekly production with salary   
               total=Production.objects.filter(Date__range=(start_of_week, today)).aggregate(
               total_tfo_shift=Sum('Tfo_shift'),
               total_cheese=Sum('Cheese_bag'),
               
               total_double=Sum('Doubled_bag'),
               total_salary=Sum('Total_salary') 
               )
          

     #individual staff
               individualreport=Production.objects.values('Staff').filter(Date__range=(start_of_week, today)).annotate(
               tfo_shift=Sum('Tfo_shift'),
               cheese_bal=Sum('Cheese_bag'),
               
               double_bal=Sum('Doubled_bag'),
               total_salary=Sum('Total_salary') 
                    
          ).exclude(total_salary=0)
          
     
     else:
               
     #daily
               dreport=Production.objects.values('Date','Company','Colour','Count','Tp').filter(Date__range=(start_of_week, today)).annotate(
              
               cheese_bal=Sum('Cheese_bag'),
               
               double_bal=Sum('Doubled_bag'),
                    
          ).exclude(cheese_bal=0,double_bal=0)

          #weekly  production with salary  
               total=Production.objects.filter(Date__range=(start_of_week, today)).aggregate(
               total_tfo_shift=Sum('Tfo_shift'),
               total_cheese=Sum('Cheese_bag'),
               
               total_double=Sum('Doubled_bag'),
               total_salary=Sum('Total_salary') 
               )


          #individual salary
               individualreport=Production.objects.values('Staff').filter(Date__range=(start_of_week, today)).annotate(
               tfo_shift=Sum('Tfo_shift'),
               cheese_bal=Sum('Cheese_bag'),
               
               double_bal=Sum('Doubled_bag'),
               total_salary=Sum('Total_salary') 
                    
          ).exclude(total_salary=0)
               
               


     context={
         'dreport':dreport,
          'start_of_week': start_of_week,
          'today':today,
          'colour':colour,
          'count':count,
          'tp':tp,
        'company':company,
        'total':total,
        'individualreport':individualreport,
        'staff':staff,
        'salary_day':salary_day,
        'form':form,

         
    }
     
     return render(request,'myapp/dailyreport.html',context)


def addexpense(request):
     form=addexpenseform()
     if request.method == 'POST':
          form=addexpenseform(request.POST)
          if form.is_valid():
               if( int(request.POST['Amount']) > 0):

                    form.save()
                    return redirect('myapp:expenselist')
               messages.error(request,'Enter valid data')
               return render(request,'myapp/additem.html',{'form':form})
               
     return render(request,'myapp/additem.html',{'form':form})


def expenselist(request):
     current_year = date.today().year
     From=date(current_year, 1, 1)
     To=date.today()
     expense=Expense.objects.filter(Date__range=(From,To))
     amount=expense.aggregate(tot=Sum('Amount'))

     form=dateform()
     if request.method == 'POST':
          form=dateform(request.POST)
          if form.is_valid():
               From=request.POST['From']
               To=request.POST['To']
               
               expense=Expense.objects.filter(Date__range=(From,To))
               amount=expense.aggregate(Sum('Amount'))
               return render(request,'myapp/listexpense.html',{'expense':expense,'amount':amount,'form':form})


     return render(request,'myapp/listexpense.html',{'expense':expense,'amount':amount,'form':form})


def editexpense(request):
     q=request.GET.get('q')
     expense=Expense.objects.get(id=q)
     form=addexpenseform(instance=expense)
     if request.method == 'POST':
          form=addexpenseform(request.POST,instance=expense)
          if form.is_valid():
               if( int(request.POST['Amount']) > 0):
                    form.save()
                    return redirect('myapp:expenselist')
               messages.error(request,'Enter valid data')
               return render(request,'myapp/additem.html',{'form':form})
     return render(request,'myapp/additem.html',{'form':form})


def addadvanceandbonus(request):
    
     form=addadvanceandbonusform()
     if request.method == 'POST':
          form=addadvanceandbonusform(request.POST)
          if form.is_valid():
               if( int(request.POST['Advance'] or request.POST['Bonus']) > 0):
                    form.save()
                    return redirect('myapp:listothers')
               messages.error(request,'Enter valid data')
               return render(request,'myapp/additem.html',{'form':form})

     return render(request,'myapp/additem.html',{'form':form})


def listothers(request):
     staff=Staffprofile.objects.all()
     
     q=request.GET.get('q')
     if(q == None):
          q=1
     try:
          adv=Others.objects.get(Staff_id=q)
          return render(request,'myapp/listothers.html',{'adv':adv,'staff':staff})
     except:
          messages.error(request,'No records found')
          return render(request,'myapp/listothers.html')


def editothers(request):
     q=request.GET.get('q')
     expense=Others.objects.get(id=q)
     form=addadvanceandbonusform(instance=expense)
     if request.method == 'POST':
          form=addadvanceandbonusform(request.POST,instance=expense)
          if form.is_valid():

               if( int(request.POST['Advance'] or request.POST['Bonus']) > 0):
                    form.save()
                    redirect_url=reverse('myapp:listothers') + f'?q={q}'
                    return redirect(redirect_url)
               messages.error(request,'Enter valid data')
               return render(request,'myapp/additem.html',{'form':form})
               
        
               
     return render(request,'myapp/additem.html',{'form':form})


def deleteothers(request):

     q=request.GET.get('q')
     expense=Others.objects.get(id=q)
     expense.delete()
     redirect_url=reverse('myapp:listothers') + f'?q={1}'
        
     return redirect(redirect_url)


def addotherincome(request):
    
     form=addotherincomeform()
     if request.method == 'POST':
          form=addotherincomeform(request.POST)
          print(request.POST['Bag'])
          if form.is_valid():
               if( ((int(request.POST['Bag']) )or (int(request.POST['Paper_cone']))) > 0):
                    form.save()
                    return redirect('myapp:listotherincome')
               messages.error(request,'Enter valid data')
               return render(request,'myapp/additem.html',{'form':form})

     return render(request,'myapp/additem.html',{'form':form})


def listotherincome(request):
     current_year = date.today().year
     From=date(current_year, 1, 1)
     To=date.today()
         
     try:
          item=Otherincome.objects.filter(Date__range=(From,To))
          return render(request,'myapp/listotherincome.html',{'item':item,})
     except:
          messages.error(request,'No records found')
          return render(request,'myapp/listotherincome.html')


def editotherincome(request):
     q=request.GET.get('q')
     expense=Otherincome.objects.get(id=q)
     form=addotherincomeform(instance=expense)
     if request.method == 'POST':
          form=addotherincomeform(request.POST,instance=expense)
          if form.is_valid():
                if( int(request.POST['Bag'] or request.POST['Paper_cone']) > 0):
                    form.save()
                    return redirect('myapp:listotherincome')
                
                messages.error(request,'Enter valid data')
                return render(request,'myapp/additem.html',{'form':form})
                
     return render(request,'myapp/additem.html',{'form':form})


def deleteotherincome(request):

     q=request.GET.get('q')
     income=Otherincome.objects.get(id=q)
     income.delete()
     
     return redirect('myapp:listotherincome')


