"""Main module with example functionality."""

import asyncio
from typing import Optional

import aiohttp
import requests
from pydantic import BaseModel


class User(BaseModel):
    """Example user model using Pydantic."""
    id: int
    name: str
    email: str
    active: bool = True


class APIClient:
    """Example API client using requests."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user data from API."""
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user: {e}")
            return None


class AsyncAPIClient:
    """Example async API client using aiohttp."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def get_user_async(self, user_id: int) -> Optional[dict]:
        """Get user data from API asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/users/{user_id}") as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching user: {e}")
            return None


def process_users(users_data: list) -> list[User]:
    """Process raw user data into User models."""
    return [User(**user_data) for user_data in users_data]


async def main():
    """Example main function."""
    # Sync example
    client = APIClient("https://jsonplaceholder.typicode.com")
    user_data = client.get_user(1)
    
    if user_data:
        user = User(**user_data)
        print(f"User: {user.name} ({user.email})")
    
    # Async example
    async_client = AsyncAPIClient("https://jsonplaceholder.typicode.com")
    async_user_data = await async_client.get_user_async(2)
    
    if async_user_data:
        async_user = User(**async_user_data)
        print(f"Async User: {async_user.name} ({async_user.email})")


if __name__ == "__main__":
    asyncio.run(main())
