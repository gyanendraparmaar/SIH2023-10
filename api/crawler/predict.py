from __future__ import annotations
import numpy as np
import pandas as pd 
from datasets import load_dataset, load_from_disk
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import LongformerTokenizer, LongformerForMultipleChoice
import transformers
import pandas as pd
import pickle
import numpy as np
from tqdm import tqdm
import unicodedata
import os, time
import gc
import pandas as pd
import numpy as np
import re
from tqdm.auto import tqdm
import blingfire as bf
from collections.abc import Iterable
import torch
import ctypes
libc = ctypes.CDLL("libc.so.6")
from dataclasses import dataclass
from typing import Optional, Union
import torch
import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer
from transformers import AutoModelForMultipleChoice, TrainingArguments, Trainer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy
from torch.utils.data import DataLoader
from scipy.special import softmax
import os
import evaluate
import numpy as np
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import DataCollatorWithPadding
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


departments = [
    "Department for Promotion of Industry and Internal Trade",
    "Department of Administrative Reforms and Public Grievances (DARPG)",
    "Department of Agricultural Research and Education (DARE)",
    "Department of Agriculture and Farmers Welfare",
    "Department of Animal Husbandry and Dairying",
    "Department of Biotechnology",
    "Department of Border Management",
    "Department of Chemicals and Petrochemicals",
    "Department of Commerce",
    "Department of Consumer Affairs",
    "Department of Defence",
    "Department of Defence Production",
    "Department of Defence Research & Development",
    "Department of Drinking Water and Sanitation",
    "Department of Economic Affairs",
    "Department of Empowerment of Persons with Disabilities",
    "Department of Ex-Servicemen Welfare",
    "Department of Expenditure",
    "Department of Fertilizers",
    "Department of Financial Services",
    "Department of Fisheries",
    "Department of Food and Public Distribution",
    "Department of Health Research",
    "Department of Health and Family Welfare",
    "Department of Higher Education",
    "Department of Home",
    "Department of Investment and Public Asset Management",
    "Department of Justice",
    "Department of Land Resources (DLR)",
    "Department of Legal Affairs",
    "Department of Military Affairs (DMA)",
    "Department of Official Language",
    "Department of Pension & Pensioner's Welfare",
    "Department of Personnel and Training",
    "Department of Pharmaceuticals",
    "Department of Posts",
    "Department of Public Enterprises",
    "Department of Revenue",
    "Department of Rural Development (DRD)",
    "Department of School Education and Literacy",
    "Department of Science and Technology",
    "Department of Scientific and Industrial Research",
    "Department of Social Justice and Empowerment",
    "Department of Sports",
    "Department of Telecommunications",
    "Department of Water Resources, River Development and Ganga Rejuvenation",
    "Department of Youth Affairs",
    "Inter-State Council Secretariat",
    "Legislative Department"
]

class Department_classifier:
    
    def __init__(self):
