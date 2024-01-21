# Incremental Backups with Git and Python

This script is designed to set up and manage backups using Git repositories. It provides the following functionality:

- **Initialization**: Sets up necessary repositories for backup by creating a Git repository in the source directory and creating destination repositories for backups. You can choose to add new destinations or overwrite existing ones. The initialization process also creates a `README.md` file with default content in the source directory and commits it to the source repository (the file you are reading now).

- **Commit**: Commits all files in the source directory and syncs the backups by pulling changes from the destination repositories. The commit message contains the current date and time.

- **Restore**: Displays available backup locations and allows you to select a backup location to restore from.

- **Info**: Displays available backup locations, Git information for the master location, and provides general help.

The script uses a JSON file (`backup_config.json`) to store the paths of the source directory and the destination directories.

To use the script, follow these steps:

1. Make sure you have Python and Git installed on your system.

2. Clone this repository to your system.

3. Install the necessary Python packages using the command `pip install -r requirements.txt`.

4. Run the script using either of the following commands:
   - `./backup.py` (will require you to make it executable with `chmod +x backup.py`)
   - `python backup.py`

5. Use the available commands (`init`, `commit`, `restore`, `info`, `help`) to set up backups, commit files, restore backups, and get information about backup locations.

**Note**: This script assumes that you have basic knowledge of Git and command line usage.
