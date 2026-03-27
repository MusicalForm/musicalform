#!/usr/bin/env python3

#######################################################################
#
# SYMBOLS SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


import os
import re
import sys
from functools import partial
from typing import Any, Callable, List, Tuple

RxPatternType = re.Pattern

try:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    scriptdir = ""
if scriptdir and scriptdir not in sys.path:
    sys.path.append(scriptdir)

try:
    pass
except (ImportError, ModuleNotFoundError):
    i = scriptdir.rfind("/DHParser/")
    if i >= 0:
        dhparserdir = scriptdir[: i + 10]  # 10 = len("/DHParser/")
        if dhparserdir not in sys.path:
            sys.path.insert(0, dhparserdir)

import DHParser.versionnumber
from DHParser import dsl
from DHParser.compile import Compiler, Junction
from DHParser.configuration import (
    NEVER_MATCH_PATTERN,
    access_presets,
    finalize_presets,
    get_config_value,
    set_config_value,
    set_preset_value,
)
from DHParser.dsl import never_cancel, recompile_grammar
from DHParser.error import (
    ERROR,
    FATAL,
    Error,
    canonical_error_strings,
    has_errors,
)
from DHParser.log import start_logging
from DHParser.nodetree import (
    Node,
    RootNode,
)
from DHParser.parse import (
    Alternative,
    Grammar,
    OneOrMore,
    Option,
    RegExp,
    Series,
    Synonym,
    Text,
    Whitespace,
    ZeroOrMore,
    mixin_comment,
)
from DHParser.pipeline import (
    PseudoJunction,
    create_junction,
    create_parser_junction,
    create_preprocess_junction,
    end_points,
    full_pipeline,
)
from DHParser.toolkit import (
    RX_NEVER_MATCH,
    ThreadLocalSingletonFactory,
    expand_table,
    static,
)
from DHParser.transform import (
    TransformerFunc,
    transformer,
)

if DHParser.versionnumber.__version_info__ < (1, 8, 3):
    print(
        f"DHParser version {DHParser.versionnumber.__version__} is lower than the DHParser "
        f"version 1.8.3, {os.path.basename(__file__)} has first been generated with. "
        f"Please install a more recent version of DHParser to avoid unexpected errors!"
    )


#######################################################################
#
# PREPROCESSOR SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


# To capture includes, replace the NEVER_MATCH_PATTERN
# by a pattern with group "name" here, e.g. r'\input{(?P<name>.*)}'
RE_INCLUDE = NEVER_MATCH_PATTERN
RE_COMMENT = NEVER_MATCH_PATTERN  # THIS MUST ALWAYS BE THE SAME AS lcma_standardGrammar.COMMENT__ !!!


def lcma_standardTokenizer(original_text) -> Tuple[str, List[Error]]:
    # Here, a function body can be filled in that adds preprocessor tokens
    # to the source code and returns the modified source.
    return original_text, []


preprocessing: PseudoJunction = create_preprocess_junction(lcma_standardTokenizer, RE_INCLUDE, RE_COMMENT)


#######################################################################
#
# PARSER SECTION - Don't edit! CHANGES WILL BE OVERWRITTEN!
#
#######################################################################


