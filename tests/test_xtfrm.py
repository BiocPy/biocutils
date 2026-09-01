import numpy as np
import pytest
from biocutils import xtfrm, order, sort, match, duplicated, unique, Factor
from iranges import IRanges
from genomicranges import GenomicRanges
from biostrings import DNAString, DNAStringSet
from summarizedexperiment import RangedSummarizedExperiment
import biocframe

def test_xtfrm_basic():
    x = [20, 10, 20, 30]
    tx = xtfrm(x)
    assert isinstance(tx, np.ndarray)
    assert list(tx) == [1, 0, 1, 2] # sorted is 10, 20, 20, 30 -> ranks [1, 0, 1, 2]

    arr = np.array([1.5, -0.5, 1.5])
    t_arr = xtfrm(arr)
    assert np.array_equal(t_arr, arr)

    strings = ["banana", "apple", "banana", "cherry"]
    tx_str = xtfrm(strings)
    assert list(tx_str) == [1, 0, 1, 2]

def test_xtfrm_Factor():
    f = Factor.from_sequence(["B", "A", "B", "C"])
    tf = xtfrm(f)
    assert np.array_equal(tf, f.get_codes())

    assert list(order(f)) == [1, 0, 2, 3]

def test_xtfrm_IRanges():
    ir = IRanges([10, 5, 10], [5, 8, 3])
    tx_ir = xtfrm(ir)
    assert tx_ir == [(10, 5), (5, 8), (10, 3)]

    o = order(ir)
    assert list(o) == [1, 2, 0]

    sir = sort(ir)
    assert list(sir.get_start()) == [5, 10, 10]
    assert list(sir.get_width()) == [8, 3, 5]

    targets = IRanges([5, 10], [8, 3])
    m = match(ir, targets)
    assert list(m) == [-1, 0, 1] # only range 1 and range 2 are matched

    ir2 = IRanges([10, 5, 10, 5], [5, 8, 5, 8])
    assert list(duplicated(ir2)) == [False, False, True, True]

def test_xtfrm_GenomicRanges():
    gr = GenomicRanges(
        seqnames=["chr1", "chr2", "chr1"],
        ranges=IRanges([10, 5, 10], [5, 8, 3]),
        strand=["+", "-", "+"]
    )
    tx_gr = xtfrm(gr)
    assert len(tx_gr) == 3

    o = order(gr)
    assert list(o) == [2, 0, 1]

    # verify sort
    sgr = sort(gr)
    assert list(sgr.get_start()) == [10, 10, 5]
    assert list(sgr.get_seqnames()) == ["chr1", "chr1", "chr2"]

def test_xtfrm_DNAStringSet():
    dset = DNAStringSet(["ACGT", "TGCA", "ACGT"])

    tx_dset = xtfrm(dset)
    assert tx_dset == ["ACGT", "TGCA", "ACGT"]

    assert list(order(dset)) == [0, 2, 1]
    assert list(duplicated(dset)) == [False, False, True]

def test_xtfrm_RangedSummarizedExperiment():
    gr = GenomicRanges(
        seqnames=["chr1", "chr2", "chr1"],
        ranges=IRanges([10, 5, 10], [5, 8, 3]),
        strand=["+", "-", "+"]
    )
    rse = RangedSummarizedExperiment(
        assays={"counts": np.random.rand(3, 2)},
        row_ranges=gr
    )

    assert len(xtfrm(rse)) == 3
    assert list(order(rse)) == [2, 0, 1]
