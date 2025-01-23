from data_processing.utils import get_logger


short_name = "extreme_tokenized"
cli_prefix = short_name + "_"

logger = get_logger(__name__, level="INFO")

# configuration keys
contents_column_name_key = "contents_column_name"
""" Key holds the name of the column holding the document text."""
arrow_path_key = "arrow_path"
""" Key holds the arrow folder location"""

# CLI parameters corresponding to each config key
contents_column_name_cli_param = f"{cli_prefix}{contents_column_name_key}"
""" Name of the column holding the document text"""
arrow_path_cli_param = f"{cli_prefix}{arrow_path_key}"
""" Arrow folder location"""

captured_arg_keys = [
    contents_column_name_key,
    arrow_path_key,
]
""" The set of keys captured from the command line """

# defaults
contents_column_name_default = "text"
""" The default name of the column holding the document text. Default is `text`."""
arrow_path_default = None
""" The default location of the arrow folder."""

# data access configuration
extreme_tokenized_data_factory_key = f"{short_name}_data_factory"
extreme_tokenized_data_access_key = "data_access"
