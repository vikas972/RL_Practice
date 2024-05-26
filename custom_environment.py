import gymnasium as gym
import numpy as np
import turtle as t
import random

class CustomRL_Environment(gym.Env):
    """Custom Environment for Reinforcement Learning."""
    
    def __init__(self):
        super().__init__()
        
        # Define action and observation space
        self.action_space = gym.spaces.Discrete(4)  # Four discrete actions
        self.observation_space = gym.spaces.Box(low=np.array([0, 0]), 
                                            high=np.array([1, 1]), 
                                            dtype=np.float32)  # [needy, fire]

        # self.observation_space = gym.spaces.Box(low=np.array([0, 0, -300, -300]), 
        #                                         high=np.array([1, 1, 300, 300]), 
        #                                         dtype=np.float32)
        
        # Setup Background
        self.win = t.Screen()
        self.win.title('Reinforcement Learning Environment')
        self.win.bgcolor('white')
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

        # Set background image
        self.win.bgpic("map/map_image.png")

        # Create legend
        self.create_legend()

        # Agent 1: Logistics and Supply Agent
        self.logistics_agent = self.create_agent(-200, -200, 'triangle', 'green')

        # Agent 2: Command and Control Agent
        self.command_agent = self.create_agent(200, 200, 'circle', 'red')

        # Needy People
        self.needy_people = []

        # Fire
        self.fire_danger = []

        # Delay for appearance of fire and needy people
        self.fire_appearance_delay = 1000
        self.needy_appearance_delay = 3000
        
        # Define max steps
        self.max_steps = 1000
        self.current_step = 0
        
        # Define rewards
        self.logistics_reward = 0.0
        self.command_reward = 0.0
        self.reward = 0.0

    # Create agent
    def create_agent(self, x, y, shape, color):
        agent = t.Turtle()
        agent.shape(shape)
        agent.color(color)
        agent.penup()
        agent.goto(x, y)
        return agent

    # Create legend
    def create_legend(self):
        legend = t.Turtle()
        legend.penup()
        legend.goto(290, 290)  # Adjust coordinates to move to extreme upper-right corner
        legend.color('black')
        legend.write("Legend:", align="right", font=("Arial", 14))
        
        legend.goto(290, 270)
        legend.dot(12, 'green',)  # Dot for Logistics and Supply Agent
        legend.write("Logistics and Supply Agent   ", align="right", font=("Arial", 12,"bold"))
        
        legend.goto(290, 250)
        legend.dot(12, 'red')  # Dot for Command and Control Agent
        legend.write("Command and Control Agent   ", align="right", font=("Arial", 12,"bold"))
        
        legend.goto(290, 210)
        legend.dot(12, 'yellow')  # Dot for Fire
        legend.write("Fire   ", align="right", font=("Arial", 12,"bold"))
        
        legend.goto(290, 230)
        legend.dot(12, 'black')  # Dot for Needy People
        legend.write("Needy People  ", align="right", font=("Arial", 12,"bold"))

    def step(self, action):
        # self.current_step += 1
        done = False
        
        logistics_action = action
        command_action = action

        self.logistics_reward = 0.0
        self.command_reward = 0.0

        

        if logistics_action == 0:
            x = self.logistics_agent.xcor()
            if x > -300:
                self.logistics_agent.setx(x - 20)
        elif logistics_action == 1:
            x = self.logistics_agent.xcor()
            if x < 300:
                self.logistics_agent.setx(x + 20)
        elif logistics_action == 2:
            y = self.logistics_agent.ycor()
            if y < 300:
                self.logistics_agent.sety(y + 20)
        elif logistics_action == 3:
            y = self.logistics_agent.ycor()
            if y > -300:
                self.logistics_agent.sety(y - 20)



        if command_action == 0:
            x = self.command_agent.xcor()
            if x > -300:
                self.command_agent.setx(x - 20)
        elif command_action == 1:
            x = self.command_agent.xcor()
            if x < 300:
                self.command_agent.setx(x + 20)
        elif command_action == 2:
            y = self.command_agent.ycor()
            if y < 300:
                self.command_agent.sety(y + 20)
        elif command_action == 3:
            y = self.command_agent.ycor()
            if y > -300:
                self.command_agent.sety(y - 20)


        for needy_person in self.needy_people:
            if abs(needy_person.xcor() - self.logistics_agent.xcor()) < 20 and abs(needy_person.ycor() - self.logistics_agent.ycor()) < 20:
                self.logistics_reward += 1.0
                self.needy_people.remove(needy_person)
                needy_person.goto(1000, 1000) 

        for fire in self.fire_danger:
            if abs(fire.xcor() - self.command_agent.xcor()) < 20 and abs(fire.ycor() - self.command_agent.ycor()) < 20:
                self.command_reward += 1.0
                self.fire_danger.remove(fire)
                fire.goto(1000, 1000)  

        if random.randint(1, self.needy_appearance_delay) == 1:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            self.add_needy_person(x, y)

        if random.randint(1, self.fire_appearance_delay) == 1:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            self.add_fire(x, y)

        # done = self.current_step >= self.max_steps
        # Determine if the episode is done
        if len(self.needy_people) == 0 and len(self.fire_danger)==0:  # No more needy people left
            done = True
        self.reward = self.logistics_reward+self.command_reward
        return self._get_obs(),float(self.reward), done,False, {}


    def _get_obs(self):
        return np.array([len(self.needy_people) > 0, len(self.fire_danger) > 0],dtype=np.float32)

    def reset(self,seed=None, options=None):
        info = {}
        self.current_step = 0
        self.logistics_reward = 0.0
        self.command_reward = 0.0
        self.reset_env()

        return self._get_obs(),info

    def reset_env(self):
        for needy_person in self.needy_people:
            needy_person.goto(1000, 1000)
        self.needy_people = []
        for fire in self.fire_danger:
            fire.goto(1000, 1000)
        self.needy_people = []
        self.fire_danger = []

    def render(self, mode='human'):
        self.win.update()

    def close(self):
        self.win.bye()

    def add_needy_person(self, x, y):
        needy_person = t.Turtle()
        needy_person.shape('circle')
        needy_person.color('black')
        needy_person.penup()
        needy_person.goto(x, y)
        self.needy_people.append(needy_person)
    
    def add_fire(self, x, y):
        fire = t.Turtle()
        fire.shape('circle')
        fire.color('yellow')
        fire.penup()
        fire.goto(x, y)
        self.fire_danger.append(fire)

# # Example usage:
# env = CustomRL_Environment()

# # Reinforcement Learning loop
# for i in range(10000):
#     logistics_action = random.randint(0, 3)
#     command_action = random.randint(0, 3)

#     obs, rewards, done, _ = env.step([logistics_action, command_action])
#     env.render()
#     if done:
#         print(f"Episode {i} finished")

# # After reinforcement learning loop, you can reset the environment if needed:
# env.close()
