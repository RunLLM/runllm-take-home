# Retrieval Augmented Generation Take Home

Contains starter code for the RunLLM Take Home interview.

## Development

1. Start a new GitHub Workspace. This will open a VSCode-like editor in your browser. We expect you to do your development here.
2. Obtain your API key from RunLLM. Go do `server/server/api_key.py` and set the `API_KEY` variable to your API key.
3. Run `source setup/setup.sh`. This will start the Elasticsearch and Ollama docker containers.
4. Run `make server` to start the server. You should see something like:
```bash
Starting server app...
INFO:     Will watch for changes in these directories: ['/workspaces/rag/server/server']
INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
INFO:     Started reloader process [2996] using StatReload
INFO:     Started server process [2998]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
5. Open a new terminal and attempt to chat with the server `api/chat` endpoint.
```bash
curl -X POST http://127.0.0.1:5001/api/chat --data '{"message": "hi"}' -H "Content-Type: application/json"
```

You should get the following response back:

```json
{
  "message":"example response",
  "data_source_ids":[
    "9a6584e4041f69a91fb4d0445eb997e3","f1f051ca587dcdccce3cac1ecf442cc7","59cb0b50d17febda2430502dd4722c40"
  ]
}
```
From now on, the server logs will be streamed to this terminal. The server will automatically detect
any changes to it's source code and reload itself, so **you will never need to manually restart it**.

6. Finally, let's verify that our LLM is working. Run `python examples/llm_client.py`. The verify the output:
```
Good day! I'm doing well, thank you for asking. How can I assist you today? Do you have a technical issue or question that requires my help?
[[-0.031731643, -0.04901344, -0.13550061, -0.010585614, 0.009690352, 0.027844097, ...]]
```


## Debugging
### Connection Error
If you leave the codespace idle for some amount of time and come back later, your docker container may be stopped by the workspace.
To restart them, run `docker restart elasticsearch`. The common failure messages we see for this:

`elastic_transport.ConnectionError: Connection error caused by: ConnectionError(Connection error caused by: ProtocolError(('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))))`

### Python Interpreter Error
Since the package manager `poetry` interally creates a `.venv/` folder in `server`, there might be a python binary issue if you are attempting to run any python process within a subdirectory. The common failure messages are: `server/.venv/bin/python: bad interpreter: No such file or directory`.

To resolve this, try to **run your command from the project root**. For example, instead of `cd tests && pytest .`, do `pytest tests/`.


## Running the Static Checkers

Run `make run-static-checks` to quickly apply type checks and linters to your code. Feel free to use this liberally as you develop!

You may ignore the warnings for now:
```
Warning: [tool.poetry.name] is deprecated. Use [project.name] instead.
Warning: [tool.poetry.version] is set but 'version' is not in [project.dynamic]. If it is static use [project.version]. If it is dynamic, add 'version' to [project.dynamic].
If you want to set the version dynamically via `poetry build --local-version` or you are using a plugin, which sets the version dynamically, you should define the version in [tool.poetry] and add 'version' to [project.dynamic].
Warning: [tool.poetry.description] is deprecated. Use [project.description] instead.
Warning: [tool.poetry.readme] is set but 'readme' is not in [project.dynamic]. If it is static use [project.readme]. If it is dynamic, add 'readme' to [project.dynamic].
If you want to define multiple readmes, you should define them in [tool.poetry] and add 'readme' to [project.dynamic].
Warning: [tool.poetry.authors] is deprecated. Use [project.authors] instead.
```

## Running the Test Suite

Run `make run-tests` to run the test suite in `/tests`. Ensure the server is running before you run the tests.
