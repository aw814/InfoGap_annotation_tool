import polars as pl
import loguru
from tqdm import tqdm
import os
from typing import List, Callable, Any
import polars as pl

logger = loguru.logger


TARGET_LANG = "Bangla"
# Some packages you may need to pip install:
# - polars
# - loguru

# Instructions:
## You're going to be answering questions about whether a fact is present in a Wikipedia article.
## The two languages you'll be considering are English and Korean.
## For each fact, you'll be given the fact in one language (e.g., English)
##   and potentially relevant snippets from the Wikipedia article in the other language (e.g., Korean).
## If the English fact is conveyed by the Korean snippets, answer 'A'.
## If it is mostly conveyed by the Korean snippets, answer 'B'.
## If not, then open up the Korean Wikipedia article and see if the fact is present there. Then there are three possibilities:
    ## If the fact is present in the article, answer 'C'.
    ## If it is mostly (but not completely) present in the article, answer 'D'.
    ## If the fact is not present in the article, answer 'E'.
## It is up to your discretion to decide whether a fact is "mostly" present in the snippets or the article.

ANNOTATION_FNAME = "annotation_2025-02-18_Dosa (food).json" # TODO: set to whatever directory you want to save the annotations to
frame = pl.read_json(ANNOTATION_FNAME)
en_link = "https://en.wikipedia.org/wiki/Dosa_(food)"
tgt_link = "https://bn.wikipedia.org/wiki/%E0%A6%A7%E0%A7%8B%E0%A6%B8%E0%A6%BE"


def get_candidate_annotations(frame, annotation_column_names) -> pl.DataFrame: # TODO: need to test this
    return frame.filter(
        pl.any_horizontal(pl.col(name) == 'tbd' for name in annotation_column_names)
    )


def update_annotations(original_frame: pl.DataFrame, annotated_subset_frame: pl.DataFrame):
    # 1. convert the tbds in original frame to nulls
    # 2. update original frame with the annotated subset frame, joining on the 'index' column

    # original_frame = original_frame.with_columns([
    #     pl.when(pl.col('annotation_col_1') == 'tbd').then(None).otherwise(pl.col('annotation_col_1')).keep_name(),
    #     pl.when(pl.col('annotation_col_2') == 'tbd').then(None).otherwise(pl.col('annotation_col_2')).keep_name()
    # ])

    # iterate through the columns of annotated subset frame, excluding the index column
    # cast 'index' column of both to f32.
    original_frame = original_frame.with_columns([
        pl.col('index').cast(pl.Float32)
    ])
    annotated_subset_frame = annotated_subset_frame.with_columns([
        pl.col('index').cast(pl.Float32)
    ])
    original_frame = original_frame.with_columns([
        pl.when(pl.col(name) == 'tbd').then(None).otherwise(pl.col(name)).keep_name()
        for name in annotated_subset_frame.columns if name != 'index'
    ])
    result_frame = original_frame.update(annotated_subset_frame, on='index')
    # assert that there are no None values in the result frame
    return result_frame


def load_save_if_nexists(df: pl.DataFrame, path: str):
        # save the en_intersection_contexts and fr_intersection_contexts as a string by joining with a newline
        if (not os.path.exists(path)):
            df.write_json(path)
        else:
            # df = pl.read_csv(path)
            # ask the user if we should overwrite the file
            overwrite = input(f"File {path} already exists. Overwrite? (y/n): ")
            if overwrite == 'y':
                # ask the user if they are sure
                overwrite = input(f"Are you sure you want to overwrite {path}? (y/n): ")
                if overwrite == 'y':
                    df.write_json(path)
            else:
                df = pl.read_json(path)
        return df

