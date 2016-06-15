import pandas as pd

def clem_lda(a):
	df = pd.read_csv(a)
	return str(df.head())