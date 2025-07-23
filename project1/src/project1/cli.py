"""CLI interface using Click."""

import click

from .main import APIClient, User


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Example CLI application."""
    pass


@cli.command()
@click.argument("user_id", type=int)
@click.option("--base-url", default="https://jsonplaceholder.typicode.com", 
              help="Base URL for the API")
def get_user(user_id: int, base_url: str):
    """Get user information by ID."""
    client = APIClient(base_url)
    user_data = client.get_user(user_id)
    
    if user_data:
        user = User(**user_data)
        click.echo(f"User ID: {user.id}")
        click.echo(f"Name: {user.name}")
        click.echo(f"Email: {user.email}")
        click.echo(f"Active: {user.active}")
    else:
        click.echo(f"User {user_id} not found", err=True)


@cli.command()
@click.option("--count", default=5, help="Number of users to list")
@click.option("--base-url", default="https://jsonplaceholder.typicode.com",
              help="Base URL for the API")
def list_users(count: int, base_url: str):
    """List multiple users."""
    client = APIClient(base_url)
    
    click.echo(f"Fetching {count} users...")
    for i in range(1, count + 1):
        user_data = client.get_user(i)
        if user_data:
            user = User(**user_data)
            click.echo(f"{user.id}: {user.name} ({user.email})")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
