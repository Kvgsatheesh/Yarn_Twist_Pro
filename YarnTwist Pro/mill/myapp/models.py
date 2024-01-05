from django.db import models
from datetime import date


# Create your models here.


class Company(models.Model):
    Company=models.CharField(max_length=50,unique=True)
    Address=models.TextField(blank=True,null=True)


    def __str__(self):
        return self.Company
    
class Colour(models.Model):
    
    Colour=models.CharField( max_length=50,unique=True)

    def __str__(self):
        return self.Colour
    
class Tp(models.Model):
    Tp=models.PositiveIntegerField(max_length=2, unique=True)

    def __str__(self):
        return str(self.Tp)
    
class Count(models.Model):
    Count=models.PositiveIntegerField(max_length=2, unique=True)

    def __str__(self):
        return str( self.Count)

class Price(models.Model):
    Company=models.ForeignKey("Company",on_delete=models.CASCADE)
    Count=models.ForeignKey("Count", on_delete=models.CASCADE)
    Tp=models.ForeignKey("Tp", on_delete=models.CASCADE)
    Tfo_price=models.PositiveBigIntegerField(default=1)
    Cheese_price=models.PositiveBigIntegerField(default=1)
    Doubled_price=models.PositiveBigIntegerField(default=1)
    Per_bag=models.FloatField(default=1)
     
    def __str__(self):
        return f'({self.Tfo_price} {self.Cheese_price} {self.Doubled_price} {self.Company} {self.Count} {self.Tp} {self.Per_kg})'


class Stocks(models.Model):

    Company=models.ForeignKey("Company",on_delete=models.CASCADE)
    Colour=models.ForeignKey("Colour",on_delete=models.CASCADE)
    Count=models.ForeignKey("Count", on_delete=models.CASCADE)
    Tp=models.ForeignKey("Tp", on_delete=models.CASCADE)

    Inward=models.FloatField(default=0)
    Outward=models.FloatField(default=0)

    Bag=models.FloatField(default=0)
    Amount=models.FloatField(default=0)
    Date=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True,null=True)



    def __str__(self):
         return f'({self.Date} {self.Company} {self.Colour} {self.Inward} {self.Outward} {self.Date})'
    
          
class Staffprofile(models.Model):
    name=models.CharField(max_length=30)
    mobile_number=models.PositiveIntegerField(max_length=10)

    def __str__(self):
        return self.name
    
class Production(models.Model):
    Stocks=models.ForeignKey("Stocks", on_delete=models.CASCADE,null=True) 
    Staff=models.ForeignKey("Staffprofile", on_delete=models.CASCADE,null=True)
    Company=models.ForeignKey("Company", on_delete=models.CASCADE)
    Colour=models.ForeignKey("Colour", on_delete=models.CASCADE)
    Count=models.ForeignKey("Count", on_delete=models.CASCADE)
    Tp=models.ForeignKey("Tp", on_delete=models.CASCADE)

    Inward=models.FloatField(default=0)
    Outward=models.FloatField(default=0)

    Tfo_shift=models.FloatField(default=0)
    Cheese_bag=models.PositiveIntegerField(default=0)
    Waste=models.PositiveIntegerField(default=0)
    Doubled_bag=models.PositiveIntegerField(default=0)
    
    Total_salary=models.FloatField(default=0)
    Date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'({self.Colour} {self.Count} {self.Tp} {self.Cheese_bag}{self.Doubled_bag} {self.Company} {self.Date}  )'



class Expense(models.Model):
    Expense=models.CharField(max_length=50)
    Amount=models.PositiveIntegerField()
    
    Date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'({self.Expense} {self.Amount})'


class Others(models.Model):
    Staff=models.ForeignKey("Staffprofile", on_delete=models.CASCADE,null=True)
    Advance=models.PositiveIntegerField(default=0)
    Bonus=models.PositiveIntegerField(default=0)
    Date=models.DateField(auto_now_add=True)


    def __str__(self):
        return f'({self.Staff} {self.Advance} {self.Bonus} {self.Date} )'
    
class Otherincome(models.Model):
    Paper_cone=models.PositiveIntegerField(default=0)
    Bag=models.PositiveIntegerField(default=0)
    Date=models.DateField(auto_now_add=True)


    def __str__(self):
        return f'({self.Paper_cone} {self.Bag} {self.Date} )'