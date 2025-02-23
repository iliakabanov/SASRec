# -*- coding: utf-8 -*-
"""tests_for_datasets.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eMySSXgTLj37GxMYBII5HdU5Hshe3p3C
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.sql.functions import col
from pyspark.sql.functions import to_timestamp

def test_actions_structure(df):
    # Проверка названий колонок
    expected_columns = {"user_id", "item_id", "datetime", "weight"}
    assert set(df.columns) == expected_columns, f"Ошибка: Ожидались колонки {expected_columns}, но получены {set(df.columns)}"

    # Проверка типов данных
    assert pd.api.types.is_integer_dtype(df["user_id"]), "Ошибка: 'user_id' должен быть целым числом"
    assert pd.api.types.is_integer_dtype(df["item_id"]), "Ошибка: 'item_id' должен быть целым числом"
    assert pd.api.types.is_datetime64_any_dtype(df["datetime"]), "Ошибка: 'datetime' должен быть datetime"
    assert pd.api.types.is_numeric_dtype(df["weight"]), "Ошибка: 'weight' должен быть числом"

    print("✅ Тест структуры данных пройден")

def test_missing_values(df):
    missing_values = df.isnull().sum()
    assert missing_values.sum() == 0, f"Ошибка: Найдены пропущенные значения\n{missing_values}"

    print("✅ Тест на пропущенные значения пройден")


def test_number_users(df_final, df_original):
  n_users_original = df_original.filter(df_original['action']=='conversion').select('customer_user_id').dropna().distinct().count()
  n_users_final = len(df_final.user_id.unique())

  assert n_users_final <= n_users_original, 'Ошибка: слишком большое число юзеров'
  assert n_users_final > 0.95*n_users_original, 'Ошибка: пропало больше 5% нужных юзеров'

  print("✅ Тест на множество юзеров пройден")


def test_users_actions(df_final, df_original, n_users=3):
  users = df_final['user_id'].sample(n=n_users)
  for user in users:
    test_user_actions(user, df_final, df_original)

  print("✅ Тест на добавления в корзину пройден ")


def test_user_actions(user_id, df_final, df_original):
  assert  get_user_items_from_final(user_id, df_final) == get_user_items_from_original(user_id, df_original), f"Ошибка: неправильно указаны добавления в корзину для юзера {user_id}"


def get_user_items_from_final(user_id, df):
    df = df[df["user_id"] == user_id][["item_id", "datetime"]]
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
    return set(zip(df['item_id'], df['datetime']))

def get_user_items_from_original(user_id, df):
    df = df.filter(df['action']=='conversion').filter(df['customer_user_id']==str(user_id)).select("customer_id", "timestamp").toPandas().dropna()
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S').apply(lambda x: x.replace(microsecond=0))
    df['customer_id'] = df['customer_id'].apply(lambda x: int(x))
    result = set(zip(df['customer_id'], df['timestamp']))

    return result

def test_actions_petco(df_final, df_original):
  test_actions_structure(df_final)
  test_missing_values(df_final)
  test_users_actions(df_final, df_original)

def test_items_structure(df):
    # Проверка названий колонок
    expected_columns = {"id", "value", "feature"}
    assert set(df.columns) == expected_columns, f"Ошибка: Ожидались колонки {expected_columns}, но получены {set(df.columns)}"

    # Проверка типов данных
    assert pd.api.types.is_integer_dtype(df["id"]), "Ошибка: 'id' должен быть целым числом"
    assert pd.api.types.is_string_dtype(df["value"]), "Ошибка: 'value' должен быть строкой"
    assert pd.api.types.is_string_dtype(df["feature"]), "Ошибка: 'feature' должен быть строкой"

    print("✅ Тест структуры данных пройден")

def test_missing_values(df):
    missing_values = df.isnull().sum()
    assert missing_values.sum() == 0, f"Ошибка: Найдены пропущенные значения\n{missing_values}"

    print("✅ Тест на пропущенные значения пройден")


def test_number_items(df_final, df_original):
  n_items_original = df_original.select('customer_id').dropna().distinct().count()
  n_items_final = len(df_final['id'].unique())

  assert n_items_final == n_items_original, 'Ошибка: число юзеров не совпадает с каталогом'

  print("✅ Тест на множество товаров пройден")


def test_items_features(df_final, df_original, n_users=3):

  print("✅ Тест на признаки товаров пройден ")

def test_items_petco(df_final, df_original):
  test_items_structure(df_final)
  test_missing_values(df_final)
  test_number_items(df_final, df_original)