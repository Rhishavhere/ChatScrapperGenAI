from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from config import EDGE_DATA_PATH
from dotenv import load_dotenv

import time

import os

import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="Your are a chatbot but dont identify yourself . you will play my role and reply to my messages sent by my friends on behave of me . I am rhishav . chat in a casual style like whatsapp chat style. and keep in mind to reply short messages and dont use emojies , just plain text ",
)

history=[] 

# opening app

options =Options()
options.add_argument(EDGE_DATA_PATH)
options.add_experimental_option("detach",True)

service=Service(executable_path="msedgedriver.exe")
driver=webdriver.Edge(service=service,options=options)

driver.get("https://web.telegram.org/k/")
driver.maximize_window()
time.sleep(5)

def openChat(contact_name):
    search_box = driver.find_element(By.XPATH, '//*[@id="column-left"]/div/div/div[1]/div[2]/input')
    search_box.clear()
    search_box.send_keys(contact_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    chatButton=driver.find_element(By.XPATH, '//*[@id="search-container"]/div[2]/div[2]/div/div[1]/div/div[1]/ul/a[1]/div[1]')
    chatButton.click()
    time.sleep(10)

def getLastMessage():
    message = driver.find_element(By.XPATH, "//div[contains(@class, 'bubbles-group-last')]//div[contains(@class, 'message')]/span")
    text = message.get_attribute("innerText").strip()
    # text = text.rsplit(' ', 2)[0]
    return text
    

def replyBack():

  text=getLastMessage()
  print(text)

  chat_session = model.start_chat(
    history=history
  )

  response = chat_session.send_message(text)

  reply=response.text

  history.append({"role": "user","parts":[text]})
  history.append({"role": "model","parts":[reply]})

  input=driver.find_element(By.XPATH,'//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')
  print(reply)

  input.clear()

  chunk_size = 100
  for i in range(0, len(reply), chunk_size):
    chunk = reply[i:i+chunk_size]
    input.send_keys(chunk)
    time.sleep(0.1)

  input.send_keys(Keys.RETURN)
  time.sleep(2)

name='Maaa'
openChat(name)
while True:
  replyBack()
  time.sleep(10)
