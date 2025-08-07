import time

freqs = {}


with open('./ch6/all-1gram') as f:
    print('Читаю файл...')
    start = time.time()
    lines = f.readlines()
    print(f'Файл прочитан, время чтения {time.time() - start:.4f}...\r\n') 

    start = time.time()
    for line in lines:
        data = line.split('\t')
        word = data[0]
        count = int(data[2])

        if word in freqs:
            freqs[word] += count
        else:
            freqs[word] = count
    
    end = time.time()
    print(f'Время обработки: {end - start:.4f}')