class lcma_standardGrammar(Grammar):
    r"""Parser for a lcma_standard document.

    Instantiate this class and then call the instance with the source
    code as the single argument in order to use the parser, e.g.:
        parser = lcma_standard()
        syntax_tree = parser(source_code)
    """

    source_hash__ = "a736d0b583c7355dd85d77ee166577bc"
    disposable__ = re.compile("$.")
    static_analysis_pending__ = []  # type: List[bool]
    parser_initialization__ = ["upon instantiation"]
    COMMENT__ = r""
    comment_rx__ = RX_NEVER_MATCH
    WHITESPACE__ = r"\s*"
    WSP_RE__ = mixin_comment(whitespace=WHITESPACE__, comment=COMMENT__)
    wsp__ = Whitespace(WSP_RE__)
    Name = OneOrMore(RegExp("[a-zA-Z0-9']"))
    MaterialOperators = OneOrMore(RegExp("[!*~^\xb0+]"))
    Shorthand = Synonym(MaterialOperators)
    Entry = Series(Alternative(Series(Text('"'), Name, Text('"')), Name), Option(MaterialOperators))
    Concatenation = Series(Entry, OneOrMore(Series(Text(","), Entry)))
    MaterialRef = Alternative(
        Series(Text("["), Concatenation, Text("]")), Series(Text("("), Concatenation, Text(")")), Concatenation, Entry
    )
    SourceOnly = Series(MaterialRef, Text(","))
    TargetOnly = Series(Text(","), MaterialRef)
    MaterialPositions = Alternative(TargetOnly, Series(MaterialRef, Text(","), MaterialRef), SourceOnly, MaterialRef)
    Unit = Alternative(
        Text("unit"),
        Text("x"),
        Text("part"),
        Text("section"),
        Text("phrase"),
        Text("sub-phrase"),
        Text("idea"),
        Text("work"),
        Text("movement"),
        Text("zone"),
        Text("theme"),
        Text("album"),
        Text("song"),
        Text("cycle"),
        Text("group"),
    )
    FormalType = Alternative(
        Text("hybrid1"),
        Text("hyb1"),
        Text("hybrid2"),
        Text("hyb2"),
        Text("hybrid3"),
        Text("hyb3"),
        Text("hybrid4"),
        Text("hyb4"),
        Text("period"),
        Text("pd"),
        Series(Text("repeated"), Option(Text("_")), wsp__, Unit),
        Text("ritornello form"),
        Text("ritornello"),
        Text("rondo form"),
        Text("rondo"),
        Text("sentence"),
        Text("sent"),
        Text("sequence"),
        Text("seq"),
        Text("sonata form"),
        Text("sonata"),
        Text("unary form"),
        Text("unary"),
        Text("simple_binary.balanced"),
        Text("simple_binary"),
        Text("rounded_binary"),
        Text("ternary.through_composed"),
        Text("ternary.da_capo"),
        Text("ternary"),
    )
    SpecificFunction = Alternative(
        Text("antecedent"),
        Text("ant"),
        Text("after-the-end"),
        Text("ate"),
        Text("basic idea"),
        Text("bi"),
        Text("cadential idea"),
        Text("cad"),
        Text("compound basic idea"),
        Text("cbi"),
        Text("codetta"),
        Text("cdta"),
        Text("contrasting idea"),
        Text("ci"),
        Text("closing theme"),
        Text("cls"),
        Text("coda"),
        Text("consequent"),
        Text("cons"),
        Text("continuation idea"),
        Text("continuation"),
        Text("conti"),
        Text("cont"),
        Text("development section"),
        Text("dev"),
        Text("essential expositional closure"),
        Text("eec"),
        Text("essential sonata closure"),
        Text("esc"),
        Text("exposition"),
        Text("exp"),
        Text("fragmentation"),
        Text("frag"),
        Text("introduction"),
        Text("intro"),
        Text("lead-in"),
        Text("lin"),
        Text("model"),
        Text("mod"),
        Text("movement"),
        Text("mvt"),
        Text("postcadential"),
        Text("pcad"),
        Text("presentation"),
        Text("pres"),
        Text("primary theme zone"),
        Text("primary theme"),
        Text("ptz"),
        Text("pt"),
        Text("recapitulation"),
        Text("recap"),
        Text("ritornello"),
        Text("rit"),
        Text("retransition"),
        Text("rtr"),
        Text("secondary theme zone"),
        Text("secondary theme"),
        Text("stz"),
        Text("st"),
        Text("sequence"),
        Text("seq"),
        Text("transition"),
        Text("tr"),
    )
    TypeExp = Alternative(Series(Text('"'), FormalType, Text('"')), FormalType)
    Cardinality = Alternative(
        Text("1st"),
        Text("2nd"),
        Text("3rd"),
        Text("4th"),
        Text("5th"),
        Text("6th"),
        Text("7th"),
        Text("8th"),
        Text("9th"),
    )
    GenericFunction = Series(Option(Series(Cardinality, Option(Text("_")))), wsp__, Unit)
    FunctionName = Alternative(GenericFunction, SpecificFunction)
    Function = Alternative(Series(Text('"'), FunctionName, Text('"')), FunctionName)
    FunctionExpr = Series(Function, Option(Shorthand))
    Combinator = Text(">")
    Connector = Text("/")
    FunctionLabel = Alternative(
        Series(FunctionExpr, Connector),
        Series(FunctionExpr, Option(Series(wsp__, Combinator, wsp__, Option(FunctionExpr)))),
    )
    Certainty = Text("?")
    Form = Series(FunctionLabel, Option(Series(Text("|"), TypeExp)), Option(Certainty))
    MaterialBrackets = Series(Text("["), MaterialPositions, Text("]"))
    Placeholder = Text("%")
    PlaceholderLabel = Series(Placeholder, Option(Shorthand), wsp__, Option(MaterialBrackets))
    FormLabel = Series(Form, wsp__, Option(MaterialBrackets))
    Label = Series(
        Option(Series(Name, Text(":"))),
        wsp__,
        Alternative(FormLabel, PlaceholderLabel),
        ZeroOrMore(Series(wsp__, Text("-"), wsp__, FormLabel)),
    )
    root__ = Label


