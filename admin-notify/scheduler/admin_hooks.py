from django.contrib import admin


class GroopTaskModelAdmin(admin.ModelAdmin):
    
    #def __init__(self):
    #    super().__init__()

    def save_model(self, request, obj, form, change):
        print(f'type model: {type(self.model)}')
        print(f'type model: {type(obj)}')
        obj.save()