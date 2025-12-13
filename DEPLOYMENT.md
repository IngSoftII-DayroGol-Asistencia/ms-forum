# 🚀 Deployment Guide - Cloud Run CI/CD

This guide explains how to set up automated CI/CD for the `ms-forum` microservice using Google Cloud Run.

## 📋 Prerequisites

1. **Google Cloud Project** with billing enabled
2. **GitHub repository** connected to your project
3. **MongoDB Atlas** cluster (or Firestore with MongoDB API)

## 🔧 Initial Setup

### 1. Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Set Up Environment Variables

You need to configure the following secrets/variables in your CI/CD platform:

#### For Cloud Build Triggers:

1. Go to Cloud Build > Triggers in Google Cloud Console
2. Create a new trigger or edit existing one
3. Add substitution variables:
   - `_MONGO_URI`: Your MongoDB connection string
   - `_JWT_SECRET_KEY`: Your JWT secret key (generate with `openssl rand -hex 32`)
   - `_REGION`: Deployment region (default: `us-central1`)

#### For GitHub Actions:

1. Go to your GitHub repository > Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Service account JSON key (see below)
   - `MONGO_URI`: Your MongoDB connection string
   - `JWT_SECRET_KEY`: Your JWT secret key

### 3. Create Service Account (for GitHub Actions)

```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployment"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

# Copy the contents of key.json to GitHub secret GCP_SA_KEY
cat key.json
```

## 🎯 Deployment Methods

### Option 1: Cloud Build (Recommended for GCP-native CI/CD)

This method uses `cloudbuild.yaml` and Google Cloud Build triggers.

#### Set Up Trigger:

```bash
# Connect your repository first via Cloud Console, then:
gcloud builds triggers create github \
  --repo-name=ms-forum \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_MONGO_URI="your-mongo-uri",_JWT_SECRET_KEY="your-secret"
```

#### Manual Deployment:

```bash
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_MONGO_URI="your-uri",_JWT_SECRET_KEY="your-key"
```

### Option 2: GitHub Actions

This method uses `.github/workflows/deploy.yml` for CI/CD.

**Setup:**

1. Push code to `main` or `production` branch
2. GitHub Actions will automatically build and deploy
3. View progress in the Actions tab of your repository

**Manual Trigger:**

- Go to Actions > Deploy to Cloud Run > Run workflow

### Option 3: Manual Deployment

For quick deployments without CI/CD:

```bash
# Set environment variables
export PROJECT_ID=$(gcloud config get-value project)
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/forum_db"
export JWT_SECRET_KEY=$(openssl rand -hex 32)

# Deploy from source
gcloud run deploy ms-forum \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars MONGO_URI="${MONGO_URI}",JWT_SECRET_KEY="${JWT_SECRET_KEY}"
```

## 🔐 Security Best Practices

### Use Secret Manager (Recommended)

```bash
# Create secrets
echo -n "your-mongo-uri" | gcloud secrets create mongo-uri --data-file=-
echo -n "your-jwt-secret" | gcloud secrets create jwt-secret --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding mongo-uri \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Update cloudbuild.yaml or deploy command to use secrets
gcloud run deploy ms-forum \
  --image gcr.io/$PROJECT_ID/ms-forum:latest \
  --region us-central1 \
  --set-secrets MONGO_URI=mongo-uri:latest,JWT_SECRET_KEY=jwt-secret:latest
```

## 📊 Monitoring and Logs

### View Logs

```bash
# Stream logs
gcloud run services logs tail ms-forum --region us-central1

# View recent logs
gcloud run services logs read ms-forum --limit 100 --region us-central1
```

### Access Service

```bash
# Get service URL
gcloud run services describe ms-forum \
  --region us-central1 \
  --format 'value(status.url)'
```

## 🔄 Updating the Service

### Update Environment Variables

```bash
gcloud run services update ms-forum \
  --update-env-vars NEW_VAR=value \
  --region us-central1
```

### Scale Configuration

```bash
gcloud run services update ms-forum \
  --min-instances 1 \
  --max-instances 20 \
  --cpu 2 \
  --memory 1Gi \
  --region us-central1
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Error**: Ensure `PORT` env var is set to `8080` (Cloud Run default)
2. **Connection Timeout**: Check MongoDB Atlas network access (allow 0.0.0.0/0)
3. **Build Fails**: Review Cloud Build logs in GCP Console
4. **Deployment Fails**: Verify service account permissions

### Debug Commands

```bash
# Check service status
gcloud run services describe ms-forum --region us-central1

# View revisions
gcloud run revisions list --service ms-forum --region us-central1

# Rollback to previous revision
gcloud run services update-traffic ms-forum \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

## 📝 Configuration Files

- `cloudbuild.yaml` - Cloud Build configuration
- `.gcloudignore` - Files to exclude from deployment
- `.github/workflows/deploy.yml` - GitHub Actions workflow
- `Dockerfile` - Container configuration

## 🎓 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [GitHub Actions for GCP](https://github.com/google-github-actions)
