import os.path

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_key

pf = PetFriends()


def test_pet_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_pet_api_key_for_empty_email(email='', password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при незаполненном поле емайл """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_pet_api_key_for_empty_password(email=valid_email, password=''):
    """ Проверяем, что запрос api ключа возвращает статус 403 при незаполненном поле пароль """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_pet_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при невалидном емайл и пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проеряем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сораняем в переменную auth_key. Далее используя этот ключа
    запрашиваем список всех питомцев и проверяем, что список не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проеряем, что статус ответа при невалидном auth_key 403."""

    status, result = pf.get_list_of_pets(invalid_key, filter)

    assert status == 403


def test_get_all_pets_with_invalid_filte(filter='mdf'):
    """ Проеряем, что статус ответа при невалидном фильтре 403."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_get_all_my_pets_with_valid_key(filter='my_pets'):
    """ Проеряем, что запрос моих питомцев возвращает статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200


def test_add_new_pet_with_valid_data(name='Жучка', animal_type='Кот', age='4',
                                     pet_photo='images/1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в перемнную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ pi и сохраняем в перемнную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_negative_age(name='Жучка', animal_type='Кот', age='-4',
                                     pet_photo='images/1.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в перемнную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ pi и сохраняем в перемнную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_with_invalid_age(name='Жучка', animal_type='Кот', age='asda',
                                     pet_photo='images/1.jpg'):
    """Проверяем что нельзя добавить питомца с неправильным форматом в поле возраст"""

    # Получаем полный путь изображения питомца и сохраняем в перемнную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ pi и сохраняем в перемнную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_with_empty_name(name='', animal_type='Кот', age='-4',
                                     pet_photo='images/1.jpg'):
    """Проверяем что нельзя добавить питомца с пустым именем"""

    # Получаем полный путь изображения питомца и сохраняем в перемнную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ pi и сохраняем в перемнную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_successful_delete_self_pet():
    """Проверяем воможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Зверек", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем id первого питомца из списа и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Еще раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_seccessful_update_self_pet_info(name='Мурзик', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и  имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутсвии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_info_invalid_name(name='', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце с пустым именем"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутсвии своих питомцев
        raise Exception("There is no my pets")
