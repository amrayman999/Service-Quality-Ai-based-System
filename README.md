# Service-Quality-Ai-based-System
### Service Quality Ai-based System is a cutting-edge platform designed to enhance customer service and support in various industries specifically in Arabic language. <br>
#### The main three tasks of the Plateform: 
<ul> 
    <li>Topic classification</li>
    <li>Sentiment Analysis</li> 
    <li>Solution Generation</li>
</ul> 
<br>
<h2>The deployment process is applied using frontend and 
backend development with Django framework.
</h2>
<table>
  <tr>
    <td><img src="Home.jpg" width=400 hieght=400/></td>
    <td><img src="Log-in.jpg" width=400 hieght=400/></td>
    <td><img src="Registration.jpg" width=400 hieght=400/></td>
  </tr>
  <tr>
    <td><img src="Complaint.jpg" width=400 hieght=400/></td>
    <td><img src="Adminstration.jpg" width=400 hieght=400/></td>
    <td><img src="About-team.jpg" width=400 hieght=400/></td>
  </tr>
  
</table>

---

## Used Models:
### ARBERT & MARBERT: Deep Bidirectional Transformers for Arabic
<img src="ARBERT_MARBERT.jpg" alt="drawing" width="30%" height="30%" align="right"/>

### What is the repository is about?
This is the repository accompanying our project [ARBERT & MARBERT: Deep Bidirectional Transformers for Arabic].
In the paper, we:
* introduce ```ARBERT``` and ```MARBERT```, two powerful Transformer-based language models for Arabic;
* introduce ```ArBench```, a multi-domain, multi-variety benchmark for Arabic naturaal language understanding based on 41 datasets across 5 different tasks and task clusters;
* evaluate ARBERT and MARBERT on ArBench and compare against available language models.

Our model establish new state-of-the-art (SOTA) on all 5 tasks/task clusters on 37 out of the 41 datasets.
Our language models are publicaly available for research (see below).
The rest of this repository provides more information about our new language models, benchmark, and experiments.
### How to use ARBERT and MARBERT

#### Loading directly from Huggingface
You can use ARBERT and MARBERT with [Hugging Face's Transformers](https://github.com/huggingface/transformers) library as follow.
 
 ```python
    from transformers import AutoTokenizer, AutoModel
    #load AEBERT model from huggingface
    ARBERT_tokenizer = AutoTokenizer.from_pretrained("UBC-NLP/ARBERT")
    ARBERT_model = AutoModel.from_pretrained("UBC-NLP/ARBERT")
  
    #load MAEBERT model from huggingface
    MARBERT_tokenizer = AutoTokenizer.from_pretrained("UBC-NLP/MARBERT")
    MARBERT_model = AutoModel.from_pretrained("UBC-NLP/MARBERT") 
 ```
### 4.2 Example: Fine-tuning MARBERT for Sentiment Analysis
MARBERT Fine-Tuning demo with PyTorch checkpoint for Sentiment Analysis on the AJGT dataset [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1M0ls7EPUi1dwqIDh6HNfJ5y826XvcgGX?usp=sharing)

