def search4letters(phrase: str, letters: str = 'aouie') -> set:
    """выводит переданные буквы, найденные во введенном слове"""
    found = set(letters).intersection(set(phrase))
    return found
    # for vowel in found:
    #     print('vowels in input string: ' + vowel)


search4letters('tratata', 'aouie')
