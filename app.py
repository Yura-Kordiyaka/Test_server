import time

from flask import Flask
from flask_caching import Cache

FILES_PATH = 'static/users_files'
app = Flask(__name__)
app.config['SECRET_KEY'] = '#cv)3v7w$*s3fk;5c!@y0?:?№3"9)#'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['MAX_FORM_MEMORY_SIZE'] = 1024 * 1024  # 1MB

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 30
app.config['CACHE_KEY_PREFIX'] = 'myapp_'
cache = Cache()
cache.init_app(app)

@app.route('/user/<int:user_id>')
@cache.cached(timeout=60)
def get_user_profile(user_id):
    data = cache.get(f'user_id_{user_id}')
    print(data)
    if data is not None:
        return f"Профіль користувача: {user_id}"
    else:
        cache.set(f"user_id_{user_id}", user_id, 60)
    time.sleep(2)
    return f"Профіль користувача: {user_id}"


@app.route('/clear-cache')
def clear_cache():
    cache.clear()
    return "Кеш очищено!"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
