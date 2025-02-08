from django.db import models

class Review(models.Model):
    
    	
    Subject = models.TextField(max_length=50 , default = 'NA')
    review = models.TextField(max_length=1000 , default = 'NA')
    Sector = models.TextField(max_length=20 , default = 'NA')
    Governorate = models.TextField(max_length=20 , default = 'NA')
    City = models.TextField(max_length=20 , default = 'NA')
    Important_Topics = models.TextField(max_length=30 , default = 'NA')
    Sentiment_type = models.TextField(max_length=20 , default='NA')
    Topic = models.TextField(max_length=30 , default='NA')
    Recommended_action = models.TextField(max_length=2000 , default= "NA")
    class Meta:
        verbose_name = 'review'
    
