from api import PetFriends
from settings import valid_email, valid_password
import os
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    #
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    #
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


# def test_get_all_pets_with_valid_key(filter=''):  # filter available values : my_pets
def test_get_all_pets_with_valid_key(filter=''):
    # """ Проверяем что запрос всех питомцев возвращает не пустой список.
    # Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    # запрашиваем список всех питомцев и проверяем что список не пустой.
    # Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
#
#
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")



def test_successful_add_new_pet_without_photo_n1(name="ToM", animal_type="cat", age=5):

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status == 200



def test_fail_add_new_pet_without_photo_otric_age_n2(name="ToM", animal_type="cat", age=-3):

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status != 200


def test_fail_add_new_pet_without_photo_no_name_n3(name="", animal_type="cat", age=3):

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status != 200


def test_get_api_key_for_invalid_user_password_n4(email="1111.com", password="0000"):
    status, _ = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_key_for_invalid_user_email_n5(email="1111", password="1111"):
    status, _ = pf.get_api_key(email, password)

    assert status == 403


def test_add_new_pet_without_photo_incorrect_auth_key_n6(auth_key = {"key": "15fba3c114f061b314af69faf66c4421c8272fbf02338c61bc0f0f5c"}, name="max", animal_type="cat", age=3):
	status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status == 403


def test_add_photo_of_pet_n7(name="max", pet_id="441002a4-f762-4624-8e0d-ddb3de667fa6", pet_photo="images/cat1.jpg"):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


	status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

	assert status == 200



def test_add_photo_of_foreign_pet_n8(name="Misha", pet_id="154af336-9c30-42ba-8046-31fac3f3d8ab", pet_photo="images/cat1.jpg"):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, result = pf.get_list_of_pets(auth_key)

	status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

	assert status == 500


def test_delete_pet_incorrect_auth_key_n9(auth_key={"key": "15fba3c114f061b314af69faf66c4421c8272fbf02338c61bc0f0f5c"}, pet_id="441002a4-f762-4624-8e0d-ddb3de667fa6"):

	status, result = pf.delete_pet(auth_key, pet_id)

	assert status == 403


def test_fail_add_new_pet_without_photo_lage_age_n10(name="ToMb", animal_type="cat", age=10000000000):

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status != 200