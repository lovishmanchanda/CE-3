from .models import Food, Clothes, Medicine, Accessory

def get_product_instance(category, product_id):
    if category == 'food':
        return Food.objects.get(id=product_id)
    elif category == 'clothes':
        return Clothes.objects.get(id=product_id)
    elif category == 'medicine':
        return Medicine.objects.get(id=product_id)
    elif category == 'accessory':
        return Accessory.objects.get(id=product_id)  # ✅ Singular name
    return None

def get_product_by_category(category, product_id):
    model_map = {
        'food': Food,
        'cloth': Clothes,
        'medicine': Medicine,
        'accessory': Accessory,
    }
    model = model_map.get(category.lower())
    if model:
        try:
            return model.objects.get(id=product_id)
        except model.DoesNotExist:
            return None
    return None
