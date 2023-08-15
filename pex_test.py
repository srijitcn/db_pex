# Databricks notebook source
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
dbutils.fs.put("file:///root/.databrickscfg","[DEFAULT]\nhost=https://adb-8590162618558854.14.azuredatabricks.net/\ntoken = "+token,overwrite=True)

# COMMAND ----------

# MAGIC %sh
# MAGIC /dbfs/FileStore/tmp/pex/db_pex.pex

# COMMAND ----------


