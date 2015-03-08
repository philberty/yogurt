#!/usr/bin/env python3

from Yogurt import AppCache
from Yogurt.Routes import app

app.config.from_pyfile('../etc/yogurt/yogurt.py')
AppCache.CacheServer = AppCache.CacheSystem(app.config['APP_CACHE'])

if __name__ == "__main__":
    app.run(debug=True)
