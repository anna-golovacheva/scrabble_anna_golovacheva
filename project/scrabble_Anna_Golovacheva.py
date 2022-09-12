import random

LETTERS = {
    'а': 8,
    'б': 2,
    'в': 4,
    'г': 2,
    'д': 4,
    'е': 8,
    'ё': 1,
    'ж': 1,
    'з': 2,
    'и': 5,
    'й': 1,
    'к': 4,
    'л': 4,
    'м': 3,
    'н': 5,
    'о': 10,
    'п': 4,
    'р': 5,
    'с': 5,
    'т': 5,
    'у': 4,
    'ф': 1,
    'х': 1,
    'ц': 1,
    'ч': 1,
    'ш': 1,
    'щ': 1,
    'ъ': 1,
    'ы': 2,
    'ь': 2,
    'э': 1,
    'ю': 1,
    'я': 2
}

letters_list = []
for letter, num in LETTERS.items():
    for i in range(num):
        letters_list.append(letter)
        num -= 1

user_words_list = []
game = True


def give_letters(letter_list_user, if_correct):
    """
        Функция выдает пользователю буквы в первый раз,
        после правильного ответа, чтобы восполнить потраченные,
        или после неправильного ответа (1 букву). Возвращает список букв пользователя.
    """

    if if_correct:
        length = len(letter_list_user)
        if length == 0:
            letter_list_user = random.sample(letters_list, 7)
            for used_letter in letter_list_user:
                letters_list.remove(used_letter)
        elif length < 8:
            quantity = 8 - length
            new_letter_list_user = random.sample(letters_list, quantity)
            for new_used_letter in new_letter_list_user:
                letters_list.remove(new_used_letter)
            new_letters_for_user_str = ', '.join(new_letter_list_user)
            print(f'Добавляю буквы "{new_letters_for_user_str}"')
            letter_list_user += new_letter_list_user
    else:
        new_letter_list_user = random.sample(letters_list, 1)
        for new_used_letter in new_letter_list_user:
            letters_list.remove(new_used_letter)
        new_letters_for_user_str = new_letter_list_user[0]
        print(f'Добавляю буквы "{new_letters_for_user_str}"')
        letter_list_user += new_letter_list_user

    return letter_list_user


def letters_check(letter_list_user_check, user_word):
    """
        Функция проверяет, что пользователь использовал только те буквы,
        которые были у него в списке, и только столько раз, сколько у него было.
    """

    if_user_letter = []
    for w in user_word:
        if w in letter_list_user_check:
            if_user_letter.append(True)
            letter_list_user_check.remove(w)
        else:
            if_user_letter.append(False)

    letters_check_f = all(if_user_letter)

    return letters_check_f


def word_choice(user_name, russian_word_list, letter_list_user, user_name_1, user_name_2, user_1_total, user_2_total):
    """
        Функция принимает ответ пользователя и оценивает его.
        Возвращает результат выбора пользователя, назначенные за него баллы
        и список использованных в игре слов.
        Если пользователь решил завершить игру, вызывается функция finish_game().
    """

    global game
    is_typo = True
    while is_typo:
        user_word = input(f'Ходит {user_name}: ')
        user_word = user_word.lower()
        choice, points = False, 0
        letter_list_user_check = letter_list_user.copy()
        if user_word == 'stop' or len(letters_list) == 0:
            print(f'Игра окончена.\n')
            finish_game(user_name_1, user_name_2, user_1_total, user_2_total)
            game = False
            is_typo = False
        elif letters_check(letter_list_user_check, user_word):
            if user_word not in russian_word_list or len(user_word) < 3:
                print(f'Такого слова нет, или оно слишком короткое.\n{user_name} не получает очков.')
            elif user_word in user_words_list:
                print(f'Такое слово уже было использовано в игре.')
            else:
                choice = True
                points_dict = {3: 3, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10}
                for word_len, word_points in points_dict.items():
                    if len(user_word) == word_len:
                        points = word_points
                user_words_list.append(user_word)
            is_typo = False
        else:
            print('Вы использовали не свои буквы.')

    return choice, points, user_words_list


def finish_game(user_name_1, user_name_2, user_1_total, user_2_total):
    """
            Функция подводит итоги игры.
        """

    if user_1_total > user_2_total:
        print(f'Выигрывает {user_name_1}.\nСчет {user_1_total}:{user_2_total}.')
    elif user_1_total < user_2_total:
        print(f'Выигрывает {user_name_2}.\nСчет {user_2_total}:{user_1_total}.')
    else:
        print(f'Ничья!\nСчет {user_2_total}:{user_1_total}.')


def main():
    global user_words_list, game
    user_words_list = []

    user_1_total = 0
    user_2_total = 0

    letter_list_user_1 = []
    letter_list_user_2 = []

    russian_word_list = []
    with open('russian_word.txt', 'r', encoding='utf-8') as russian_word:
        for word in russian_word:
            russian_word_list.append(word.rstrip('\n'))

    user_name_1 = input('Как зовут первого игрока? ')
    user_name_2 = input('Как зовут второго игрока? ')
    print(f'{user_name_1} vs {user_name_2}\nРаздаю случайные буквы...')

    game_counter = 0

    while True:
        if_correct = True
        game_counter += 1
        if game_counter % 2 == 1:
            user_name = user_name_1
            user_total = user_1_total
            letter_list_user = letter_list_user_1.copy()

        else:
            user_name = user_name_2
            user_total = user_2_total
            letter_list_user = letter_list_user_2.copy()

        letter_list_user = give_letters(letter_list_user, if_correct)
        letter_list_user_str = ', '.join(letter_list_user)
        print(f'{user_name}, все буквы: "{letter_list_user_str}"')
        user_choice, user_points, user_words_list = word_choice(user_name, russian_word_list, letter_list_user, user_name_1, user_name_2, user_1_total, user_2_total)

        if game is False:
            break
        elif user_choice:
            print(f'Такое слово есть.\n{user_name} получает {user_points} баллов.')
            user_total += user_points
            for letter_ in user_words_list[-1]:
                letter_list_user.remove(letter_)
        else:
            if_correct = False
            letter_list_user = give_letters(letter_list_user, if_correct)

        if game_counter % 2 == 1:
            letter_list_user_1 = letter_list_user.copy()
            user_1_total = user_total
            print(f'У {user_name_1} {user_1_total} баллов.')
        else:
            letter_list_user_2 = letter_list_user.copy()
            user_2_total = user_total
            print(f'У {user_name_2} {user_2_total} баллов.')

        if len(user_words_list) > 0:
            print('Разыгранные слова:')
            for word_in_game in user_words_list:
                print(f'{word_in_game}')

        print(letters_list)
main()


