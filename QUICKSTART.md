# 🚀 Quick Start - CI/CD Deployment

## For Cloud Build (GCP Native)

### 1. Connect Repository

Go to Cloud Build > Triggers > Connect Repository (Google Cloud Console)

### 2. Create Trigger

```bash
gcloud builds triggers create github \
  --repo-name=ms-forum \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### 3. Add Secrets to Trigger

In Cloud Console > Cloud Build > Triggers > Edit your trigger:

- Add `_MONGO_URI` = your MongoDB connection string
- Add `_JWT_SECRET_KEY` = your JWT secret (use `openssl rand -hex 32`)

### 4. Push to Trigger

```bash
git push origin main
```

---

## For GitHub Actions

### 1. Add Secrets to GitHub

Repository > Settings > Secrets > Actions:

- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Service account JSON (see DEPLOYMENT.md)
- `MONGO_URI`: Your MongoDB connection string
- `JWT_SECRET_KEY`: Your JWT secret

### 2. Push to Deploy

```bash
git push origin main
```

---

## Manual Deployment

```bash
gcloud run deploy ms-forum \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars MONGO_URI="your-uri",JWT_SECRET_KEY="your-key"
```

---

📖 **Full Documentation**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
