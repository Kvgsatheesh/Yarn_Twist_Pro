from django.urls import path
from .import views

app_name='myapp'

urlpatterns = [
    path('',views.homeview,name='home'),
    path('addcolour',views.addcolour,name='addcolour'),
    path('addcompany',views.addcompany,name='addcompany'),
    path('addcount',views.addcount,name='addcount'),
    path('addtp',views.addtp,name='addtp'),
    path('edit',views.edit,name='edit'),
    path('addprice',views.addprice,name='addprice'),
    path('addstaff',views.addstaff,name='addstaff'),
    path('deleteinventory/<int:id>',views.deleteinventory,name='deleteinventory'),
    path('updateinventory/<int:id>',views.updateinventory,name='updateinventory'),
    path('inward',views.inward,name='inward'),
    path('return',views.returnview,name='return'),   
    path('outward',views.Outward,name='outward'),
    path('statement',views.statementview,name='statement'),
    path('inventory',views.inventory,name='inventory'),
    path('paymentlist',views.paymentlist,name='paymentlist'),
    path('payment',views.paymentview,name='payment'),
    path('updateinward/<int:id>',views.updateinward,name='updateinward'),
    path('updateoutward/<int:id>',views.updateoutward,name='updateoutward'),
    path('updatepayment/<int:id>',views.updatepayment,name='updatepayment'),
    path('production',views.addproductionview,name='production'),
    path('productionreport',views.productionreportview,name='productionreport'),
    path('productionlist',views.productionlistview,name='productionlist'),
     path('productionedit',views.productioneditview,name='productionedit'),
     path('productiondelete',views.productiondeleteview,name='productiondelete'),
     path('productiondaily',views.productionweeklyview,name='productionweekly'),
     path('updatecolour',views.updatecolour,name='updatecolour'),
     path('updatecompany',views.updatecompany,name='updatecompany'),
    path('updatecount',views.updatecount,name='updatecount'),
    path('updatetp',views.updatetp,name='updatetp'),
    path('updatestaff',views.updatestaff,name='updatestaff'),
    path('updateprice',views.updateprice,name='updateprice'),
    path('addexpense',views.addexpense,name='addexpense'),
    path('expenselist',views.expenselist,name='expenselist'),
    path('editexpense',views.editexpense,name='editexpense'),
    path('addadvanceandbonus',views.addadvanceandbonus,name='addadvanceandbonus'),
    path('listothers',views.listothers,name='listothers'),
    path('editothers',views.editothers,name='editothers'),
    path('deleteothers',views.deleteothers,name='deleteothers'),
    path('addotherincome',views.addotherincome,name='addotherincome'),
    path('listotherincome',views.listotherincome,name='listotherincome'),
    path('editotherincome',views.editotherincome,name='editotherincome'),
    path('deleteotherincome',views.deleteotherincome,name='deleteotherincome'),

    

   

     
     


    


    
]
