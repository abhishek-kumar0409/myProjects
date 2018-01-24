# myProjects

Tree-structure for Openai-gym-sdn::
---------------------------------
gym-sdn/
├── gym-sdn
│   ├── envs
│   │   ├── __init__.py
│   │   └── sdn_env.py
│   └── __init__.py
├── README.md
└── setup.py

GymTutorial
https://www.oreilly.com/learning/introduction-to-reinforcement-learning-and-openai-gym

self.observation_space = spaces.Dict({"position": spaces.Discrete(2), "velocity": spaces.Discrete(3)})
    Example usage [nested]:
    self.nested_observation_space = spaces.Dict({
        'sensors':  spaces.Dict({
            'position': spaces.Box(low=-100, high=100, shape=(3)),
            'velocity': spaces.Box(low=-1, high=1, shape=(3)),
            'front_cam': spaces.Tuple((
                spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                spaces.Box(low=0, high=1, shape=(10, 10, 3))
            )),
            'rear_cam': spaces.Box(low=0, high=1, shape=(10, 10, 3)),
        }),





self.observation_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(3)))


self.observation_space = spaces.Dict({ 'ap':  spaces.Dict({ 'position': spaces.Tuple((spaces.Discrete(400),spaces.Discrete(400))) }), 'sta1':  spaces.Dict({ 'position': spaces.Tuple((spaces.Discrete(400),spaces.Discrete(400))), 'sigStrength': spaces.Discrete(100) }), 'sta2':  spaces.Dict({ 'position': spaces.Tuple((spaces.Discrete(400),spaces.Discrete(400))), 'sigStrength': spaces.Discrete(100) }) })

{'ap':{'position':(10,10)},'sta1':{'position':(30,40),'sigStrength':60}}
