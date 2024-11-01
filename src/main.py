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
        {
            "output_column_name": "jobid",
            "comparison_levels": [
                cll.ExactMatchLevel("jobid").as_dict(),
                cll.NullLevel("jobid").as_dict(),
                cll.ElseLevel().as_dict()
            ]
        },
        {
            "output_column_name": "clntkey",
            "comparison_levels": [
                cll.ExactMatchLevel("clntkey").as_dict(),
                cll.NullLevel("clntkey").as_dict(),
                cll.ElseLevel().as_dict()
            ]
        },
        {
            "output_column_name": "clntname",
            "comparison_levels": [
                cll.ExactMatchLevel("clntname").as_dict(),
                {
                    "sql_condition": "jaro_winkler_sim(clntname_l, clntname_r) > 0.95",
                    "label_for_charts": "Jaro-Winkler > 0.95"
                },
                {
                    "sql_condition": "jaro_winkler_sim(clntname_l, clntname_r) > 0.85",
                    "label_for_charts": "Jaro-Winkler > 0.85"
                },
                cll.NullLevel("clntname").as_dict(),
                cll.ElseLevel().as_dict()
            ]
        },
        {
            "output_column_name": "clntaccount",
            "comparison_levels": [
                cll.ExactMatchLevel("clntaccount").as_dict(),
                {
                    "sql_condition": "jaro_winkler_sim(clntaccount_l, clntaccount_r) > 0.90",
                    "label_for_charts": "Jaro-Winkler > 0.90"
                },
                cll.NullLevel("clntaccount").as_dict(),
                cll.ElseLevel().as_dict()
            ]
        },
        {
            "output_column_name": "desc_1",
            "comparison_levels": [
                {
                    "sql_condition": "l.desc_1 LIKE '%' || r.clntaccount || '%' OR l.desc_1 LIKE '%' || r.clntname || '%'",
                    "label_for_charts": "In Condition on desc_1"
                },
                cll.NullLevel("desc_1").as_dict(),
                cll.ElseLevel().as_dict()
            ]
        }
    ]
}

linker = Splink(settings, [gl_df, athena_df])
result_df = linker.get_scored_comparisons()
result_df
