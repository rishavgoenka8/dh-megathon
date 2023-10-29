from django.db import models
from django.core.exceptions import ValidationError

class PsychometricWeights(models.Model):
	general = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	reading = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	verbal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	number = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	numerical = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	spatial = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	nonverbal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	checking = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	spatial = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	personal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	
	def __str__(self):
		return "PsychometricWeights"

def validate_csv_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('Only CSV files are allowed.')

class Applicant(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    linkedIn_url = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, blank=True, null=True)
    psychometric_file = models.FileField(upload_to='files/psychometric_files/', validators=[validate_csv_extension], blank=True, null=True)
    profile_review = models.CharField(max_length=5000, blank=True, null=True)
    psychometric_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    post_review = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.name