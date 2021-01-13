#!/bin/zsh

# # Prereq libraries
# # ----------------
# brew install --cask google-cloud-sdk
# # add to path via brew instructions
# pip install --upgrade google-cloud-storage

# # First time setup
# # ----------------
# gcloud auth login --no-launch-browser
# gcloud projects create simplelist
# gcloud config set project simplelist
# gcloud config set run/region us-east1
# gcloud beta billing projects link simplelist --billing-account=ACCOUNT_ID
# gcloud auth application-default login --no-launch-browser
# python -c 'from google.cloud import storage; c = storage.Client(); c.create_bucket("simplelist_datastore")'

# # Upload and Deploy Container
# # ---------------------------
# gcloud builds submit --tag gcr.io/simplelist/simplelistcont
gcloud run deploy simplelistcont --image gcr.io/simplelist/simplelistcont --platform managed --region us-east1 --max-instances 20
