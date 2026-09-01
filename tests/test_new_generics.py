import pytest
import numpy as np
import pandas as pd
import biocframe
from biocframe import BiocFrame
from genomicranges import GenomicRanges, CompressedGenomicRangesList
from biostrings import DNAString, DNAStringSet
import biocutils as ut

def test_unlist_relist_lists():
    lst = [[1, 2], [3, 4, 5]]
    flat = ut.unlist(lst)
    assert flat == [1, 2, 3, 4, 5]

    rel = ut.relist(flat, lst)
    assert rel == [[1, 2], [3, 4, 5]]

def test_unlist_relist_genomicranges():
    gr1 = GenomicRanges.from_pandas(pd.DataFrame({
        "seqnames": ["chr1", "chr1"],
        "starts": [10, 20],
        "ends": [15, 25],
        "strand": ["+", "-"]
    }))
    gr2 = GenomicRanges.from_pandas(pd.DataFrame({
        "seqnames": ["chr2"],
        "starts": [100],
        "ends": [105],
        "strand": ["+"]
    }))

    grl = CompressedGenomicRangesList.from_list([gr1, gr2], names=["a", "b"])

    flat = ut.unlist(grl)
    assert isinstance(flat, GenomicRanges)
    assert len(flat) == 3
    assert list(flat.get_start()) == [10, 20, 100]

    rel = ut.relist(flat, grl)
    assert isinstance(rel, CompressedGenomicRangesList)
    assert len(rel) == 2
    assert len(rel[0]) == 2
    assert len(rel[1]) == 1

def test_unlist_relist_biostrings():
    ds = DNAStringSet(["ACGT", "AAAA"])

    flat = ut.unlist(ds)
    assert isinstance(flat, DNAString)
    assert str(flat) == "ACGTAAAA"

    rel = ut.relist(flat, ds)
    assert isinstance(rel, DNAStringSet)
    assert len(rel) == 2
    assert rel.to_list() == ["ACGT", "AAAA"]

def test_pmin_pmax():
    v1 = [1, 5, 3]
    v2 = [2, 4, 6]

    min_res = ut.pmin(v1, v2)
    assert list(min_res) == [1, 4, 3]

    max_res = ut.pmax(v1, v2)
    assert list(max_res) == [2, 5, 6]

def test_mcols_metadata():
    gr = GenomicRanges.from_pandas(pd.DataFrame({
        "seqnames": ["chr1"],
        "starts": [10],
        "ends": [15],
        "strand": ["+"]
    }))

    mc = ut.mcols(gr)
    assert isinstance(mc, BiocFrame)
    assert len(mc.colnames) == 0

    new_mc = BiocFrame({"score": [100]})
    gr = ut.set_mcols(gr, new_mc)
    assert list(ut.mcols(gr).column("score")) == [100]

    meta = ut.metadata(gr)
    assert meta is None or len(meta) == 0

    gr = ut.set_metadata(gr, {"author": "AI"})
    assert ut.metadata(gr)["author"] == "AI"
