def default_before_hook(query, params, stage):
    print(f"[HOOK] {stage.upper()} QUERY: {query} PARAMS: {params}")

def default_after_hook(query, params, stage):
    print(f"[HOOK] {stage.upper()} QUERY COMPLETE")