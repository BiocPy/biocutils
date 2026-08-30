import pytest
import numpy as np
import pandas as pd
import biocframe
from biocframe import BiocFrame
from genomicranges import GenomicRanges
from summarizedexperiment import SummarizedExperiment
from multiassayexperiment import MultiAssayExperiment
import biocutils as ut

def test_melt_biocframe():
    bf = BiocFrame({"A": [1, 2], "B": [3, 4]})
    res = ut.melt(bf)
    assert isinstance(res, pd.DataFrame)
    assert list(res["variable"]) == ["A", "A", "B", "B"]
    assert list(res["value"]) == [1, 2, 3, 4]

def test_melt_genomicranges():
    gr = GenomicRanges.from_pandas(pd.DataFrame({
        "seqnames": ["chr1"],
        "starts": [10],
        "ends": [15],
        "strand": ["+"]
    }))
    res = ut.melt(gr)
    assert isinstance(res, pd.DataFrame)
    # Check that coordinate variables are in the melted DataFrame
    # self.to_pandas() returns a DataFrame with seqnames, starts, ends, strand, names
    assert "variable" in res.columns
    assert "value" in res.columns

def test_melt_summarizedexperiment():
    se = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_names=["gene_A", "gene_B"],
        column_names=["sample_1", "sample_2"]
    )
    res = ut.melt(se, assay=0)
    assert isinstance(res, pd.DataFrame)
    assert len(res) == 4
    assert list(res["value"]) == [1, 2, 3, 4]

def test_melt_multiassayexperiment():
    se1 = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_names=["gene_A", "gene_B"],
        column_names=["sample_1", "sample_2"]
    )
    se2 = SummarizedExperiment(
        assays={"counts": np.array([[5, 6], [7, 8]])},
        row_names=["gene_A", "gene_B"],
        column_names=["sample_1", "sample_2"]
    )
    mae = MultiAssayExperiment(
        experiments={"assay1": se1, "assay2": se2}
    )
    res = ut.melt(mae)
    assert isinstance(res, pd.DataFrame)
    assert len(res) == 8
    assert "assay" in res.columns
    assert list(res["assay"]) == ["assay1"] * 4 + ["assay2"] * 4
