To run the app, only python and uv and git are needed on the target system.

```
git clone https://github.com/ivelinhristovipsos/londemo.git
```

```
pip install uv
```
```
uv sync
```

After uv is installed, the streamlit server can be ran via:
```
uv run streamlit run target_python_file.py
```

For the time being, the entry point for app is homepage.py
