# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**
142301038


## notify retry count

<!-- How many attempts did notify take in your run? (Check
     dag_run_summary.json.) -->

notify took 3 attempts in my run. Upon inspecting the run_pipeline.py code I saw that there is a simulated error kept in its code which throws an error for number of attempts < 3. This is why it succeeded on 3rd try.

## Branch independence

<!-- Why does load still succeed even though notify — its "sibling" in the
     DAG — failed on its first two attempts? What does that tell you about
     how failures in one branch of a DAG should (or shouldn't) affect an
     unrelated branch? -->
load still succeeds even when notify fails because when you see the run_pipeline code you will notice that both load and notify only depend on score.

Which means load does not depend on notify to run, thus even if notify fails, load can run independently and it will not violate the DAG order.

So failures in one branch should never prevent parallel or sibling branches from executing. Because if that happens, a task may stop another key task which has no dependencies on it, which is unnecessary and breaking the execution when it shouldn't.


## Retry cost under FinOps

<!-- Tying back to this week's FinOps content: if notify were a metered API
     call you paid for per attempt, what would you change about the retry
     strategy, and why is "retry every failed task the same way" a risky
     default once cost enters the picture? -->

One way is to just optimize the number of retries based on the task, but that would be a hardcoded or manual tuning.

As discussed in class, we could otherwise use exponential backoff instead of keeping fixed delays for retrying.

Unspaced, uniform retries hammer struggling or rate-limited APIs, burning money on rapid sequential attempts during outage windows that were never going to recover in fractions of a second anyway.

For example: If the API server is overloaded, hitting it with uniform retries every N seconds keeps the server overloaded and ensures all your retries will fail.

Example 2: if the API server is down, out for 10 seconds, and we keep retrying every 0.1 seconds. In 5 seconds 50 retries would have happened but for exponential back off it will be around 5.

