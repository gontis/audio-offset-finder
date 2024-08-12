#!/bin/bash

# Determine which shell is being used
current_shell=$(basename "$SHELL")

# Function to update the PATH in the appropriate shell configuration file
update_path() {
    config_file=$1
    path_entry='export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"'

    # Check if the path is already in the configuration file
    if grep -Fxq "$path_entry" "$config_file"; then
        echo "PATH already updated in $config_file."
    else
        # Add the path entry to the configuration file
        echo "$path_entry" >> "$config_file"
        echo "PATH updated in $config_file."
    fi

    # Reload the configuration file
    source "$config_file"
}

# Determine which configuration file to update based on the shell
case "$current_shell" in
    zsh)
        update_path "$HOME/.zshrc"
        ;;
    bash)
        # Check for .bash_profile or .bashrc, create if missing
        if [ -f "$HOME/.bash_profile" ]; then
            update_path "$HOME/.bash_profile"
        else
            update_path "$HOME/.bashrc"
        fi
        ;;
    *)
        echo "Unsupported shell: $current_shell"
        echo "Please update your PATH manually."
        exit 1
        ;;
esac

# Verify that the PATH has been updated and print the result
echo "Current PATH: $PATH"
echo "Verification of pip and python:"

# Verify the installation of Python and pip
python_version=$(python --version 2>&1)
pip_version=$(pip --version 2>&1)

echo "$python_version"
echo "$pip_version"
