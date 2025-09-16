if not contains "$HOME/Documents/IOA/Coral-Protocol/agents/Coral-Economics-Agent" $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$HOME/Documents/IOA/Coral-Protocol/agents/Coral-Economics-Agent" $PATH
end
