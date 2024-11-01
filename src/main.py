from splink import Splink
from splink_settings import Settings

settings = {
    "link_type": "link_only",
    "blocking_rules": [
        # Adjust blocking as needed
        "l.jobid = r.jobid OR l.clntkey = r.clntkey"
    ],
    "comparison_columns": [
        {"col_name": "jobid", "comparison_levels": [{"level_type": "exact"}]},
        {"col_name": "clntkey", "comparison_levels": [{"level_type": "exact"}]},
        {
            "col_name": "clntname",
            "comparison_levels": [
                {"level_type": "levenshtein", "threshold": 0.85}  # Adjust threshold as needed
            ]
        },
        {
            "col_name": "clntaccount",
            "comparison_levels": [
                {"level_type": "jaro_winkler", "threshold": 0.80}  # Adjust threshold as needed
            ]
        },
        {
            "col_name": "desc_1",
            "comparison_levels": [
                {"level_type": "in_condition", "columns_to_search": ["clntaccount", "clntname"]}
            ]
        }
    ]
}

linker = Splink(settings, [gl_df, athena_df])
result_df = linker.get_scored_comparisons()

result_df
