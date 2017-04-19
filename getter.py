from PIL import Image  # модуль для работы с изображениями
from operator import itemgetter  # для сортировки списков
import math  # математика для энтропии

result_1 = []  # список с результатом

im = Image.open("FORLAB.bmp")  # открытие изображения для работы с ним
pixels = im.load()  # для возможности работы с изображением попиксельно
for i in range(0, 128):  # 128 - ширина строки
    result_1.append(pixels[64, i])  # сохранение значения каждого пикселя

f = open('pixels.txt', 'w')  # запись в файл
for i in range(0, len(result_1)):
    f.write(('{}  {} \n').format(i + 1, result_1[i]))

result_2 = []

for pixel in result_1:  # квантование
    if pixel % 20 >= 10:
        temp = math.ceil(pixel / 20) * 20
    else:
        temp = math.floor(pixel / 20) * 20
    result_2.append(temp)

f = open('quanted.txt', 'w')  # запись в файл
for i in range(0, len(result_2)):
    f.write(('{}  {} \n').format(i + 1, result_2[i]))

frequency_dict = {}  # количество появления символов
for pixel in result_2:
    if pixel not in frequency_dict.keys():
        frequency_dict.update([(pixel, 1)])
    else:
        frequency_dict[pixel] += 1

for pixel in frequency_dict.keys():  # преобразование к частотам
    frequency_dict[pixel] /= 128
    frequency_dict[pixel] = round(frequency_dict[pixel], 2)

e = 0
for pixel in frequency_dict.keys():
    e += frequency_dict[pixel] * math.log(frequency_dict[pixel], 2)
e = -e

f = open('frequences.txt', 'w')  # запись в файл
for pixel in frequency_dict.keys():
    f.write(('{}  {} \n').format(pixel, frequency_dict[pixel]))
f.write('Entropy = {}'.format(e))

f_list = list(frequency_dict.items())  # преобразование в список и его дальнейшая сортировка
f_list.sort(key=itemgetter(1))


balanced_code_l = math.ceil(math.log2(len(frequency_dict)))  # длина равномерного кода
symbols = [i for i in frequency_dict.keys()]
symbols.sort()
balanced_codes = []

iter = 0

for pixel in symbols:  # формирование равномерного кода
    binary = bin(iter)
    binary = binary.replace('b', '')
    while len(binary) < balanced_code_l:
        binary = '0' + binary
    while len(binary) > balanced_code_l:
        binary = binary[1:len(binary)]
    balanced_codes.append((pixel, binary))
    iter += 1

balanced_codes_dict = {pixel[0] : pixel[1] for pixel in balanced_codes}
balanced_coded = []
for pixel in result_2:
    balanced_coded.append(balanced_codes_dict[pixel])


f = open('balanced.txt', 'w')  # запись в файл
for pixel in balanced_codes:
    f.write(('{}  {} \n').format(pixel[0], pixel[1]))

for i in range(0, len(balanced_coded)):
    f.write(('{} {} \n').format(i + 1, balanced_coded[i]))

def sh_fano(freq_list):  # получение кодов Шеннона-Фано
    answer = {pixel[0]: '' for pixel in freq_list}  # словарь под ответ
    if len(freq_list) == 1:  # для выхода из рекурсии
        return None
    freq_sum = 0
    for i in freq_list:
        freq_sum += i[1]
    sumleft = [0, 0]
    sumindex = 0
    for pixel in freq_list:  # деление списка на 2 части
        sumleft[0] += pixel[1]
        sumleft[1] += pixel[1]
        sumindex += 1
        if sumleft[0] >= freq_sum / 2:
            sumleft[1] -= pixel[1]
            sumindex -= 1
            break
    if abs(freq_sum / 2 - sumleft[0]) <= abs(freq_sum / 2 - sumleft[1]):
        sumindex += 1
    for index in range(0, sumindex):  # рекурсивно получаем коды
        try:
            answer[freq_list[index][0]] += '0'
            answer[freq_list[index][0]] += sh_fano(freq_list[0:sumindex])[freq_list[index][0]]
        except:
            pass
    for index in range(sumindex, len(freq_list)):
        try:
            answer[freq_list[index][0]] += '1'
            answer[freq_list[index][0]] += sh_fano(freq_list[sumindex:(len(freq_list))])[freq_list[index][0]]
        except:
            pass
    return answer