parsing: PseudoJunction = create_parser_junction(lcma_standardGrammar)
get_grammar = parsing.factory  # for backwards compatibility, only

try:
    assert RE_INCLUDE == NEVER_MATCH_PATTERN or RE_COMMENT in (lcma_standardGrammar.COMMENT__, NEVER_MATCH_PATTERN), (
        "Please adjust the pre-processor-variable RE_COMMENT in file lcma_standardParser.py so that "
        "it either is the NEVER_MATCH_PATTERN or has the same value as the COMMENT__-attribute "
        "of the grammar class lcma_standardGrammar! "
        'Currently, RE_COMMENT reads "%s" while COMMENT__ is "%s". ' % (RE_COMMENT, lcma_standardGrammar.COMMENT__)
        + "\n\nIf RE_COMMENT == NEVER_MATCH_PATTERN then includes will deliberately be "
        "processed, otherwise RE_COMMENT==lcma_standardGrammar.COMMENT__ allows the "
        "preprocessor to ignore comments."
    )
except (AttributeError, NameError):
    pass


#######################################################################
#
# AST SECTION - Can be edited. Changes will be preserved.
#
#######################################################################

lcma_standard_AST_transformation_table = {
    # AST Transformations for the lcma_standard-grammar
    # "<": [],  # called for each node before calling its specific rules
    # "*": [],  # fallback for nodes that do not appear in this table
    # ">": [],   # called for each node after calling its specific rules
    "Label": [],
    "FormLabel": [],
    "Name": [],
    "Form": [],
    "FunctionLabel": [],
    "Connector": [],
    "Combinator": [],
    "FunctionExp": [],
    "Function": [],
    "FunctionName": [],
    "GenericFunction": [],
    "Count": [],
    "Unit": [],
    "SpecificFunction": [],
    "TypeExp": [],
    "FormalType": [],
    "MaterialBrackets": [],
    "MaterialPositions": [],
    "MaterialRef": [],
    "Concatenation": [],
    "Shorthand": [],
    "MaterialOperators": [],
    "Entry": [],
}


# DEPRECATED, because it requires pickling the transformation-table, which rules out lambdas!
# ASTTransformation: Junction = create_junction(
#     lcma_standard_AST_transformation_table, "CST", "AST", "transtable")


def lcma_standardTransformer() -> TransformerFunc:
    return static(
        partial(
            transformer,
            transformation_table=lcma_standard_AST_transformation_table.copy(),
            src_stage="CST",
            dst_stage="AST",
        )
    )


ASTTransformation: Junction = Junction("CST", ThreadLocalSingletonFactory(lcma_standardTransformer), "AST")


#######################################################################
#
# COMPILER SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


class lcma_standardCompiler(Compiler):
    """Compiler for the abstract-syntax-tree of a
    lcma_standard source file.
    """

    def __init__(self):
        super(lcma_standardCompiler, self).__init__()
        self.forbid_returning_None = True  # set to False if any compilation-method is allowed to return None

    def reset(self):
        super().reset()
        # initialize your variables here, not in the constructor!

    def prepare(self, root: RootNode) -> None:
        assert root.stage == "AST", f"Source stage `AST` expected, `but `{root.stage}` found."
        root.stage = "lcma_standard"

    def finalize(self, result: Any) -> Any:
        return result

    def on_Label(self, node):
        return self.fallback_compiler(node)

    # def on_FormLabel(self, node):
    #     return node

    # def on_Name(self, node):
    #     return node

    # def on_Form(self, node):
    #     return node

    # def on_FunctionLabel(self, node):
    #     return node

    # def on_Connector(self, node):
    #     return node

    # def on_Combinator(self, node):
    #     return node

    # def on_FunctionExp(self, node):
    #     return node

    # def on_Function(self, node):
    #     return node

    # def on_FunctionName(self, node):
    #     return node

    # def on_GenericFunction(self, node):
    #     return node

    # def on_Count(self, node):
    #     return node

    # def on_Unit(self, node):
    #     return node

    # def on_SpecificFunction(self, node):
    #     return node

    # def on_TypeExp(self, node):
    #     return node

    # def on_FormalType(self, node):
    #     return node

    # def on_MaterialBrackets(self, node):
    #     return node

    # def on_MaterialPositions(self, node):
    #     return node

    # def on_MaterialRef(self, node):
    #     return node

    # def on_Concatenation(self, node):
    #     return node

    # def on_Shorthand(self, node):
    #     return node

    # def on_MaterialOperators(self, node):
    #     return node

    # def on_Entry(self, node):
    #     return node


