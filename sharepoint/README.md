# Setup environment
```sh
pip install -r requirements.txt
```
# Create credentials
This demo requires crendentails when regsitering the app in `App Registration` at https://portal.azure.com/ as follows:
- Application (client) ID;
- Directory (tenant) ID;
- Client secret.
Then provide credentitals by editing the `config.cfg` file
# Setup permissions
Grant consented permissions for `Microsoft Graph` in `API permissions` in `App Registration` as follows:
- Files.Read.All;
- Sites.Read.All.
# How to
```sh
python main.py
```
Steps:
1. Find site id
1. Find drive id
1. Find drive root id
1. Find items

# References
https://learn.microsoft.com/en-us/graph/overview
https://developer.microsoft.com/en-us/graph/graph-explorer