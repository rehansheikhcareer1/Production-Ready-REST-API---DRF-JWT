# Deployment Guide

Step-by-step guide to deploy this API to production.

## Option 1: Render.com (Recommended - Free Tier Available)

### Prerequisites
- GitHub account
- Render account (free)

### Steps

1. **Prepare for Deployment**

Create `build.sh` in project root:
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

2. **Update settings.py**

Add to settings.py:
```python
import os
import dj_database_url

# Add this for Render
if 'RENDER' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
    
    # Database
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
```

3. **Add to requirements.txt**
```
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
```

4. **Deploy on Render**
- Push code to GitHub
- Go to Render Dashboard
- Click "New +" → "Web Service"
- Connect your repository
- Configure:
  - Name: ecommerce-api
  - Environment: Python 3
  - Build Command: `./build.sh`
  - Start Command: `gunicorn core.wsgi:application`
- Add Environment Variables:
  - SECRET_KEY
  - DATABASE_URL (auto-provided)
  - PYTHON_VERSION=3.11.0
- Click "Create Web Service"

## Option 2: PythonAnywhere

### Steps

1. **Upload Code**
```bash
# On PythonAnywhere console
git clone <your-repo-url>
cd ecommerce_api
```

2. **Create Virtual Environment**
```bash
mkvirtualenv --python=/usr/bin/python3.10 ecommerce_env
pip install -r requirements.txt
```

3. **Configure Web App**
- Go to Web tab
- Add new web app
- Choose Manual configuration
- Python 3.10

4. **Configure WSGI File**
```python
import os
import sys

path = '/home/yourusername/ecommerce_api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Set Environment Variables**
In Web tab → Environment variables section

6. **Configure Static Files**
- URL: /static/
- Directory: /home/yourusername/ecommerce_api/staticfiles/

7. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

8. **Reload Web App**

## Option 3: Railway.app

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login and Deploy**
```bash
railway login
railway init
railway up
```

3. **Add Environment Variables**
```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
```

## Option 4: Heroku

1. **Install Heroku CLI**

2. **Create Procfile**
```
web: gunicorn core.wsgi
release: python manage.py migrate
```

3. **Deploy**
```bash
heroku login
heroku create ecommerce-api-rehan
git push heroku main
heroku run python manage.py createsuperuser
```

## Production Checklist

### Security
- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set up CORS properly
- [ ] Use environment variables for sensitive data

### Database
- [ ] Use PostgreSQL/MySQL in production
- [ ] Set up database backups
- [ ] Configure connection pooling

### Performance
- [ ] Enable caching (Redis)
- [ ] Use CDN for static files
- [ ] Optimize database queries
- [ ] Set up monitoring

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Monitor API performance

## Environment Variables for Production

```env
# Django
SECRET_KEY=<generate-strong-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Or MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=ecommerce_db
DB_USER=db_user
DB_PASSWORD=strong_password
DB_HOST=db_host
DB_PORT=3306

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Post-Deployment

1. **Test All Endpoints**
```bash
# Update BASE_URL to your production URL
python test_api.py
```

2. **Create Admin User**
```bash
python manage.py createsuperuser
```

3. **Load Sample Data** (optional)
```bash
python manage.py loaddata sample_data.json
```

4. **Monitor Logs**
```bash
# Render
render logs

# Heroku
heroku logs --tail

# PythonAnywhere
# Check error log in Web tab
```

## Troubleshooting

### Static Files Not Loading
```python
# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add whitenoise to middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest
]
```

### Database Connection Issues
- Check DATABASE_URL format
- Verify database credentials
- Ensure database server is accessible

### CORS Errors
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Custom Domain Setup

1. **Add Domain to Hosting Provider**
2. **Update DNS Records**
```
Type: A
Name: @
Value: <server-ip>

Type: CNAME
Name: www
Value: yourdomain.com
```
3. **Update ALLOWED_HOSTS**
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## SSL Certificate

Most platforms (Render, Heroku, Railway) provide free SSL automatically.

For custom setup:
- Use Let's Encrypt (free)
- Or use Cloudflare (free tier)

## Backup Strategy

1. **Database Backups**
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# MySQL
mysqldump -u user -p dbname > backup.sql
```

2. **Media Files**
- Use cloud storage (AWS S3, Cloudinary)
- Set up automated backups

## Performance Optimization

1. **Enable Caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database Optimization**
- Add indexes
- Use select_related() and prefetch_related()
- Enable query caching

3. **Use CDN**
- Cloudflare (free)
- AWS CloudFront
- Cloudinary for images

## Monitoring Tools

- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **UptimeRobot** - Uptime monitoring
- **Papertrail** - Log management

---

**Note**: Always test in staging environment before deploying to production!
