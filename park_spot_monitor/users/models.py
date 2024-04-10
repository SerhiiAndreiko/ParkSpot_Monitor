from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Plates(models.Model):
    plate = models.CharField(unique=True, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plate} User {self.user.username}"


class Sessions(models.Model):
    entrance_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True)
    plate = models.ForeignKey(Plates, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session for {self.plate.plate}"


# class BlacklistedVehicle(models.Model):
#     plate = models.ForeignKey('Plates', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


#     def __str__(self):
#         return f"{self.plate.plate} User {self.user.username}"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - ${self.amount}"


@receiver(post_save, sender=User)
def create_or_update_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
    else:
        if hasattr(instance, 'balance'):  # Check if 'balance' exists for the user
            instance.balance.amount = 0
            instance.balance.save()
        else:
            Balance.objects.create(user=instance, amount=0)  # Create 'balance' if it doesn't exist

