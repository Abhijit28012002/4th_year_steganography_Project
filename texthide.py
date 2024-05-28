letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','(', ')', '[', ']', '{', '}','1','2','3','4','5','6','7','8','9','0']
playing = ' '
final = ' '
org = ' '

def encrypt(s, n):
    result = []
    for x in s:
        if x == " ":
            converted = ' '
            result.append(converted)
        else:
            converted = (letters.index(x) + n) % 68
            result.append(letters[converted])
    final_result = ''.join(result)
    return final_result

def decrypt(s, n):
    back = []
    for x in s:
        if x == " ":
            original = ' '
            back.append(original)
        else:
            original = (letters.index(x) - n) % 68
            back.append(letters[original])
    org_result = ''.join(back)
    return org_result