#         self.inference_text = inference_text
#         self.df = pd.read_csv('/kaggle/input/sih-2023/sample1.csv')
        self.index_to_option = {i: departments[i] for i in range(len(departments))}
        self.option_to_index = {departments[i]: i for i in range(len(departments))}
        self.tokenizer = AutoTokenizer.from_pretrained('/home/atish/SIH_2k23/api/crawler/files')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "/home/atish/SIH_2k23/api/crawler/files", num_labels=len(departments),
            id2label=self.index_to_option, label2id=self.option_to_index)
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()
        
    def data_preprocessing(self, df):
        df.dropna()
        df =df.drop(columns=['image__@type', 'image__height', 'image__width', 'image__url', ])
        df['context'] =df['headline'] + '.' +df['description'] + '.' +df[
                    'datePublished'] + '.' + df['articleBody']
        df =df.drop(columns=['inLanguage', 'headline', 'description', 'datePublished', 'articleBody'])
        df.dropna()
        df =df.drop(df[df['context'].isna()].index)
        df =df.drop(df[df['department'] == 'indian_government'].index)
        df =df.reset_index(drop=True)
        columns = [i for i in range(len(departments))]
        matrix = [columns] * len(self.df)
        data = pd.DataFrame(matrix, columns=departments)
        df.loc[df['department'] == "department_for_promotion_of_industry", 'department'] = "Department for Promotion of Industry and Internal Trade"
        df.loc[df['department'] == "department_of_personnel_and_training", 'department'] = "Department of Personnel and Training"
        df.loc[df['department'] == "department_of_food", 'department'] = "Department of Food and Public Distribution"
        df.loc[df['department'] == "department_of_legal_affair", 'department'] = "Department of Legal Affairs "
        df.loc[df['department'] == "department_of_health", 'department'] = "Department of Health and Family Welfare"
        df.loc[df['department'] == "department_of_science_and_technology", 'department'] = "Department of Science and Technology "
        df.loc[df['department'] == "department_of_sports", 'department'] = "Department of Sports"
        contexts = []
        df['department'] =df['department'].map(self.option_to_index)
        return df

    def pre_process(self, example):
        first_sentence = "[CLS]" + example["context"] + "[SEP]"
        tokenized_example = self.tokenizer(first_sentence, max_length=256, truncation=True, padding=True)
        tokenized_example['label'] = example['department']    
        return tokenized_example

    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=labels)

    def train_fn(self, tokenized_test_dataset, tokenized_val_dataset):
        accuracy = evaluate.load("accuracy")
        
        training_args = TrainingArguments(
            warmup_ratio=0.1, 
            learning_rate=2e-5,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=2,
            num_train_epochs=20,
            report_to='none',
            output_dir=f'./checkpoints_{1}',
            overwrite_output_dir=True,
            fp16=True,
            gradient_accumulation_steps=8,
            logging_steps=25,
            evaluation_strategy='steps',
            eval_steps=25,
            save_strategy="steps",
            save_steps=25,
            load_best_model_at_end=False,
            metric_for_best_model='accuracy',
            lr_scheduler_type='cosine',
            weight_decay=0.01,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_test_dataset,
            eval_dataset=tokenized_val_dataset,
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
            compute_metrics=self.compute_metrics,
        )

        trainer.train()

    def inference(self, inference_text):
        text = "[CLS]" + inference_text + "[SEP]"
        tokenized_example = self.tokenizer(text, max_length=256, truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**tokenized_example)
        preds = outputs.logits.cpu().detach().numpy()
        max_pred_index = np.argmax(preds)
        department = self.index_to_option[max_pred_index]
        return department

    def returnSentiment(self, text):
        x = self.sia.polarity_scores(text)
        return x
        
    def main(self, option, inference_text = None):
        if option == 'Train':
            df = pd.read_csv('/kaggle/input/sih-2023/sample1.csv')
            data_frame = self.data_preprocessing(df)
            train_df, val_df = train_test_split(data_frame, test_size=0.2, random_state=42)
            filtered_train_df = train_df[train_df['department'].notna()]
            filtered_val_df = val_df[val_df['department'].notna()]
            tokenized_test_dataset = Dataset.from_pandas(filtered_train_df[['department', 'context']]).map(self.pre_process, remove_columns=['department', 'context'])
            tokenized_val_dataset = Dataset.from_pandas(filtered_val_df[['department', 'context']]).map(self.pre_process, remove_columns=['department', 'context'])

            tokenized_test_dataset = tokenized_test_dataset.remove_columns(["__index_level_0__"])
            tokenized_val_dataset = tokenized_val_dataset.remove_columns(["__index_level_0__"])
            test_dataloader = DataLoader(tokenized_test_dataset, batch_size=1, shuffle=False, collate_fn=self.data_collator)
            val_dataloader = DataLoader(tokenized_val_dataset, batch_size=1, shuffle=False, collate_fn=self.data_collator)

            self.train_fn(tokenized_test_dataset, tokenized_val_dataset)
        elif option == 'Inference':
            if inference_text == None:
                return "Error No Text"
            department = self.inference(inference_text)
            score = self.returnSentiment(inference_text)
            score = score['compound']
            return {"Department":department, "Score":score}
            
# You'll need to define 'departments' and make sure all the required libraries are imported.
classifier = Department_classifier()
# outputs = ob.main('Inference', pred)
# print(outputs)