sh_fano_codes = sh_fano(f_list)
l = list(sh_fano_codes.items())
l.sort(key=itemgetter(1))

# кодирование последовательности
sh_fano_coded = []
for pixel in result_2:
    sh_fano_coded.append(sh_fano_codes[pixel])

f = open('sh_fano.txt', 'w')  # запись в файл
for pixel in l:
    f.write(('{}  {} \n').format(pixel[0], pixel[1]))

sum = 0
for pixel in result_2:
    sum += len(sh_fano_codes[pixel])
f.write('Code length: {} \n'.format(sum))

shf_sum = sum

for i in range(0, len(sh_fano_coded)):
    f.write(('{} {} \n').format(i + 1, sh_fano_coded[i]))

new_flist = f_list.copy()

answer = {pixel[0]: '' for pixel in new_flist}

while len(new_flist) != 1:  # получение кодов Хаффмана
    temp_freq = new_flist[0][-1] + new_flist[1][-1]  # сложение двух наименьших вероятностей
    tt = []
    try:  # добавление полученной вероятности
        for i in new_flist[0][0]:
            tt.append(i)
            answer[i] += '0'
    except:
        tt.append(new_flist[0][0])
        answer[new_flist[0][0]] += '0'
    try:
        for i in new_flist[1][0]:
            tt.append(i)
            answer[i] += '1'
    except:
        tt.append(new_flist[1][0])
        answer[new_flist[1][0]] += '1'
    new_flist.append((tt, temp_freq))
    new_flist.pop(0)  # удаление вероятностей
    new_flist.pop(0)
    new_flist.sort(key=itemgetter(-1))  # сортировка


def sortbylen(tuple):
    return len(tuple[1])


huff_codes = answer
answ_list = list(answer.items())
answ_list.sort(key=sortbylen)

# кодирование последовательности
huff_coded = []
for pixel in result_2:
    huff_coded.append(huff_codes[pixel])

f = open('huff.txt', 'w')  # запись в файл
for pixel in answ_list:
    f.write(('{}  {} \n').format(pixel[0], pixel[1]))

sum = 0
for pixel in result_2:
    sum += len(huff_codes[pixel])
f.write('Code length: {} \n'.format(sum))
huff_sum = sum

for i in range(0, len(huff_coded)):
    f.write(('{} {} \n').format(i + 1, huff_coded[i]))

# средние длины кодовых комбинаций
shf_i_avg = 0
for pixel in sh_fano_codes.items():
    shf_i_avg += len(sh_fano_codes[pixel[0]]) * frequency_dict[pixel[0]]

huff_i_avg = 0
for pixel in huff_codes.items():
    huff_i_avg += len(huff_codes[pixel[0]]) * frequency_dict[pixel[0]]

f = open('Iavg.txt', 'w')
f.write(('Sh_F Iavg = {} \n').format(round(shf_i_avg, 3)))
f.write(('Huff Iavg = {} \n').format(round(huff_i_avg, 3)))

# степень сжатия
comp_shf = round(512 / shf_sum, 3)
comp_huff = round(512 / huff_sum, 3)
f.write(('Sh_F compression = {} \n').format(comp_shf))
f.write(('Huff compression = {} \n').format(comp_huff))

# избыточность
q_shf = 1 - (e / shf_i_avg)
q_huff = 1 - (e / huff_i_avg)

f.write(('Sh_F Q = {} \n').format(round(q_shf, 6)))
f.write(('Huff Q = {} \n').format(round(q_huff, 6)))
