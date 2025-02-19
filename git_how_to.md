to create an ssh-key u've got to use ssh-keygen command (firstly check whether u have any other ssh's or not: u can do it with "ls ~/.ssh").
next, u should add the ssh-key to your ssh-agent: "eval "$(ssh-agent -s)"
and add it with "ssh-add ~/.ssh/id_ed25519"

and then use some magic --> u can use your repo on your github acc ;)
