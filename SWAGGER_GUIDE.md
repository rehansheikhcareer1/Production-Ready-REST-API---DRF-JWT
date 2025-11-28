# Swagger UI - Complete Guide

## ⚠️ Important: Login Button Ko Ignore Karo!

Swagger UI mein jo "Log in" button dikhta hai, **wo Django admin ke liye hai, API ke liye nahi!**

Us button ko click mat karo - wo error dega.

## ✅ Sahi Tarika - API Authentication

### Step 1: Register Ya Login Karo

#### Option A: Naya User Register Karo

1. Swagger UI kholo: http://127.0.0.1:8000/swagger/
2. Scroll karke **`POST /api/auth/register/`** dhundo
3. "Try it out" button click karo
4. Request body mein ye data dalo:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Test@123",
  "password2": "Test@123",
  "role": "customer"
}
```

5. "Execute" button click karo
6. Response mein **access token** milega - isko copy karo!

#### Option B: Existing User Se Login Karo

1. **`POST /api/auth/login/`** endpoint dhundo
2. "Try it out" click karo
3. Credentials dalo:

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

4. "Execute" click karo
5. Response mein **access** aur **refresh** tokens milenge
6. **access token** copy karo

### Step 2: Token Ko Swagger Mein Add Karo

1. Page ke **top-right corner** mein **"Authorize"** button dhundo (🔓 lock icon)
2. Button click karo
3. Popup window khulega
4. **Value** field mein type karo:
   ```
   Bearer YOUR_ACCESS_TOKEN_HERE
   ```
   
   Example:
   ```
   Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk...
   ```

5. **"Authorize"** button click karo
6. **"Close"** karo

### Step 3: Test Karo!

Ab aap **koi bhi endpoint** test kar sakte ho! 🎉

Try these:
- `GET /api/auth/profile/` - Apna profile dekho
- `GET /api/products/` - Products list dekho
- `POST /api/products/create/` - Product banao (vendor/admin only)
- `POST /api/orders/create/` - Order place karo

## 🎯 Quick Test Flow

```
1. Register → Copy access token
2. Click "Authorize" button (top-right)
3. Paste: Bearer YOUR_TOKEN
4. Click "Authorize"
5. Test any endpoint!
```

## 📝 Test Credentials

**Admin User:**
- Email: `admin@example.com`
- Password: `admin123`

**Create Your Own:**
- Use `/api/auth/register/` endpoint

## ❌ Common Mistakes

1. ❌ **Login button click karna** - Ye Django admin ke liye hai
2. ❌ **Token ke aage "Bearer" nahi likhna** - Zaroor likho!
3. ❌ **Purana token use karna** - Token 1 hour mein expire hota hai
4. ❌ **Authorize kiye bina endpoint test karna** - Pehle authorize karo

## ✅ Correct Way

1. ✅ Register/Login endpoint use karo
2. ✅ Token copy karo
3. ✅ "Authorize" button use karo
4. ✅ "Bearer TOKEN" format mein paste karo
5. ✅ Endpoints test karo

## 🔄 Token Expire Ho Gaya?

Agar token expire ho gaya (1 hour ke baad), to:

1. **Option 1:** Phir se login karo (`/api/auth/login/`)
2. **Option 2:** Refresh token use karo (`/api/auth/token/refresh/`)

## 🎓 Pro Tips

- Token ko notepad mein save kar lo testing ke liye
- Swagger UI mein "Authorize" ek baar karo, phir sab endpoints work karenge
- Admin panel alag hai: http://127.0.0.1:8000/admin/
- Swagger UI sirf API testing ke liye hai

## 📸 Visual Guide

```
Swagger UI Page
├── Top Bar
│   ├── API Title
│   └── [Authorize] Button ← YE USE KARO! 🔓
│
├── Endpoints List
│   ├── auth
│   │   ├── POST /api/auth/register/ ← PEHLE YE
│   │   ├── POST /api/auth/login/    ← YA YE
│   │   └── GET /api/auth/profile/
│   ├── products
│   └── orders
│
└── Bottom
    └── [Log in] Button ← YE IGNORE KARO! ❌
```

## 🆘 Still Having Issues?

1. Check if server is running: http://127.0.0.1:8000/
2. Try admin panel: http://127.0.0.1:8000/admin/
3. Check token format: Must start with "Bearer "
4. Try registering a new user
5. Check browser console for errors

---

**Remember:** Swagger UI ka login button **ignore** karo! API authentication ke liye **Authorize button** use karo! 🔐
