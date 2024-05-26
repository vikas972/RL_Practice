import turtle as t
import random


class RL_Environment():
    def __init__(self):
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
        self.fire_appearance_delay = 5000
        self.needy_appearance_delay = 3000

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


    # Method to add needy people
    def add_needy_person(self, x, y):
        needy_person = t.Turtle()
        needy_person.shape('circle')
        needy_person.color('black')
        needy_person.penup()
        needy_person.goto(x, y)
        self.needy_people.append(needy_person)
    
    # Method to add Fire
    def add_fire(self, x, y):
        fire = t.Turtle()
        fire.shape('circle')
        fire.color('yellow')
        fire.penup()
        fire.goto(x, y)
        self.fire_danger.append(fire)

    # Method to visualize the environment
    def visualize(self):
        self.win.update()

    # Method to reset environment
    def reset(self):
        for needy_person in self.needy_people:
            needy_person.goto(1000, 1000)  # Move off-screen
        self.needy_people = []
        for fire in self.fire_danger:
            fire.goto(1000, 1000)  # Move off-screen
        self.needy_people = []
        self.fire_danger = []

    # Method to step in the environment
    def step(self, logistics_action, command_action):
        logistics_reward = 0
        command_reward = 0
        done = False

        # Logistics and Supply Agent Logic
        if logistics_action == 0:  # Move left
            x = self.logistics_agent.xcor()
            if x > -300:
                self.logistics_agent.setx(x - 20)
        elif logistics_action == 1:  # Move right
            x = self.logistics_agent.xcor()
            if x < 300:
                self.logistics_agent.setx(x + 20)
        elif logistics_action == 2:  # Move up
            y = self.logistics_agent.ycor()
            if y < 300:
                self.logistics_agent.sety(y + 20)
        elif logistics_action == 3:  # Move down
            y = self.logistics_agent.ycor()
            if y > -300:
                self.logistics_agent.sety(y - 20)

        # Command and Control Agent Logic
        if command_action == 0:  # Move left
            x = self.command_agent.xcor()
            if x > -300:
                self.command_agent.setx(x - 20)
        elif command_action == 1:  # Move right
            x = self.command_agent.xcor()
            if x < 300:
                self.command_agent.setx(x + 20)
        elif command_action == 2:  # Move up
            y = self.command_agent.ycor()
            if y < 300:
                self.command_agent.sety(y + 20)
        elif command_action == 3:  # Move down
            y = self.command_agent.ycor()
            if y > -300:
                self.command_agent.sety(y - 20)

        # Needy People Logic

        for needy_person in self.needy_people:
            # Check if logistics agent is near to needy person
            if abs(needy_person.xcor() - self.logistics_agent.xcor()) < 20 and abs(needy_person.ycor() - self.logistics_agent.ycor()) < 20:
                logistics_reward += 1
                self.needy_people.remove(needy_person)
                needy_person.goto(1000, 1000)  # Move off-screen

        for fire in self.fire_danger:
            # Check if command agent is near to fire
            if abs(fire.xcor() - self.command_agent.xcor()) < 20 and abs(fire.ycor() - self.command_agent.ycor()) < 20:
                command_reward += 1
                self.fire_danger.remove(fire)
                fire.goto(1000, 1000)  # Move off-screen

        # Add new needy person randomly
        if random.randint(1, self.needy_appearance_delay) == 1:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            self.add_needy_person(x, y)

        # Add new fire randomly
        if random.randint(1, self.fire_appearance_delay) == 1:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            self.add_fire(x, y)



        return logistics_reward, command_reward, done
    

# Example usage:
env = RL_Environment()

# Reinforcement Learning loop
for i in range(1000):
    # Random actions for demonstration
    logistics_action = random.randint(0, 3)  # 0: left, 1: right, 2: up, 3: down
    command_action = random.randint(0, 3)  # 0: left, 1: right, 2: up, 3: down

    logistics_reward, command_reward, done = env.step(logistics_action, command_action)
    env.visualize()
    if done:
        print(f"Episode {i} finished")

# After reinforcement learning loop, you can reset the environment if needed:
env.reset()
