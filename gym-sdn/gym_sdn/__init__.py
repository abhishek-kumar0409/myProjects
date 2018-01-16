from gym.envs.registeration import register

register(
    id='sdn-v0',
    entry_point='gym_sdn.envs:SdnEnv',
)

