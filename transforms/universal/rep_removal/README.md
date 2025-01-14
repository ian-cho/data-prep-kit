# Repetition removal

This tranforms performs text repetition removal to remove sequences that frequently occur at documents within a single parquet file level.

The work is adopted from https://github.com/google-research/deduplicate-text-datasets to identify and remove all substrings of a given length that are repeated more than some threshold number of times.

Several enhancements has been made to run at scale at single-parquet file level:

    - run in the same python space

    - avoid resource conflict having two processes handling two different parquet files (in making suffix_array and other steps)

    - cleanup (to prevent data fill up in container environment)

    - avoid I/O processes (file read/write operations)

    - Eliminate encoding and decoding procedures when working with related files

    - Optimize data loading (loading the data once)

    - Optimize data encoding/decoding for saving the generated output
    
    - Save the tokenizer in a local path and load it from local path to speed up the process
    
    - Copy the empty parquet file to target folder without processing
    
these enhancements speed up the task, minimize the disk storage utilization, and improve parallelism on each node.

The original code from https://github.com/google-research/deduplicate-text-datasets removes all copies of the duplicates. 
Another modification has been made to retain the first copy of each duplicate cluster. 

This repetition removal task can be fine-tuned by adjusting the length_threshold(repeated text sequence length) and frequency_threshold. 
Based on the analysis length_threshold=50 is used in the repetition removal task that also was used in the original work from google and in the RefinedWeb.


## Output format

The output format will be a new parquet file with the repeated sequence(s) removed
ex:
```
orig parquet:
0 A staffer sells cars via livestream at a deale... ...           0.012263
1 The May 1st submission deadline may feel like ... ...           0.000067
2 Yes! Cinnamon Oil is a great way to deter mice... ...           0.021643
3 Rosemary Oil can be used to deter cockroaches.... ...           0.005885
4 A cat might have discovered an insect crawling... ...           0.881134
5 A staffer sells cars via livestream at a deale... ...           0.012263
6 The May 1st submission deadline may feel like ... ...           0.000067
7 Yes! Cinnamon Oil is a great way to deter mice... ...           0.021643
8 Rosemary Oil can be used to deter cockroaches.... ...           0.005885
9 A cat might have discovered an insect crawling... ...           0.881134
```

```
dedup output:
0 A staffer sells cars via livestream at a deale... ...           0.012263
1 The May 1st submission deadline may feel like ... ...           0.000067
2 Yes! Cinnamon Oil is a great way to deter mice... ...           0.021643
3 Rosemary Oil can be used to deter cockroaches.... ...           0.005885
4 A cat might have discovered an insect crawling... ...           0.881134
5                           ...           0.012263
6                           ...           0.000067
7                           ...           0.021643
8                           ...           0.005885
9                           ...           0.881134

```


## Parameters

The transform can be initialized with the following parameters.

| Parameter  | Default   | Description  |
|------------|-----------|--------------|
| `contents_column_name`             | `text`    | Name of the column holding the document text |
| `dedup_level_name`         | `parquet` | Name of the type of file to process |
| `length_thresh`         | `50`      | Length threshold for processing |
| `frequency_threshold`         | `1`       | Frequency threshold for processing |
| `retain_first_copy`                     | `True`    | Boolean value for whether to retain first copy |
| `tokenize`           | `True`    | Boolean value for whether to tokenize |
| `num_threads`           | `4`       | Value for number of threads to use for processing |

