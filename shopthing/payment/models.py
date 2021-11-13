from django.db import models


class Invoice(models.Model):

    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    card_number = models.TextField(default="****")
    idpay_track_id = models.IntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)

    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + "  |  " + self.order_id + "  |  " + str(self.status)