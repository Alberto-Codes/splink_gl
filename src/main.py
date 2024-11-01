from splink import Splink
from splink_settings import Settings
import splink.comparison_library as cl
import splink.comparison_level_library as cll

settings = {
    "link_type": "link_only",
    "blocking_rules": [
        "l.jobid = r.jobid OR l.clntkey = r.clntkey"
    ],
    "comparisons": [
        cl.ExactMatch("jobid"),
        cl.ExactMatch("clntkey"),
        cl.JaroWinkler("clntname", threshold=0.85),  # Partial match with threshold 0.85
        cl.JaroWinkler("clntaccount", threshold=0.90),  # Adjust threshold as needed
        {
            "output_column_name": "desc_1",
            "comparison_levels": [
                {
                    "sql_condition": "l.desc_1 LIKE '%' || r.clntaccount || '%' OR l.desc_1 LIKE '%' || r.clntname || '%'",
                    "label_for_charts": "In Condition on desc_1"
                },
                cll.NullLevel("desc_1"),
                cll.ElseLevel()
            ]
        }
    ]
}

linker = Splink(settings, [gl_df, athena_df])
result_df = linker.get_scored_comparisons()
result_df

linker = Splink(settings, [gl_df, athena_df])
result_df = linker.get_scored_comparisons()
result_df
