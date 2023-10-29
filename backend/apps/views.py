from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import PsychometricWeights, Applicant
import json
from django.http import JsonResponse
import csv
from io import TextIOWrapper
from .scrape import scrape
from .prompt import _openAI_skills, _openAI_culture
# Create your views here.


def fetch_psychometric_weights(request):
    try:
        # Retrieve the PsychometricWeights instance (assuming only one instance exists)
        psychometric_weights = PsychometricWeights.objects.first()

        if psychometric_weights:
            # Convert the model data to a dictionary
            data = {
                'general': psychometric_weights.general,
                'reading': psychometric_weights.reading,
                'verbal': psychometric_weights.verbal,
                'number': psychometric_weights.number,
                'numerical': psychometric_weights.numerical,
                'spatial': psychometric_weights.spatial,
                'nonverbal': psychometric_weights.nonverbal,
                'checking': psychometric_weights.checking,
                'personal': psychometric_weights.personal,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'No psychometric weights found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch psychometric weights', 'details': str(e)}, status=500)


# Use this decorator to bypass CSRF protection (for demonstration purposes)
@csrf_exempt
def update_weights(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            weights = data.get('weights', {})

            if not weights:
                return JsonResponse({'error': 'No data provided for update'}, status=400)

            # Assuming there's only one instance of PsychometricWeights
            psychometric_weights = PsychometricWeights.objects.first()

            if psychometric_weights:
                # Update the weights
                for criterion, value in weights.items():
                    setattr(psychometric_weights, criterion, value)
                psychometric_weights.save()

                return JsonResponse({'message': 'Weights updated successfully'})
            else:
                return JsonResponse({'error': 'No psychometric weights found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Failed to update psychometric weights', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_applicant(request):
    if request.method == 'POST':
        try:
            data = dict(request.POST)
            print('Received data:', data)
            applicant = Applicant.objects.create(
                name=data['name'][0],
                linkedIn_url=data['linkedIn_url'][0],
                email=data['email'][0],
                twitter_url=data['twitter_url'][0],
            )
            print(applicant)
            profile_url = data['linkedIn_url'][0]
            profile_info, post_info = scrape(profile_url)
            analysis1 = _openAI_skills(profile_info)
            analysis2 = _openAI_culture(post_info)
            print(analysis1)
            print(analysis2)
            print(analysis1)
            # Handle file upload
            if 'psychometric_file' in request.FILES:
                file = request.FILES['psychometric_file']
                # Save the file to a directory
                applicant.psychometric_file.save(file.name, file)
                print(type(file))
                psychometric_weights = PsychometricWeights.objects.first()
                uploaded_file = TextIOWrapper(
                    file, encoding='utf-8')  # Ensure it's in text mode
                print(uploaded_file)
                uploaded_file.seek(0)
                csv_reader = csv.reader(uploaded_file)
                candiate_scores = {}
                for row in csv_reader:
                    key = row[0]
                    if key == 'metric':
                        continue
                    val = float(row[1])
                    candiate_scores[key] = val
                total_score = 0.0
                total_weight = 0
                for field in psychometric_weights._meta.fields:
                    field_name = field.name  # Get the name of the field
                    # Get the value of the field
                    field_value = getattr(psychometric_weights, field_name)
                    print(field_name, field_value)
                    if field_name in candiate_scores:
                        total_score += float(field_value) * \
                            candiate_scores[field_name]
                        total_weight += float(field_value)
                print("Candidate score:", total_score/total_weight)
                applicant.psychometric_score = total_score/total_weight
                applicant.profile_review = analysis1
                applicant.post_review = analysis2
                applicant.save()
                # app_scores = csv.DictReader(applicant.psychometric_file)
                # print(type(app_scores))
                # for row in app_scores:
                #     try:
                #         print(row)
                #     except Exception as e:
                #         print(e)

            return JsonResponse({'message': 'Applicant created successfully'})
        except Exception as e:
            return JsonResponse({'error': 'Failed to create applicant', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def fetch_applicants(request):
    if request.method == 'GET':
        try:
            applicants = Applicant.objects.all()
            data = []
            for applicant in applicants:
                data.append({
                    'id': applicant.id,
                    'name': applicant.name,
                    'linkedIn_url': applicant.linkedIn_url,
                    'email': applicant.email,
                    'twitter_url': applicant.twitter_url,
                    'psychometric_file': applicant.psychometric_file.name,
                    'psychometric_score': applicant.psychometric_score,
                    'profile_review': applicant.profile_review,
                    'post_review': applicant.post_review,
                })
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'Failed to fetch applicants', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)