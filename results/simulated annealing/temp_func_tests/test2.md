temperature = 500 * (0.997 ** iteration) + ((25 / (int(iteration / 1000) + 1)) * 0.997 ** (iteration % 1000))
results: [30643, 31102, 31057, 30643, 30607, 31048, 31282, 30778]