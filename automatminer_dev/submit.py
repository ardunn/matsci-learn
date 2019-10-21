from automatminer_dev.config import (
    LP,
    KFOLD_DEFAULT,
    RUN_TESTS_CMD,
    BENCHMARK_DEBUG_SET,
    BENCHMARK_FULL_SET,
)
from automatminer_dev.workflows.bench import wf_evaluate_build, wf_benchmark
from automatminer_dev.workflows.single import wf_single_fit, wf_run_test

"""
Running benchmarks
"""


if __name__ == "__main__":

    pipe_config = {
        "learner_name": "TPOTAdaptor",
        # "learner_kwargs": {"generations": 100, "population_size": 100, "memory": "auto", "n_jobs": 10, "max_eval_time_mins": 5},
        # "learner_kwargs": {"max_time_mins": 1440, "max_eval_time_mins": 20, "population_size": 100, "memory": "auto", "n_jobs": 10},
        "learner_kwargs": {
            "max_time_mins": 1440,
            "max_eval_time_mins": 20,
            "population_size": 200,
            "memory": "auto",
            "n_jobs": 20,
        },
        # "reducer_kwargs": {"reducers": ("corr",)},
        "reducer_kwargs": {
            "reducers": ("corr", "tree"),
            "tree_importance_percentile": 0.99,
        },
        # "reducer_kwargs": {"reducers": ("corr", "tree",), "tree_importance_percentile": 0.85},
        # "reducer_kwargs": {"reducers": ("pca",), "n_pca_features": 0.3},
        # "reducer_kwargs": {"reducers": ("rebate",), "n_rebate_features": 0.3},
        # "reducer_kwargs": {"reducers": ()},
        "autofeaturizer_kwargs": {"preset": "express", "n_jobs": 20},
        # "autofeaturizer_kwargs": {"preset": "heavy", "n_jobs": 20},
        # "cleaner_kwargs": {"max_na_frac": 0.01, "feature_na_method": "mean", "na_method_fit": "drop", "na_method_transform": "mean"},
        "cleaner_kwargs": {
            "max_na_frac": 0.1,
            "feature_na_method": "drop",
            "na_method_fit": "mean",
            "na_method_transform": "mean",
        },
    }

    pipe_config_debug = {
        "autofeaturizer_kwargs": {"preset": "debug", "n_jobs": 10},
        "reducer_kwargs": {"reducers": ()},
        "learner_name": "rf",
        "learner_kwargs": {"n_estimators": 500},
        "cleaner_kwargs": {
            "max_na_frac": 0.01,
            "feature_na_method": "mean",
            "na_method_fit": "drop",
            "na_method_transform": "mean",
        },
    }

    tags = [
        # "data_full",
        # "drop_mean",
        # "af_best",
        # "af_debug",
        # "rf",
        # "debug",
        # "no_reduction"
        # "tpot_limited_mem"
        # "corr_only",
        # "drop_mean",
        # "af_fast",
        # "tpot_generations",
        "debug"
    ]

    # from automatminer_dev.config import MP_E_FORM, JDFT2D, GLASS
    # wf = wf_benchmark("lrc", pipe_config, **GFA, cache=True, tags=tags)

    wf = wf_evaluate_build(
        "lrc",
        "24 hr tpot production 99% reducing with mean drop cleaning samples",
        BENCHMARK_FULL_SET,
        pipe_config,
        include_tests=False,
        cache=True,
        tags=tags,
    )

    # wf = wf_run_test("lrc", )

    # wf = wf_evaluate_build("local", "test_local", BENCHMARK_DEBUG_SET, pipe_config_debug)

    # wf = wf_evaluate_build("cori", "rf run for comparison to the paper", BENCHMARK_FULL_SET,
    #                        pipe_config_debug, include_tests=False, cache=True, tags=tags)

    # LP.reset(password=None, require_password=False)
    LP.add_wf(wf)