import argparse
from helpers import parse_output
from llm_utils.dpk.langchain_tools.tools.language.pdf2parquet import (
    Pdf2parquetTransform,
)
from llm_utils.dpk.langchain_tools.tools.universal.ededup import EdedupTransform
from llm_utils.dpk.langchain_tools.tools.language.doc_quality import DocQualityTransform
from llm_utils.dpk.langchain_tools.tools.universal.filter import FilterTransform


def execute_workflow(args):
    results = {}
    res = Pdf2parquetTransform()._run(
        input_folder=args.in_folder,
        output_folder=args.out_folder,
        data_files_to_use=args.data_files_to_use,
    )
    results["#E1"] = parse_output(res)
    res = EdedupTransform()._run(
        input_folder=results["#E1"], output_folder=results["#E1"]
    )
    results["#E2"] = parse_output(res)
    res = DocQualityTransform()._run(
        input_folder=results["#E2"],
        output_folder=results["#E2"],
        docq_bad_word_filepath=args.docq_bad_word_filepath,
    )
    results["#E3"] = parse_output(res)
    res = FilterTransform()._run(
        input_folder=results["#E3"],
        output_folder=results["#E3"],
        filter_criteria_list=args.filter_criteria_list,
    )
    results["#E4"] = parse_output(res)
    return results


def main():
    parser = argparse.ArgumentParser(description="Execute the workflow plan.")
    parser.add_argument(
        "--in_folder",
        type=str,
        required=True,
        help="Input folder for the workflow.",
    )
    parser.add_argument(
        "--out_folder",
        type=str,
        required=True,
        help="Output folder for the workflow.",
    )
    parser.add_argument(
        "--data_files_to_use",
        type=str,
        required=True,
        default="['pdf']",
        help="Data files to use for the workflow.",
    )
    parser.add_argument(
        "--docq_bad_word_filepath",
        type=str,
        required=True,
        default="bad_words.txt",
        help="Bad word filepath for the workflow.",
    )
    parser.add_argument(
        "--filter_criteria_list",
        type=str,
        required=True,
        default="[docq_bad_word_count==0]",
        help="Filter query for the workflow.",
    )

    args = parser.parse_args()

    try:
        results = execute_workflow(args)
        print(results)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
