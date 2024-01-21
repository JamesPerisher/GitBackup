#!/usr/bin/env python

from datetime import datetime
import subprocess
import shutil
import click
import json
import git
import os


def is_repo(directory):
    try:
        git.Repo(directory)
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

@click.group()
def backup():
    pass


# Get the path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
backup_config = os.path.join(current_dir, "backup_config.json")

# Check if the file already exists
if not os.path.exists(backup_config):
    # Create the file
    with open(backup_config, "w") as f:
        f.write("{}")

@backup.command()
@click.argument('source', type=click.Path(file_okay=False))
@click.argument('destinations', type=click.Path(file_okay=False), nargs=-1)
@click.option('-f', '--force', is_flag=True, help='Force overwrite existing JSON file')
@click.option('-a', '--add', is_flag=True, help='Add destinations instead of overwriting existing ones')
def init(*args, **kwargs):
    return _init(*args, **kwargs)
def _init(source, destinations, force, add):
    """
    Sets up necessary repositories for backup.

    SOURCE: Backup source directory.
    DESTINATIONS: Directories where backups will be stored.
    """
       
    click.echo(f"Setting up backup repositories for {source}...")
    
    # Create the source directory if it doesn't exist
    if not os.path.exists(source):
        os.makedirs(source)
        click.echo(f"Created source directory: {source}")

    # Check if the directory is already a Git repo
    if is_repo(source):
        if force and add:
            click.echo("Error: Cannot use -f and -a flags together!")
            return
        elif add:
            click.echo(f"Warning: Directory {source} is already a Git repository. Adding new destinations.")
        elif force:
            click.echo(f"Warning: Directory {source} is already a Git repository. Overwriting destinations.")
        else:
            click.echo(f"Warning: Directory {source} is already a Git repository. Use -f flag to force overwrite its destinations or -a to add new destinations.")
            return
    
    else:
        # Create a Git repository in the source directory if it doesn't exist
        source_repo = git.Repo.init(source)

        # Check if a README.md already exists in the source directory otherwise create one with default content
        if not os.path.exists(os.path.join(source, 'README.md')):
            shutil.copy("README.md", os.path.join(source, 'README.md'))

        # Add and commit the README.md to the source repository with commit message "Initial Backup Commit"
        source_repo.index.add("README.md")
        source_repo.index.commit('Initial Backup Commit')

        # Display a message confirming the initialization of the Git repository
        click.echo(f"Initialized Git repository in source directory: {source}")

    # Load the existing JSON file into a dictionary
    with open(backup_config) as config_file:
        paths = json.load(config_file)
    
    if add:
        # Add new destinations without overwriting existing ones
        if source in paths:
            paths[source].extend(destinations)
        else:
            paths[source] = destinations
    else:
        # Overwrite existing destinations with new ones
        paths[source] = destinations
    
    # Write the updated dictionary back to the JSON file
    with open(backup_config, 'w') as config_file:
        json.dump(paths, config_file)
    
    for dest in destinations:
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest):
            os.makedirs(dest)
            click.echo(f"Created destination directory: {dest}")
        
        # Check if the directory is already a Git repo
        if is_repo(dest):
            click.echo(f"Warning: Directory {dest} is already a Git repository. This destination will be ignored!")
            continue
        
        # Create a Git repository in each destination directory
        dest_repo = git.Repo.init(dest)
        click.echo(f"Initialized Git repository in destination directory: {dest}")
        
        # Set the source directory as the origin for each destination
        raw_source_dir = os.path.join(os.getcwd(), source, ".git") # cos git doesnt like the relative path
        origin = dest_repo.create_remote('origin', url=f"file://{raw_source_dir}")
        origin.fetch()
        dest_repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        dest_repo.remotes.origin.pull()

    click.echo("Setup complete!")


@backup.command()
@click.argument('source', required=False, type=click.Path(exists=True, file_okay=False))
def commit(*args, **kwargs):
    return _commit(*args, **kwargs)
def _commit(source):
    """Commits all files in the source directory and syncs the backups."""

    with open(backup_config) as config_file:
        paths = json.load(config_file)

    # If no source directory is provided
    if not source:
        if len(paths) == 0:
            click.echo("No source directory found in config!")
            return
        elif len(paths) == 1:
            source = list(paths.keys())[0]
        else:
            source = click.prompt("Select a source directory:", type=click.Choice(paths.keys()))

    # Get the destination directories from the config
    if source not in paths:
        click.echo(f"No destinations found for source directory: {source}!")
        return
    destinations = paths[source]

    # Commit files in the source directory with commit message containing date and time
    source_repo = git.Repo(source)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    source_repo.index.add(source_repo.untracked_files)
    source_repo.index.commit(f"Backup: {timestamp}")

    # Sync the backups
    for dest in destinations:
        dest_repo = git.Repo(dest)
        dest_repo.remotes.origin.pull()

    click.echo("Backup committed and synced!")


@backup.command()
def restore(*args, **kwargs):
    return _restor(*args, **kwargs)
def _restore():
    """Displays and allows selecting a backup location to restore from."""
    click.echo("Available backup locations:")
    # Place your implementation here to display available backup locations
    
    # Simulating selection of a backup location
    selected_location = click.prompt("Select a backup location", type=click.Choice(['location1', 'location2', 'location3']))
    click.echo(f"Restoring from backup location: {selected_location}")


@backup.command()
def info():
    """Displays available backup locations, Git info for the master location, and provides general help."""
    click.echo("Available backup locations:")
    # Place your implementation here to display available backup locations
    
    click.echo("Git info for master location:")
    # Place your implementation here to print Git info for the master location
    
    click.echo("For help, refer to the documentation or contact support.")


if __name__ == '__main__':
    backup()
