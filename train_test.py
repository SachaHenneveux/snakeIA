from graphics import save_reward_plot
import torch
from agent import DQNAgent
import pygame
import time
from graphics import init_graphics, draw_game, save_reward_plot
from environnement import BLACK, SnakeGame
import argparse

def train():
    game = SnakeGame()
    agent = DQNAgent()
    episodes = 10000
    total_score = 0
    max_score = 0
    reward_history = []
    for episode in range(episodes):
        state = game.reset()
        done = False
        episode_score = 0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = game.step(action)
            agent.update(state, action, reward, next_state, done)
            state = next_state
            episode_score += reward
        agent.decay_epsilon()
        total_score += episode_score
        reward_history.append(episode_score)
        max_score = max(max_score, game.score)
        print(f"Episode {episode}, Score : {episode_score}, Max Score : {max_score},  Score : {game.score}")

        save_reward_plot(reward_history, episode, "your_model/dqn_model_your_model.png")
        torch.save(agent.model.state_dict(), f'your_model/dqn_model_your_model.pth')
        print(f"Modèle sauvegardé pour l'épisode {episode} dans 'dqn_model_your_model.pth'.")
    
    print(f"Score moyen : {total_score / episodes}")
    print(f"Score max : {max_score}")
    torch.save(agent.model.state_dict(), 'your_model/dqn_model_your_model.pth')
    print("Modèle sauvegardé dans 'your_model/dqn_model_your_model.pth'.")

def test():
    game = SnakeGame()
    agent = DQNAgent()
    try:
        agent.model.load_state_dict(torch.load('model/dqn_model.pth', map_location=agent.device))
        print("Modèle chargé avec succès.")
    except Exception as e:
        print("Erreur lors du chargement du modèle. Avez-vous déjà entraîné l'IA ?", e)
        return
    screen = init_graphics()
    state = game.reset()
    done = False
    font = pygame.font.Font(None, 20)
    while not done:
        draw_game(screen, game)
        
        score_text = font.render(f"Score: {game.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        pygame.event.pump()
        time.sleep(0.07)
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(agent.device)
        with torch.no_grad():
            q_values = agent.model(state_tensor)
        action = torch.argmax(q_values).item()
        state, _, done = game.step(action)
    print("Test terminé, score :", game.score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train or test the Snake AI.")
    parser.add_argument("--train", action="store_true", help="Train the AI.")
    parser.add_argument("--test", action="store_true", help="Test the AI.")

    args = parser.parse_args()

    if args.train:
        train()
    elif args.test:
        test()
    else:
        print("Veuillez spécifier --train ou --test.")