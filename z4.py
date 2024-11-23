import requests
import json
import random
from typing import Dict, Any, List


class RickAndMortyClient:
    BASE_URL = "https://rickandmortyapi.com/api"

    def get_random_character(self) -> Dict[str, Any]:
        response = requests.get(f"{self.BASE_URL}/character")
        data = json.loads(response.text)
        total_characters = data["info"]["count"]

        random_id = random.randint(1, total_characters)
        response = requests.get(f"{self.BASE_URL}/character/{random_id}")
        character = json.loads(response.text)

        return character

    def search_characters(self, name: str) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.BASE_URL}/character", params={"name": name})
        data = json.loads(response.text)

        if "results" in data:
            return data["results"]
        return []

    def get_all_locations(self) -> List[Dict[str, Any]]:
        locations = []
        url = f"{self.BASE_URL}/location"
        while url:
            response = requests.get(url)
            data = json.loads(response.text)
            locations.extend(data["results"])
            url = data["info"]["next"]  
        return locations

    def search_episodes(self, name: str) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.BASE_URL}/episode", params={"name": name})
        data = json.loads(response.text)

        if "results" in data:
            return data["results"]
        return []

    def analyze_character_status(self) -> Dict[str, int]:
        statuses = {"Alive": 0, "Dead": 0, "unknown": 0}
        url = f"{self.BASE_URL}/character"

        while url:
            response = requests.get(url)
            data = json.loads(response.text)
            for character in data["results"]:
                status = character["status"]
                if status in statuses:
                    statuses[status] += 1
            url = data["info"]["next"]  

        return statuses


client = RickAndMortyClient()
random_character = client.get_random_character()
print(f"Случайный персонаж: {random_character['name']}")
name = "Rick"
characters = client.search_characters(name)
print(f"Персонажи по имени '{name}': {[char['name'] for char in characters]}")

locations = client.get_all_locations()
print(f"Количество локаций: {len(locations)}")

episode_name = "Pilot"
episodes = client.search_episodes(episode_name)
print(f"Эпизоды по названию '{episode_name}': {[ep['name'] for ep in episodes]}")

character_statuses = client.analyze_character_status()
print("Статусы персонажей:", character_statuses)