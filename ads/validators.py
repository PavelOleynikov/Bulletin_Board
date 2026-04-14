from django.core.exceptions import ValidationError


class TitleValidator:
    """Валидатор для заголовка объявления"""

    def __call__(self, value):
        if len(value) < 3:
            raise ValidationError("Заголовок должен содержать минимум 3 символа")
        if len(value) > 200:
            raise ValidationError("Заголовок не должен превышать 200 символов")
        return value


class PriceValidator:
    """Валидатор для цены объявления"""

    def __call__(self, value):
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной")
        if value > 100000000:
            raise ValidationError("Цена не может превышать 100 000 000 рублей")
        return value


class DescriptionValidator:
    """Валидатор для описания объявления"""

    def __call__(self, value):
        if len(value) < 10:
            raise ValidationError("Описание должно содержать минимум 10 символов")
        if len(value) > 5000:
            raise ValidationError("Описание не должно превышать 5000 символов")
        return value


def validate_image_size(value):
    """Валидатор размера изображения (не более 5MB)"""

    if value.size > 5 * 1024 * 1024:
        raise ValidationError("Размер изображения не должен превышать 5MB")
    return value


def validate_image_extension(value):
    """Валидатор расширения изображения"""

    allowed_extensions = ["jpg", "jpeg", "png", "gif"]
    ext = value.name.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Разрешены только следующие форматы: {", ".join(allowed_extensions)}')
    return value


# Готовые экземпляры валидаторов для использования в сериализаторах
title_validator = TitleValidator()
price_validator = PriceValidator()
description_validator = DescriptionValidator()