def annotate_frame(frame: pl.DataFrame, num_samples, 
    annotation_columns: List[str], question_fns: List[Callable], 
    answer_validate_fn: List[Callable],
    save_path: str,
    input_fn: Callable = input) -> pl.DataFrame:
    """Annotate the frame with the given annotation columns and save intermediate results."""
    
    # Ensure annotation columns exist
    for annotation_column in annotation_columns:
        if annotation_column not in frame.columns:
            frame = frame.with_columns([
                pl.Series(['tbd' for _ in range(len(frame))]).alias(annotation_column)
            ])
    
    # Add an index column if not already present
    if 'index' not in frame.columns:
        frame = frame.with_columns([
            pl.Series(list(range(len(frame)))).alias('index')
        ])

    subset_frame = get_candidate_annotations(frame, annotation_columns)
    if len(subset_frame) == 0:
        logger.info("No more samples to annotate in this dataframe")
        return frame.drop('index') 

    logger.info(f"Number of samples that are unannotated: {len(subset_frame)}")
    pbar = tqdm(total=min(num_samples, len(subset_frame)))

    subset_annotation_map = {
        'index': subset_frame['index'].to_list()
    }

    for annotation_column in annotation_columns:
        subset_annotation_map[annotation_column] = subset_frame[annotation_column].to_list()

    num_annotated = 0
    try:
        for i, index in enumerate(subset_annotation_map['index']):
            row = frame.filter(pl.col('index') == index).to_dicts()[0]
            questions = [question_fn(row) for question_fn in question_fns]
            answers = [input_fn(question) for question in questions]

            for answer, validate_fn, annotation_column, question in zip(answers, answer_validate_fn, annotation_columns, questions):
                if validate_fn(answer):
                    subset_annotation_map[annotation_column][i] = answer
                else:
                    while not validate_fn(answer):
                        answer = input(f"Invalid answer. {question}")
                    subset_annotation_map[annotation_column][i] = answer

            num_annotated += 1
            pbar.update(1)

            # Save progress after each annotation
            subset_frame = pl.DataFrame(subset_annotation_map)
            result_frame = update_annotations(frame, subset_frame)
            result_frame.drop('index').write_json(save_path)

            if num_annotated >= num_samples:
                break

    except KeyboardInterrupt:
        print("\nAnnotation interrupted. Saving progress before exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure progress is saved even if an error occurs
        subset_frame = pl.DataFrame(subset_annotation_map)
        result_frame = update_annotations(frame, subset_frame)
        result_frame.drop('index').write_json(save_path)
        logger.info(f"Progress saved to {save_path}")

    return result_frame.drop('index')


def ask_question(fact_row):
    src_lang = fact_row['language']
    # TODO: adjust this so that the context is a string.
    # convert to List[str] by making every inner list a string by enumerating its contents

    candidate_tgt_contexts = fact_row['tgt_contexts'] # List[List[str]]
    # candidate_tgt_contexts_translations = fact_row['tgt_contexts_en_translation']
    tgt_contexts_lst = [] # List[str]
    for i in range(len(candidate_tgt_contexts)):
        tgt_context = candidate_tgt_contexts[i]
        # tgt_context_translated = candidate_tgt_contexts_translations[i]
        # if src_lang == 'en':
        #     tgt_contexts_str = ''.join([f"{j+1}. {fact} ({tgt_context_translated[j]})\n" for j, fact in enumerate(tgt_context)]) 
        # else:
        tgt_contexts_str = ''.join([f"{j+1}. {fact}\n" for j, fact in enumerate(tgt_context)])
        tgt_contexts_lst.append(tgt_contexts_str)
    tgt_contexts_complete = '\n'.join(tgt_contexts_lst)
    tgt_lang = TARGET_LANG if fact_row['language'] == 'en' else 'English'

    # context_translated = fact_row['src_contexts_en_translation']
    context_str = fact_row['src_context']
    # if src_lang == 'fr':
    #     context_str = ''.join([f"{i+1}. {fact} ({context_translated[i]})\n" for i, fact in enumerate(context_str)])
    # else:
    context_str = ''.join([f"{i+1}. {fact}\n" for i, fact in enumerate(context_str)])

    link = en_link if src_lang == TARGET_LANG else tgt_link
    # question = f"\n\nConsider the following fact(s) about {fact_row['person_name']}:\n\n{context_str}\n\nIs the final fact present in the {tgt_lang} Wikipedia article about {fact_row['person_name']})?\n\nHere are some snippets from the {tgt_lang} article:\n{tgt_contexts_complete}\n\n"
    question = f"\n\nConsider the following fact(s) about {fact_row['person_name']}:\n\n{context_str}\n\nIs the final fact present in the {tgt_lang} Wikipedia article about {fact_row['person_name']} ({link})?\n\nHere are some snippets from the {tgt_lang} article:\n{tgt_contexts_complete}\n\n"
    
    response_options = "\n".join(["A: covered by the snippets", "B: partly covered by the snippets", "C: covered by the article", "D: partly covered by the article", "E: Not in the article"])
    full_prompt = question + response_options + "\nAnswer (A/B/C/D/E): "
    return full_prompt
annotated_frame = annotate_frame(
    frame, # frame containing data to annotate 
    num_samples=30, # number of samples to annotate in one setting
    annotation_columns=['sam_annotations'], # column to store the annotation in
    question_fns=[ask_question],
    answer_validate_fn=[lambda answer: answer in ['A', 'B', 'C', 'D', 'E']],
    save_path=ANNOTATION_FNAME
)