compiling: Junction = create_junction(lcma_standardCompiler, "AST", "lcma_standard")


#######################################################################
#
# END OF DHPARSER-SECTIONS
#
#######################################################################

#######################################################################
#
# Post-Processing-Stages [add one or more postprocessing stages, here]
#
#######################################################################

# class PostProcessing(Compiler):
#     ...

# # change the names of the source and destination stages. Source
# # ("lcma_standard") in this example must be the name of some earlier stage, though.
# postprocessing: Junction = create_junction(PostProcessing, "lcma_standard", "refined")
#
# DON'T FORGET TO ADD ALL POSTPROCESSING-JUNCTIONS TO THE GLOBAL
# "junctions"-set IN SECTION "Processing-Pipeline" BELOW!

#######################################################################
#
# Processing-Pipeline
#
#######################################################################

# Add your own stages to the junctions and target-lists, below
# (See DHParser.compile for a description of junctions)

# ADD YOUR OWN POST-PROCESSING-JUNCTIONS HERE:
junctions = set([ASTTransformation, compiling])

# put your targets of interest, here. A target is the name of result (or stage)
# of any transformation, compilation or postprocessing step after parsing.
# Serializations of the stages listed here will be written to disk when
# calling process_file() or batch_process() and also appear in test-reports.
targets = end_points(junctions)
# alternative: targets = set([compiling.dst])

# provide a set of those stages for which you would like to see the output
# in the test-report files, here. (AST is always included)
test_targets = set(j.dst for j in junctions)
# alternative: test_targets = targets

# add one or more serializations for those targets that are node-trees
serializations = expand_table(dict([("*", [get_config_value("default_serialization")])]))


#######################################################################
#
# Main program
#
#######################################################################


def compile_src(source: str, target: str = "lcma_standard") -> Tuple[Any, List[Error]]:
    """Compiles the source to a single target and returns the result of the compilation
    as well as a (possibly empty) list or errors or warnings that have occurred in the
    process.
    """
    full_compilation_result = full_pipeline(source, preprocessing.factory, parsing.factory, junctions, set([target]))
    return full_compilation_result[target]


def compile_snippet(source_code: str, target: str = "lcma_standard") -> Tuple[Any, List[Error]]:
    """Compiles a piece of source_code. In contrast to :py:func:`compile_src` the
    parameter source_code is always understood as a piece of source-code and never
    as a filename, not even if it is a one-liner that could also be a file-name.
    """
    if source_code[0:1] not in ("\ufeff", "\ufffe") and source_code[0:3] not in (
        "\xef\xbb\xbf",
        "\x00\x00\ufeff",
        "\x00\x00\ufffe",
    ):
        source_code = "\ufeff" + source_code  # add a byteorder-mark for disambiguation
    return compile_src(source_code)


def process_file(source: str, out_dir: str = "") -> str:
    """Compiles the source and writes the serialized results back to disk,
    unless any fatal errors have occurred. Error and Warning messages are
    written to a file with the same name as `result_filename` with an
    appended "_ERRORS.txt" or "_WARNINGS.txt" in place of the name's
    extension. Returns the name of the error-messages file or an empty
    string, if no errors or warnings occurred.
    """
    global serializations
    # serializations = get_config_value('lcma_standard_serializations', serializations)
    return dsl.process_file(
        source,
        out_dir,
        preprocessing.factory,
        parsing.factory,
        junctions,
        targets,
        serializations,
    )


def _process_file(args: Tuple[str, str]) -> str:
    return process_file(*args)


def batch_process(
    file_names: List[str],
    out_dir: str,
    *,
    submit_func: Callable = None,
    log_func: Callable = None,
    cancel_func: Callable = never_cancel,
) -> List[str]:
    """Compiles all files listed in file_names and writes the results and/or
    error messages to the directory `our_dir`. Returns a list of error
    messages files.
    """
    return dsl.batch_process(
        file_names,
        out_dir,
        _process_file,
        submit_func=submit_func,
        log_func=log_func,
        cancel_func=cancel_func,
    )


