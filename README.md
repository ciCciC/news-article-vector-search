# ⚡️ Blazing fast NRC search

<p align='center'>
  <img width='50%' src="/asset/preview.gif">
</p>

[EXPERIMENTAL]

The objective of this repo is to build a blazing fast semantic Neural search using a multilingual LLM and Qdrant (Quadrant) vector db. The following techs are used

- [Qdrant](https://qdrant.tech)
- [FastEmbed](https://github.com/qdrant/fastembed)
- [Sentence Transformer](https://www.sbert.net)
- [distiluse-base-multilingual-cased-v1](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1) (model)
  - generates aligned vector spaces, i.e., similar inputs in different languages are mapped close in vector space
  - 14 languages (incl. NL)
- [Scalar Quantization](https://qdrant.tech/articles/scalar-quantization/) (for faster inference time and memory efficiency)
  - 8-bit

## 📊 Data
The data was scraped by utilizing the NRC [scraper api](https://github.com/ciCciC/nrcnewsapi) given a set of categories. The result is a large amount of NRC articles > 6500.

## 🚀 Installation
```
pip install -r requirements.txt
```

## 📖 Usage

qdrant
```
http://localhost:6333
```

api
```
http://localhost:8000
```

web ui
```
index.html
```

swagger
```
http://localhost:8000/docs
```