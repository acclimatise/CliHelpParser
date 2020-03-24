from test.util import process_help_section as p

import pytest
from acclimatise.model import Flag, SimpleFlagArg
from acclimatise.usage_parser import parse_usage
from acclimatise.usage_parser.elements import (  # short_flag_list,
    stack,
    usage,
    usage_element,
)
from acclimatise.usage_parser.model import UsageElement


def test_bwa():
    txt = "Usage: bwa mem [options] <idxbase> <in1.fq> [in2.fq]"
    els = usage.parseString(txt)
    print(els)


@pytest.mark.skip(
    "It's impossible to distinguish between a grouped list of short flags and one long flag with a single dash"
)
def test_samtools_merge_short_flags():
    text = "-nurlf"
    els = short_flag_list.parseString(text)
    assert len(els) == 5
    assert isinstance(els[0], Flag)


@pytest.mark.skip(
    "It's impossible to distinguish between a grouped list of short flags and one long flag with a single dash"
)
def test_samtools_merge_optional_short_flags():
    text = "[-nurlf]"
    els = usage_element.parseString(text)
    assert len(els) == 5
    assert isinstance(els[0], Flag)
    assert els[0].optional


def test_samtools_merge_variable():
    text = "<out.bam>"
    els = usage_element.parseString(text)
    assert len(els) == 1
    assert isinstance(els[0], UsageElement)
    assert els[0].variable


def test_samtools_merge_flag_arg():
    text = "-h inh.sam"
    els = usage_element.parseString(text)
    assert len(els) == 1
    assert isinstance(els[0], Flag)
    assert isinstance(els[0].args, SimpleFlagArg)


def test_samtools_merge_optional_flag_arg():
    text = "[-h inh.sam]"
    els = usage_element.setDebug().parseString(text)
    assert len(els) == 1
    assert isinstance(els[0], Flag)
    assert els[0].optional
    assert isinstance(els[0].args, SimpleFlagArg)


def test_samtools_merge_full():
    text = p(
        """
    Usage: samtools merge [-nurlf] [-h inh.sam] [-b <bamlist.fofn>] <out.bam> <in1.bam> [<in2.bam> ... <inN.bam>]
    """
    )
    command = parse_usage(cmd=["samtools", "merge"], text=text)

    assert len(command.positional) == 3
    assert command.positional[0].name == "out.bam"
    assert command.positional[1].name == "in1.bam"

    assert len(command.named) == 3
    assert command.named[0].longest_synonym == "-nurlf"
    assert command.named[1].longest_synonym == "-h"
    assert command.named[2].longest_synonym == "-b"


def test_pisces_usage():
    text = "USAGE: dotnet Pisces.dll -bam <bam path> -g <genome path>"
    command = parse_usage(["pisces"], text)
    assert len(command.named) == 2
    assert command.named[0].longest_synonym == "-bam"
    assert command.named[1].longest_synonym == "-g"
    assert command.positional[0].name == "dotnet"


def test_trailing_text():
    """
    Tests that the usage parser will not parse text after the usage section has ended
    """
    text = p(
        """
    usage: htseq-count [options] alignment_file gff_file

    This script takes one or more alignment files in SAM/BAM format and a feature
    file in GFF format and calculates for each feature the number of reads mapping
    to it. See http://htseq.readthedocs.io/en/master/count.html for details.
    """
    )
    command = parse_usage(["htseq-count"], text)
    assert len(command.positional) == 3
