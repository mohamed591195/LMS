
from django.db.models.fields import PositiveIntegerField
from django.core.exceptions import ObjectDoesNotExist

class OrderField(PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
            # we check if the instance has a previous value for this field, because it could be not the first time 
            #to save this instance , may be this is an updating
        if getattr(model_instance, self.attname) is None: #self.attname is the name of the field in the model
            
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # get objects that has the same fields(attributs) in for_fields 
                    #it's like so 
                    #for_fields = 'course, module, title'
                    # the query will be the value of these fields on the instance which we work on now(and have this field(orderfield ) and will be saved)
                    # course = 1 we assume it's one in this instanse 
                    # module = 3 and so on for the title
                    query = {field: getattr(model_instance, field) for field in self.for_fields}                                                                          
                    qs = qs.filter(**query)                                
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)



