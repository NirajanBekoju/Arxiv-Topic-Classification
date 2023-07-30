# Arxiv Topic Classification

## Abstract
In today’s information-rich world, scientific publications play a pivotal role in disseminating
knowledge and advancing research across various disciplines. The exponential growth of digital
repositories, such as arXiv, has made it increasingly challenging for researchers to keep up with
the vast volume of available literature. To address this challenge, we propose a novel approach
that harnesses the power of Kaggle datasets for arXiv paper topic classification and builds a
robust recommendation system.

## Data Source
- [Arxiv Datasets](https://www.kaggle.com/datasets/Cornell-University/arxiv)

## Reports and Slides
- [Proposal](https://github.com/NirajanBekoju/Arxiv-Topic-Classification-and-Paper-Recommendation-System/blob/main/Report/Proposal/main.pdf)

- [Proposal Presentation](https://github.com/NirajanBekoju/Arxiv-Topic-Classification-and-Paper-Recommendation-System/blob/main/Report/Slides/proposal.pptx.pdf)



## Steps to run in your local machine
**Clone the repository**

```
git clone https://github.com/NirajanBekoju/Arxiv-Topic-Classification-and-Paper-Recommendation-System
```

**Setup conda environment**

```
conda env create -f environment.yml
```

## Steps to run django app (Backend)
The backend is developed using django and django rest framework.

**Activate the conda environment**
```
conda activate aifellowship
```

**Run django server**
```
python3 manage.py runserver
```

## Steps to run react frontend
The frontend is developed using React. Node version : 19.9.0 and npm version : 9.6.3
**Install npm packages**
```
npm install 
```

**Run the server**
```
npm run start
```

## Status
- Currently Working On