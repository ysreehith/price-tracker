# Deployment Guide for Price Tracker

This guide will help you deploy the Price Tracker application to Vercel.

## Project Structure

- **Frontend**: React app in `/frontend` directory
- **Backend**: FastAPI app in `/backend` directory

## Deployment Options

### Option 1: Frontend Only on Vercel (Recommended for now)

Since Vercel doesn't natively support Python backends, we'll deploy just the frontend to Vercel and host the backend separately.

#### Step 1: Deploy Backend to Railway/Render

1. **Railway** (Recommended):
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the `backend` folder as the root directory
   - Railway will automatically detect it's a Python app
   - Add environment variables if needed

2. **Render** (Alternative):
   - Go to [render.com](https://render.com)
   - Create a new Web Service
   - Connect your GitHub repository
   - Set root directory to `backend`
   - Add build command: `pip install -r requirements.txt`
   - Add start command: `python main.py`

#### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy from frontend directory**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variables**:
   - In Vercel dashboard, go to your project settings
   - Add environment variable: `REACT_APP_API_URL` = your backend URL (e.g., `https://your-backend.railway.app`)

### Option 2: Full Stack on Vercel (Advanced)

Convert the backend to Vercel serverless functions:

1. Create `/api` directory in the root
2. Convert FastAPI routes to Vercel functions
3. Deploy everything together

## Quick Start Commands

### Deploy Frontend to Vercel:

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - What's your project's name? price-tracker-frontend
# - In which directory is your code located? ./
```

### Environment Variables for Vercel:

In the Vercel dashboard, add:
- `REACT_APP_API_URL`: Your backend URL (e.g., `https://your-backend.railway.app`)

## Testing the Deployment

1. **Backend**: Visit `https://your-backend.railway.app/docs` to see the API documentation
2. **Frontend**: Visit your Vercel URL to see the React app
3. **Test**: Try adding a product URL to verify the connection works

## Troubleshooting

### CORS Issues
If you get CORS errors, update the backend's CORS settings in `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables
Make sure the `REACT_APP_API_URL` environment variable is set correctly in Vercel.

## Next Steps

1. Deploy backend to Railway/Render
2. Deploy frontend to Vercel
3. Update CORS settings if needed
4. Test the full application
5. Set up custom domain (optional)

## Cost Considerations

- **Vercel**: Free tier available for frontend
- **Railway**: $5/month for backend hosting
- **Render**: Free tier available for backend

Choose based on your needs and budget!
