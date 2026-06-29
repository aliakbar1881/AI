import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt

class SmartHomeEnv(gym.Env):
    def __init__(self):
        super(SmartHomeEnv, self).__init__()

        self.time_steps_per_day = 96
        self.current_step = 0
        self.episode_length = self.time_steps_per_day

        self.indoor_temp = 20.0
        self.target_temp = 22.0
        self.outdoor_temp_base = 10.0
        self.heat_loss_coeff = 0.5
        self.hvac_heating_rate = 1.0
        self.hvac_heating_rate_strong = 2.0
        self.hvac_cooling_rate = 1.5

        self.battery_capacity = 10.0
        self.battery_level = 5.0
        self.max_charge_rate = 2.0
        self.battery_efficiency = 0.9

        self.solar_max = 3.0 

        self.price_peak = 0.30
        self.price_off_peak = 0.10

        self.action_space = spaces.Discrete(7)

        self.observation_space = spaces.Box(
            low=np.array([0.0, -10.0, 0.0, 0.0, 0.0, 0.0, 18.0]),
            high=np.array([40.0, 40.0, self.battery_capacity, self.solar_max, self.price_peak, 24.0, 26.0]),
            dtype=np.float32
        )

    def _get_outdoor_temp(self):
        hour = (self.current_step / 4) % 24  # هر 4 مرحله = 1 ساعت
        return self.outdoor_temp_base + 10 * np.sin(2 * np.pi * (hour - 6) / 24)

    def _get_solar_power(self):
        hour = (self.current_step / 4) % 24
        if 6 <= hour <= 18:
            return self.solar_max * np.sin(np.pi * (hour - 6) / 12)
        return 0.0

    def _get_price(self):
        hour = (self.current_step / 4) % 24
        if (7 <= hour <= 9) or (18 <= hour <= 20):
            return self.price_peak
        else:
            return self.price_off_peak

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.indoor_temp = 20.0
        self.battery_level = self.battery_capacity / 2  # شارژ اولیه 50%

        outdoor_temp = self._get_outdoor_temp()
        solar = self._get_solar_power()
        price = self._get_price()
        hour = (self.current_step / 4) % 24

        state = np.array([
            self.indoor_temp,
            outdoor_temp,
            self.battery_level,
            solar,
            price,
            hour,
            self.target_temp
        ], dtype=np.float32)

        return state, {}

    def step(self, action):
        self.current_step += 1

        outdoor_temp = self._get_outdoor_temp()
        solar_power = self._get_solar_power()
        electricity_price = self._get_price()
        hour = (self.current_step / 4) % 24

        energy_consumed = 0.0
        energy_from_grid = 0.0
        temp_change = 0.0

        if action == 0:
            pass
        elif action == 1:
            temp_change += self.hvac_heating_rate
            energy_consumed += 1.0
        elif action == 2:
            temp_change += self.hvac_heating_rate_strong
            energy_consumed += 2.0
        elif action == 3:
            temp_change -= self.hvac_cooling_rate
            energy_consumed += 1.5
        elif action == 4:
            charge = min(self.max_charge_rate, energy_consumed)
            energy_from_grid = charge
            self.battery_level = min(self.battery_capacity, self.battery_level + charge * self.battery_efficiency)
        elif action == 5:
            discharge = min(self.max_charge_rate, self.battery_level / self.battery_efficiency)
            self.battery_level -= discharge / self.battery_efficiency
            temp_change += self.hvac_heating_rate
            energy_consumed += discharge
        elif action == 6:
            pass

        temp_diff = outdoor_temp - self.indoor_temp
        self.indoor_temp += temp_change - self.heat_loss_coeff * temp_diff * (1/4)  # 15 دقیقه = 1/4 ساعت

        net_energy_needed = max(0, energy_consumed - solar_power)
        if action == 4:
            energy_from_grid = net_energy_needed
        else:
            energy_from_grid = max(0, net_energy_needed)

        cost = energy_from_grid * electricity_price

        temp_deviation = abs(self.indoor_temp - self.target_temp)
        comfort_penalty = 10 * temp_deviation
        cost_penalty = 100 * cost
        reward = -cost_penalty - comfort_penalty

        if action != 4 and solar_power > energy_consumed:
            surplus = (solar_power - energy_consumed)
            charge = min(self.max_charge_rate, surplus, (self.battery_capacity - self.battery_level) / self.battery_efficiency)
            self.battery_level += charge * self.battery_efficiency

        done = self.current_step >= self.episode_length
        truncated = False

        state = np.array([
            self.indoor_temp,
            outdoor_temp,
            self.battery_level,
            solar_power,
            electricity_price,
            hour,
            self.target_temp
        ], dtype=np.float32)

        info = {
            "cost": cost,
            "temp_deviation": temp_deviation,
            "solar_power": solar_power,
            "battery_level": self.battery_level,
            "energy_from_grid": energy_from_grid
        }

        return state, reward, done, truncated, info

    def render(self):
        print(f"Step {self.current_step}: Temp={self.indoor_temp:.1f}°C, "
              f"Battery={self.battery_level:.1f}kWh, Cost={self._get_price():.2f}$")


if __name__ == "__main__":
    env = SmartHomeEnv()
    obs, _ = env.reset()
    rewards = []
    temps = []
    battery_levels = []
    costs = []

    for _ in range(env.episode_length):
        action = env.action_space.sample()  # اقدام تصادفی
        obs, reward, done, truncated, info = env.step(action)
        rewards.append(reward)
        temps.append(obs[0])
        battery_levels.append(obs[2])
        costs.append(info["cost"])
        if done:
            break

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(temps, label="Indoor Temperature")
    plt.axhline(y=env.target_temp, color='r', linestyle='--', label="Target (22°C)")
    plt.ylabel("Temperature (°C)")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(battery_levels, label="Battery Level (kWh)", color='orange')
    plt.ylabel("Battery Level")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(np.cumsum(costs), label="Cumulative Cost ($)", color='red')
    plt.xlabel("Time Steps (15-min intervals)")
    plt.ylabel("Cumulative Cost")
    plt.legend()

    plt.tight_layout()
    plt.show()