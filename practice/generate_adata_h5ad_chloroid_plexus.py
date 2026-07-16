import scanpy as sc
import scipy.io as sio
import pandas as pd
import anndata as ad

# Load matrix
mat = sio.mmread('practice/sc_rna_chloroid_plexus/matrix.mtx').tocsr()

# Load barcodes and genes (single column each)
barcodes = pd.read_csv('practice/sc_rna_chloroid_plexus/barcodes.tsv', header=None)[0].values
genes = pd.read_csv('practice/sc_rna_chloroid_plexus/genes.tsv', header=None)[0].values

# 10x convention: genes = rows, cells = columns -> transpose so cells are rows (AnnData convention)
adata = ad.AnnData(X=mat.T.tocsr())
adata.obs_names = barcodes
adata.var_names = genes

adata.write('practice/adata.h5ad')

# To view the first few cells and their metadata (e.g., cell types, batch, total counts)
print(adata.obs.head())
print('\n')

# To view the first few features/genes and their metadata (e.g., gene symbols)
print(adata.var.head())
print('\n')
print(adata.X)
print('\n')
print(adata.shape)  # (n_cells, n_genes)

