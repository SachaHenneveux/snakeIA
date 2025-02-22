# graphics.py
import pygame
import numpy as np
import matplotlib.pyplot as plt
from environnement import GRID_SIZE, SCREEN_SIZE, WHITE, GREEN, RED, BLACK

def init_graphics():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    return screen

def draw_game(screen, game):
    screen.fill(WHITE)
    for segment in game.snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (game.food[0] * GRID_SIZE, game.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()

def save_reward_plot(reward_history, episode, pathpng):
    window_size = 10

    plt.figure()
    if len(reward_history) >= window_size:
        moving_avg = np.convolve(reward_history, np.ones(window_size)/window_size, mode='valid')
        x_values = range(len(reward_history))
        plt.scatter(x_values, reward_history, color='blue', label="Récompenses par épisode", s=10)
        plt.plot(range(window_size-1, len(reward_history)), moving_avg, color='red', label=f"Moyenne mobile ({window_size} épisodes)")
    else:
        plt.scatter(range(len(reward_history)), reward_history, color='blue', label="Récompenses par épisode", s=10)
    
    plt.title(f"Évolution des récompenses - Épisode {episode}")
    plt.xlabel('Épisodes')
    plt.ylabel('Reward')
    plt.legend()
    plt.savefig(pathpng)
    plt.close()
