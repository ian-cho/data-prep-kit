# Readability Scores

This transform annotates documents of a parquet file with various Readability Scores that can later be used in Quality Filtering. 

    Parameters:
        input: The input parquet file
        contents_column_name: The column contains the text content
        Curriculum: This parameter is set to True when the data is prepared for curriculum learning and is annotated with flesch_kincaid, gunning_fog, automated_readability_index readability scores, and the average of these 3 grade-level scores to speed up the annotation process. 
        output: a new parquet file containing all documents annotated with various readability scores

textstat Readability Scores

    flesch_ease_textstat
        ######### Score	                School level (US)	    Notes
        ######### 100.00–90.00	        5th grade	            Very easy to read. Easily understood by an average 11-year-old student.
        ######### 90.0–80.0	            6th grade	            Easy to read. Conversational English for consumers.
        ######### 80.0–70.0	            7th grade	            Fairly easy to read.
        ######### 70.0–60.0	            8th & 9th grade	        Plain English. Easily understood by 13- to 15-year-old students.
        ######### 60.0–50.0	            10th to 12th grade	    Fairly difficult to read.
        ######### 50.0–30.0	            College	                Difficult to read.
        ######### 30.0–10.0	            College graduate	    Very difficult to read. Best understood by university graduates.
        ######### 10.0–0.0	            Professional	        Extremely difficult to read. Best understood by university graduates.
        While the maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid.

    flesch_kincaid_textstat
        This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

    gunning_fog_textstat
        This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

    smog_index_textstat
        the SMOG index of the given text. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document. Texts of fewer than 30 sentences are statistically invalid, because the SMOG formula was normed on 30-sentence samples. textstat requires at least 3 sentences for a result.

    coleman_liau_index_textstat
        the grade level of the text using the Coleman-Liau Formula. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

    automated_readability_index_textstat
        the ARI (Automated Readability Index) which outputs a number that approximates the grade level needed to comprehend the text. For example if the ARI is 6.5, then the grade level to comprehend the text is 6th to 7th grade.    

    dale_chall_readability_score_textstat
        Different from other tests, since it uses a lookup table of the most commonly used 3000 English words. Thus it returns the grade level using the New Dale-Chall Formula. Further reading on https://en.wikipedia.org/wiki/Dale–Chall_readability_formula
        ######### Score	            Understood by
        ######### 4.9 or lower	    average 4th-grade student or lower
        ######### 5.0–5.9	        average 5th or 6th-grade student
        ######### 6.0–6.9	        average 7th or 8th-grade student
        ######### 7.0–7.9	        average 9th or 10th-grade student
        ######### 8.0–8.9	        average 11th or 12th-grade student
        ######### 9.0–9.9	        average 13th to 15th-grade (college) student

    linsear_write_formula_textstat
        the grade level using the Linsear Write Formula. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document. Further reading on Wikipedia https://en.wikipedia.org/wiki/Linsear_Write
    
    text_standard_textstat
        Based upon all the above tests, returns the estimated school grade level required to understand the text. Optional float_output allows the score to be returned as a float. Defaults to False.
    
    spache_readability_textstat
        The grade level of english text. Intended for text written for children up to grade four.

    mcalpine_eflaw_textstat
        A score for the readability of an english text for a foreign learner or English, focusing on the number of miniwords and length of sentences. 

    reading_time_textstat
        the reading time of the given text. Assumes 14.69ms per character.
    
    avg_grade_level
        Average of grade-level scores flesch_kincaid, gunning_fog, and automated_readability_index
        
Dependencies:

    textstat 0.7.3
    pandas 2.2.2
    

