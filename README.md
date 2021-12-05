# Map of Russian OSINT and Infosec Resources

This is just-for-fun online map of Russian OSINT and InfoSecurity resources: authors, telegram channels, telegram groups, youtube channels, etc.

Rendered graph is available here https://grablab.org/ru-osint-infosec/ This web page is rendered automatically with github pages engine and is linked to "index.html file in this repository.

Fell free to submit pull requests with new graph items.

## How to submit pull request

* Clone repo to your dev machine
* Update "data/nodes.json" file with new items
* Do not forget to place new items' logo files into "static/logo" directory
* Run `python3 do.py compile` to rebuild JS file which used to render graph
* Open index.html in browser and check everything is OK
* Commit changes (including logo files), upload commit to github and create pull request
