import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
import gymnasium as gym
import time

# from environment import RL_Environment

from custom_environment import CustomRL_Environment

log_path = os.path.join('Training', 'Logs')
env  = CustomRL_Environment()


# It will check your custom environment and output additional warnings if needed
check_env(env)
print("Environement is correct")

model = PPO('MlpPolicy', env, verbose = 1,tensorboard_log=log_path)

model.learn(total_timesteps=20000)


PPO_path = os.path.join('Training', 'Saved Models', 'PPO_model')

model.save(PPO_path)