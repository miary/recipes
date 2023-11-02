from django.db import models

class Recipe(models.Model):
    llm_model = models.TextField(max_length=40)
    prompt = models.TextField(max_length=500)
    response = models.TextField(blank=True, null=True)
    executed = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 
               
    def __str__(self):
        return self.prompt
        