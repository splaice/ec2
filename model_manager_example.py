
from ec2 import Reservation
reservation = Reservation.objects.get(id='res-123')
for instance in reservation.instances:
    instance.stop()
Reservation.objects.stop([i.id for i in reservation.instances])

reservation = Reservation.objects.get(id=reservation.id)
for instance in reservation.instances:
    instance.delete()
Reservation.objects.delete([i.id for i in reservation.instances])


from ec2 import Instance
instance = Instance.objects.create('ami-123')
print instance

instance.stop()
instance.delete()

instance = Instance('ami-123')
instance.save()
print instance

instance.stop()
instance.delete()
