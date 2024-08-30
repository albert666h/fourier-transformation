import pygame
import numpy as np
import math

pygame.init()

window = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
fps = 30
dt = 0
time = 0
fr = 20

state = 0
mouse_motion = 0
mouse_down = 0

path = []

data = []

bg = pygame.surface.Surface((1080, 720))
bg.fill(0)
bg.set_alpha(150)


def mult(x, y):
    return np.array([x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]])


def dft(data):
    X = []
    N = len(data)
    for k in range(0, N):
        s = np.array([0.0, 0.0])
        for n in range(N):
            theta = np.pi * 2 * k * n / N
            s += mult(np.array([np.cos(theta), -np.sin(theta)]), data[n])
        s /= N
        X.append((k, np.sqrt(sum(s * s)), math.atan2(s[1], s[0])))

    return X


def draw(X, time):
    start = np.array([540.0, 360.0])
    for i in X:
        freq, amp, phase = i
        theta = (time * freq) + phase
        v = np.array([np.cos(theta), np.sin(theta)])
        pygame.draw.circle(window, (255, 255, 255), start, amp, 1)
        pygame.draw.line(window, (255, 255, 255), start, start + v * amp)
        start += v * amp
    path.append(start)

    window.blit(bg, (0, 0))

    if len(path) > 1:
        for j in range(1, len(path)):
            pygame.draw.line(window, (255, 255, 255), path[j - 1], path[j])


run = True

while run:
    mouse_motion = 0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            break
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            if state == 0:
                state = 1
                data = path
                mid = sum(data) / len(data)
                for i in range(len(data)):
                    data[i] -= mid
                path = []
                a = dft(data)
                a = sorted(a, key=lambda x: x[1], reverse=True)
            elif state == 1:
                state = 0
                time = 0
                path = []

        elif e.type == pygame.MOUSEMOTION:
            mouse_motion = 1
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = 1
        elif e.type == pygame.MOUSEBUTTONUP:
            mouse_down = 0

    clock.tick(fps)
    dt = clock.get_time() / 1000
    if state == 0:
        if mouse_down and mouse_motion:
            x, y = pygame.mouse.get_pos()
            path.append(np.array([x, y], dtype="float"))
        window.fill(0)

        if len(path) > 1:
            for j in range(1, len(path)):
                pygame.draw.line(window, (255, 255, 255), path[j - 1], path[j])

        pygame.display.update()

    elif state == 1:
        time += np.pi * 2 / len(data)

        if time > np.pi * 2:
            time = 0
            path = []

        window.fill(0)

        draw(a, time)

        pygame.display.update()

pygame.quit()