def main(called_from_app=False) -> bool:
    # recompile grammar if needed
    scriptpath = os.path.abspath(os.path.realpath(__file__))
    if scriptpath.endswith("Parser.py"):
        grammar_path = scriptpath.replace("Parser.py", ".ebnf")
    else:
        grammar_path = os.path.splitext(scriptpath)[0] + ".ebnf"
    parser_update = False

    def notify():
        nonlocal parser_update
        parser_update = True
        print("recompiling " + grammar_path)

    if os.path.exists(grammar_path) and os.path.isfile(grammar_path):
        if not recompile_grammar(grammar_path, scriptpath, force=False, notify=notify):
            error_file = os.path.basename(__file__).replace("Parser.py", "_ebnf_MESSAGES.txt")
            with open(error_file, "r", encoding="utf-8") as f:
                print(f.read())
            sys.exit(1)
        elif parser_update:
            if "--dontrerun" in sys.argv:
                print(
                    os.path.basename(__file__) + " has changed. " "Please run again in order to apply updated compiler"
                )
                sys.exit(0)
            else:
                import subprocess

                call = ["python", __file__, "--dontrerun"] + sys.argv[1:]
                result = subprocess.run(call, capture_output=True)
                print(result.stdout.decode("utf-8"))
                sys.exit(result.returncode)
    else:
        print(
            "Could not check whether grammar requires recompiling, " "because grammar was not found at: " + grammar_path
        )

    from argparse import ArgumentParser

    parser = ArgumentParser(description="Parses a lcma_standard-file and shows its syntax-tree.")
    parser.add_argument("files", nargs="*" if called_from_app else "+")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const="debug",
        help="Store debug information in LOGS subdirectory",
    )
    parser.add_argument(
        "-o",
        "--out",
        nargs=1,
        default=["out"],
        help="Output directory for batch processing",
    )
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="Verbose output")
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        const="force",
        help="Write output file even if errors have occurred",
    )
    parser.add_argument(
        "--singlethread",
        action="store_const",
        const="singlethread",
        help="Run batch jobs in a single thread (recommended only for debugging)",
    )
    parser.add_argument(
        "--dontrerun",
        action="store_const",
        const="dontrerun",
        help="Do not automatically run again if the grammar has been recompiled.",
    )
    parser.add_argument("-s", "--serialize", nargs="+", default=[])

    args = parser.parse_args()
    file_names, out, log_dir = args.files, args.out[0], ""

    # from DHParser.configuration import read_local_config
    # read_local_config(os.path.join(scriptdir, 'lcma_standardConfig.ini'))

    if args.serialize:
        serializations["*"] = args.serialize
        access_presets()
        set_preset_value("lcma_standard_serializations", serializations, allow_new_key=True)
        finalize_presets()

    if args.debug is not None:
        log_dir = "LOGS"
        access_presets()
        set_preset_value("history_tracking", True)
        set_preset_value("resume_notices", True)
        set_preset_value("log_syntax_trees", frozenset(["CST", "AST"]))  # don't use a set literal, here!
        finalize_presets()
    start_logging(log_dir)

    if args.singlethread:
        set_config_value("batch_processing_parallelization", False)

    def echo(message: str):
        if args.verbose:
            print(message)

    if called_from_app and not file_names:
        return False

    batch_processing = True
    if len(file_names) == 1:
        if os.path.isdir(file_names[0]):
            dir_name = file_names[0]
            echo("Processing all files in directory: " + dir_name)
            file_names = [
                os.path.join(dir_name, fn) for fn in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, fn))
            ]
        elif not ("-o" in sys.argv or "--out" in sys.argv):
            batch_processing = False

    if batch_processing:
        if not os.path.exists(out):
            os.mkdir(out)
        elif not os.path.isdir(out):
            print('Output directory "%s" exists and is not a directory!' % out)
            sys.exit(1)
        error_files = batch_process(file_names, out, log_func=print if args.verbose else None)
        if error_files:
            category = "ERRORS" if any(f.endswith("_ERRORS.txt") for f in error_files) else "warnings"
            print("There have been %s! Please check files:" % category)
            print("\n".join(error_files))
            if category == "ERRORS":
                sys.exit(1)
    else:
        result, errors = compile_src(file_names[0])

        if not errors or (not has_errors(errors, ERROR)) or (not has_errors(errors, FATAL) and args.force):
            print(result.serialize(serializations["*"][0]) if isinstance(result, Node) else result)
            if errors:
                print("\n---")

        for err_str in canonical_error_strings(errors):
            print(err_str)
        if has_errors(errors, ERROR):
            sys.exit(1)

    return True


if __name__ == "__main__":
    main()
