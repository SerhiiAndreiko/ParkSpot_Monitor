from django.utils.decorators import method_decorator
from django.views.generic import View
from users.models import Plates, Sessions
from .number_recognition import recognize_plate
from django.views.decorators.csrf import csrf_exempt
import cv2
from admin_app.forms import UploadImageForm 
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@method_decorator(csrf_exempt, name='dispatch')
class UploadImageView(View):
    def get(self, request, *args, **kwargs):
        initial_data = {
            'image': None,
        }

        form = UploadImageForm(initial=initial_data)

        context = {
            'form': form,
        }

        return render(request, 'number_recognition/number_recognition.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            image_file = request.FILES['image']
            plate_number = recognize_plate(image_file)

            if plate_number:
                try:
 
                    if request.user.is_authenticated:
                        user = request.user
                        plate = Plates.objects.create(plate=plate_number, user=user)
                        session = Sessions.objects.create(plate=plate)
                        return JsonResponse({'message': f"Номер розпізнано: {plate_number}. Сесія створена.", 'plate_number': plate_number})
                    else:
                        return JsonResponse({'message': "Для створення сесії, потрібно увійти до системи."})
                except Exception as e:
                    print(f"Error processing plate: {e}")
                    return JsonResponse({'message': "Помилка обробки даних. Спробуйте ще раз."})
            else:
                return JsonResponse({'message': "Номер не розпізнано"})
