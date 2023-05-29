#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# ### Import datasets

# In[2]:


df_true = pd.read_csv("True.csv")
df_fake = pd.read_csv("Fake.csv")


# ### Inserting a column "class" as target feature

# In[3]:


df_true["class"] = 1
df_fake["class"] = 0


# ### Merging both dataframes

# In[4]:


df=pd.concat([df_true ,df_fake ],axis=0 )
df


# In[5]:


df.head()


# In[6]:


df.shape


# ### Checking null values

# In[7]:


df.isnull().sum()


# ### Display types of news 

# In[8]:


sns.countplot(x='subject', hue='class',data=df)
plt.xticks(rotation=90)
plt.show()


# ### Display division of true and fake news

# In[9]:


plt.title('The division of true and fake news')
plt.xlabel('True or False')
plt.ylabel('Count')
df['class'].value_counts().plot(kind='bar',color='orange')
plt.show


# ### Removing unnecessary columns

# In[10]:


df.drop(['subject','date'],axis=1,inplace=True)
df


# ### Merging both columns title and text

# In[11]:


df['text'] = df['title'] + " " + df['text']
df.drop(['title'],axis=1,inplace=True)
df


# ### Creating a function to process the texts

# In[12]:


import re
import string
def process(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text


# In[13]:


df['text'].apply(process)
df


# ## Performing Machine learning

# ### Defining dependent and independent variables

# In[14]:


x=df['text']
y=df['class']


# ### Splitting Training and Testing dataset

# In[15]:


from sklearn.model_selection import train_test_split


# In[16]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)


# ### Converting text to vectors

# In[17]:


from sklearn.feature_extraction.text import CountVectorizer


# In[18]:


cv =CountVectorizer()


# In[19]:


x_train_cv = cv.fit_transform(x_train.values)
x_test_cv = cv.transform(x_test)
x_test_cv.toarray()


# ## Implementing Machine Learning Models

# ### Logistic Regression

# In[20]:


from sklearn.linear_model import LogisticRegression
model_lr = LogisticRegression()
model_lr.fit(x_train_cv,y_train)


# In[21]:


pred_lr=model_lr.predict(x_test_cv)


# In[22]:


print(model_lr.score(x_train_cv,y_train))
print(model_lr.score(x_test_cv, y_test))


# In[23]:


from sklearn.metrics import classification_report,accuracy_score,plot_confusion_matrix
print(classification_report(y_test, pred_lr))


# In[24]:


print(accuracy_score(y_test, pred_lr))


# In[25]:


plot_confusion_matrix(model_lr,x_test_cv,y_test)
plt.show()


# ## Decision Tree Classifier

# In[26]:


from sklearn.tree import DecisionTreeClassifier

model_dt = DecisionTreeClassifier()
model_dt.fit(x_train_cv, y_train)


# In[27]:


pred_dt=model_dt.predict(x_test_cv)


# In[28]:


print(model_dt.score(x_train_cv,y_train))
print(model_dt.score(x_test_cv, y_test))


# In[29]:


print(classification_report(y_test, pred_dt))


# In[30]:


plot_confusion_matrix(model_dt,x_test_cv,y_test)
plt.show()


# ## Random Forest Classifier

# In[31]:


from sklearn.ensemble import RandomForestClassifier

model_rf = RandomForestClassifier(random_state=0)
model_rf.fit(x_train_cv, y_train)


# In[32]:


pred_rf=model_rf.predict(x_test_cv)


# In[33]:


print(model_rf.score(x_train_cv,y_train))
print(model_rf.score(x_test_cv, y_test))


# In[34]:


print(classification_report(y_test, pred_rf))


# In[35]:


plot_confusion_matrix(model_rf,x_test_cv,y_test)
plt.show()


# ## Multinomial Naive Bayes

# In[36]:


from sklearn.naive_bayes import MultinomialNB


# In[37]:


model_nb = MultinomialNB()
model_nb.fit(x_train_cv,y_train)


# In[38]:


pred_nb=model_nb.predict(x_test_cv)


# In[39]:


print(model_nb.score(x_train_cv,y_train))
print(model_nb.score(x_test_cv, y_test))


# In[40]:


print(classification_report(y_test, pred_nb))


# In[41]:


plot_confusion_matrix(model_nb,x_test_cv,y_test)
plt.show()


# ## Model Testing

# In[42]:


def output(n):
    if n == 0:
        return "Fake News"
    else:
        return "Not A Fake News"
    
def testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(process) 
    new_x_test = new_def_test["text"]
    new_cv_test = cv.transform(new_x_test)
    pred_lr = model_lr.predict(new_cv_test)
    pred_dt = model_dt.predict(new_cv_test)
    pred_rf = model_rf.predict(new_cv_test)
    pred_nb = model_nb.predict(new_cv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nRF Prediction: {} \nNB Prediction: {}".format(output(pred_lr[0]),output(pred_dt[0]), output(pred_rf[0]),output(pred_nb[0])))


# In[43]:


news = str(input())
testing(news)


# In[ ]:


Vic Bishop Waking TimesOur reality is carefully constructed by powerful corporate, political and special interest sources in order to covertly sway public opinion. Blatant lies are often televised regarding terrorism, food, war, health, etc. They are fashioned to sway public opinion and condition viewers to accept what have become destructive societal norms.The practice of manipulating and controlling public opinion with distorted media messages has become so common that there is a whole industry formed around this. The entire role of this brainwashing industry is to figure out how to spin information to journalists, similar to the lobbying of government. It is never really clear just how much truth the journalists receive because the news industry has become complacent. The messages that it presents are shaped by corporate powers who often spend millions on advertising with the six conglomerates that own 90% of the media:General Electric (GE), News-Corp, Disney, Viacom, Time Warner, and CBS. Yet, these corporations function under many different brands, such as FOX, ABC, CNN, Comcast, Wall Street Journal, etc, giving people the perception of choice   As Tavistock s researchers showed, it was important that the victims of mass brainwashing not be aware that their environment was being controlled; there should thus be a vast number of sources for information, whose messages could be varied slightly, so as to mask the sense of external control. ~ Specialist of mass brainwashing, L. WolfeNew Brainwashing Tactic Called AstroturfWith alternative media on the rise, the propaganda machine continues to expand. Below is a video of Sharyl Attkisson, investigative reporter with CBS, during which she explains how  astroturf,  or fake grassroots movements, are used to spin information not only to influence journalists but to sway public opinion. Astroturf is a perversion of grassroots. Astroturf is when political, corporate or other special interests disguise themselves and publish blogs, start facebook and twitter accounts, publish ads, letters to the editor, or simply post comments online, to try to fool you into thinking an independent or grassroots movement is speaking. ~ Sharyl Attkisson, Investigative ReporterHow do you separate fact from fiction? Sharyl Attkisson finishes her talk with some insights on how to identify signs of propaganda and astroturfing  These methods are used to give people the impression that there is widespread support for an agenda, when, in reality, one may not exist. Astroturf tactics are also used to discredit or criticize those that disagree with certain agendas, using stereotypical names such as conspiracy theorist or quack. When in fact when someone dares to reveal the truth or questions the  official  story, it should spark a deeper curiosity and encourage further scrutiny of the information.This article (Journalist Reveals Tactics Brainwashing Industry Uses to Manipulate the Public) was originally created and published by Waking Times and is published here under a Creative Commons license with attribution to Vic Bishop and WakingTimes.com. It may be re-posted freely with proper attribution, author bio, and this copyright statement. READ MORE MSM PROPAGANDA NEWS AT: 21st Century Wire MSM Watch Files


# In[ ]:





# In[ ]:




