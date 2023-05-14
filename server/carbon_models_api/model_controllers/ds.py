import os

import tensorflow as tf
import torch
import numpy as np
import json
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

from PIL import Image
from keras.applications import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
# from keras.preprocessing import image
# from tensorflow.keras.utils.preprocessing import image
from keras.utils import image_utils
from transformers import T5ForConditionalGeneration, T5Tokenizer, ViltProcessor, ViltForQuestionAnswering
# from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


def load_json(path):
    with open(path, "r") as f:
        loaded_dict = json.load(f)

    return loaded_dict


def generate_embeddings(name, texts):
    my_dict = {
        "name": [],
    }

    model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')

    my_dict["name"] = texts
    df = pd.DataFrame(my_dict, columns=["name"])
    df.to_csv(f"../embeddings/name{name}.csv", index=False)
    embedding = model.encode(texts)
    np.savetxt(f"../embeddings/embed{name}.txt", embedding)


class FootPrint:
    def __init__(self, path_embd_food, path_embd_contries):
        # print(os.getcwd())
        self.name_food = pd.read_csv(os.getcwd() + "/carbon_models_api/model_controllers/embeddings/namefoods.csv")
        self.name_country = pd.read_csv(os.getcwd() + "/carbon_models_api/model_controllers/embeddings/namecountry.csv")
        self.embed_food = np.loadtxt(os.getcwd() + "/carbon_models_api/model_controllers/embeddings/embedfoods.txt")
        self.embed_country = np.loadtxt(
            os.getcwd() + "/carbon_models_api/model_controllers/embeddings/embedcountry.txt")
        self.model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
        self.distances = pd.read_csv(os.getcwd() + "/carbon_models_api/model_controllers/data/capital_distances.csv")
        self.food = pd.read_csv(os.getcwd() + "/carbon_models_api/model_controllers/data/food.csv")

    def cosine_similarity(self, u, v):
        u = np.reshape(u, (1, -1))
        v = np.reshape(v, (1, -1))
        similarity = cosine_similarity(u, v)[0][0]
        return similarity

    def embed_single(self, sentence):
        embedding = self.model.encode(sentence)
        return embedding

    def most_similar_country(self, text):
        maxi = 0
        word_ = ""
        embed = self.embed_single(text)

        for i, word in enumerate(self.name_country["name"]):
            if self.cosine_similarity(embed, self.embed_country[i]) > maxi:
                maxi = self.cosine_similarity(embed, self.embed_country[i])
                word_ = word
        return word_

    def most_similar_food(self, text):
        maxi = 0
        word_ = ""
        embed = self.embed_single(text)

        for i, word in enumerate(self.name_food["name"].to_list()):
            if self.cosine_similarity(embed, self.embed_food[i]) > maxi:
                maxi = self.cosine_similarity(embed, self.embed_food[i])
                word_ = word
        return word_


class FootPrintImage(FootPrint):

    def __init__(self, path_embd_food, path_embd_contries):

        super().__init__(path_embd_food, path_embd_contries)
        self.model_food = MobileNetV2(weights='imagenet', include_top=True)
        self.model_loc = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.processor_loc = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

        df = pd.read_csv(os.getcwd() + "/carbon_models_api/model_controllers/data/foodCO2.csv")
        self.ingredients = df["Food"].to_list()
        self.ingredient_prod = {}
        self.ingredient_trans = {}
        self.ingredient_kill = {}
        for i in range(len(df)):
            self.ingredient_prod[df["Food"][i]] = df["Production"][i]
            self.ingredient_kill[df["Food"][i]] = df["Killed"][i]
            self.ingredient_trans[df["Food"][i]] = df["Transport"][i]

    def image_location(self, image_path):
        image = Image.open(image_path)
        text = "At which country is this picture taken?"

        encoding = self.processor_loc(image, text, return_tensors="pt")
        outputs = self.model_loc(**encoding)
        logits = outputs.logits

        idx = logits.argmax(-1).item()

        return self.model_loc.config.id2label[idx]

    def image_food(self, image_path):
        img = image_utils.load_img(image_path, target_size=(224, 224))
        x = image_utils.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = self.model_food.predict(x)
        top_preds = tf.keras.applications.imagenet_utils.decode_predictions(preds, top=5)[0]

        return top_preds[0]

    def most_similar_ingridient(self, text):
        maxi = 0
        word_ = ""
        embed = self.embed_single(text)
        for word in self.ingredients:
            ingredient = self.embed_single(word)
            if self.cosine_similarity(embed, ingredient) > maxi:
                maxi = self.cosine_similarity(embed, ingredient)
                word_ = word

        return self.ingredient_prod[word_], self.ingredient_trans[word_], self.ingredient_kill[word_]

    def food_footprint(self, image_path):
        food_ = self.most_similar_food(self.image_food(image_path=image_path)[1])
        ingreds = self.food[self.food["Title"] == food_]["Ingredients"]
        sum_co2 = 0
        list_kills = []

        for ingred in ingreds:
            prod, trans, kill = self.most_similar_ingridient(ingred)
            sum_co2 += prod
            sum_co2 += 1.5 * trans
            list_kills.append(kill)

        return sum_co2, list_kills

    def location_footprint(self, image_path, country):
        closest = self.most_similar_country(self.image_location(image_path))
        somth = self.distances[self.distances["Country"] == (str(closest + "," + country))]["Distance (km)"]
        return (somth.values[0] * 115), ["plane"]

    def image_process(self, image_path, country):
        score = self.image_food(image_path=image_path)
        if score[2] > 0.15:
            return self.food_footprint(image_path=image_path)
        else:
            return self.location_footprint(image_path=image_path, country=country)


class FootPrintText(FootPrint):

    def __init__(self, path_embd_food, path_embd_contries):
        super().__init__(path_embd_food, path_embd_contries)
        model_name = 'google/flan-t5-large'
        self.tokenizer_text = T5Tokenizer.from_pretrained(model_name)
        self.model_text = T5ForConditionalGeneration.from_pretrained(model_name)

    def text_location(self, input_text):
        torch.manual_seed(0)
        input_ids = self.tokenizer_text.encode(input_text + "At which country is this picture taken?",
                                               return_tensors='pt')
        outputs = self.model_text.generate(input_ids=input_ids, max_length=5, do_sample=True)
        output_text = self.tokenizer_text.decode(outputs[0], skip_special_tokens=True)

        return output_text

    def text_footprint(self, input_text, country):
        text = self.text_location(input_text=input_text)
        closest = self.most_similar_country(text)
        somth = self.distances[self.distances["Country"] == (str(closest + "," + country))]["Distance (km)"]
        return (somth.values[0] * 115), ["plane"]


if __name__ == "__main__":
    obj = FootPrintImage("", "")
    print(obj.image_process("../examples/hotdog.jpg", "Macedonia"))
    # print(obj.text_footprint("I went to Camp Nou at Barcelona, I am blessed to be there!!!", "Macedonia"))
