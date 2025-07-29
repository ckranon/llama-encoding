# Llama Encoding: TODO.md

My current problem is trying to evaluate these parliamentary speeches and prompts with
a model with HuggingFace, but with the help of some cloud platform like Google Collab.

I'll need to redownload the data from my database in postgres, `emolex_dict` and output
the files in some kind of structure like this:

    data/ <- main directory
        | - - <id>.txt

    Where <id> is the prompt id of the combinied query on the `gpt_o4_prompts` table and the `gpt_o4_raw_outputs` on the following columns

    1. gpt_o4_prompts.id as prompts
    2. gpt_o4_raw_output.response_id as responses

This should be a LEFT JOIN, and yield

    1. prompts.text_id
    2. responses.response_text

Remember to coerce responses.id to a integer. It's already numeric but prompts's primary keyis an integer.


- - - > [ ] git init

    email: ckranon@gmail.com
    name: Christian Ranon

    llama-encoding/
    | - - TODO.md (this file)
    | - - requirements.txt
    | - - main.py
    | - - data/
           | - - <id>.txt
           | . . .
    | - - modules/
           | - - extract.py
           | - - deps.nix

- - - > [ ] extract.py

Connects to my local postgres database with psycopg2, queries for the data previously mentioned, and outputs a folder with the text promptand id as the name.

I use NixOS to hose my database, so I can just write this with a shell.nix file. I don't have a sufficient command over nix's grammar and syntax, so I just went to the nix-man page of Python for its sample developer's environment. The only package necessary would be pyscopg2 so I can connect to my database.

Steps:

1. Establish Connection
2. Execute Query
3. While there are rows in my query, go through each row and output in the data/ directory the prompt text in a file called <id>.txt

- - - > [ ] main.py

- - - > [ ] Final Upload into Google Collab

    Expected Cell Commands

    ```{python}
    1. download repository
    2. upload data folder
    3. run script
    4. extract
    ```
