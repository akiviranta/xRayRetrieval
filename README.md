# xRayRetrieval

## Overview
xRayRetrieval helps medical professionals query and compare X-ray images and diagnoses. It uses a modified version of **CheXpert dataset** and a **fine-tuned CLIP model** for image retrieval.

All the modifications were made on kaggle and can be seen in the jupyter notebook named CAPSTONEPROJECT.

## Current Status
- **Embeddings were generated using the fine-tuned CLIP model**, but the current code may still use the original model.
- **Note:** The `node_modules` folder was mistakenly pushed to GitHub—clean it up before use (i could do it myself but no:))).

## Setup
```bash
rm -rf frontend/node_modules
cd frontend && npm install  # or yarn install
cd ../backend && pip install -r requirements.txt
```

## How It Works
1. X-ray images are encoded using the fine-tuned CLIP model.
2. Users input an image or text query.
3. The system retrieves relevant X-rays based on embeddings.
4. The current code probably uses the og model for running inference that is fine. The finetuning only matters when
   creating the embeddings

## Next Steps
- Maybe add some type of object recognition model on top of this to highlight the areas of note
- When returning the nearest neighbors it would be cool to also return the images w the diagnoses
  but it took too much space in the DB and this is a school project so I wont be buying
  cloud storage:)
- More data/compute --> better results? 

