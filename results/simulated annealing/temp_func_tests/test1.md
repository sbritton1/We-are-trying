temperature = 500 * (0.997 ** iteration) + ((50 / (int(iteration / 1000) + 1)) * 0.997 ** (iteration % 1000))
results: [35193, 36147, 35931, 36012, 36039, 35904, 35877, 35985]