import time

SLOW_QUERY_THRESHOLD = 1.0  # seconds

def log_query(query, start_time):
    duration = time.time() - start_time
    if duration > SLOW_QUERY_THRESHOLD:
        print(f"⚠️ SLOW QUERY ({duration:.2f}s): {query}")
    else:
        print(f"✅ QUERY ({duration:.2f}s): {query}")