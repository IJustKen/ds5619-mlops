# README

A lightweight Python task orchestration engine designed to evaluate dependency graphs, execute tasks in valid topological order with automatic retries, and isolate failure branches.

## Overview

This lab implements a mini workflow orchestrator inspired by systems like Apache Airflow. It parses task dependencies, executes them in a valid execution order, handles failures with retries, and passes a shared context dictionary between upstream and downstream tasks.

## Code

Three key functions:

### 1. topological_order(tasks: Dict[str, Task]) -> List[str]
Computes a valid execution sequence for all tasks in the DAG such that every task runs only after its dependencies have completed successfully.

Kahn's Algorithm was used for this purpose.

Map out every task's in-degree (the number of dependencies it must wait for) and builds an adjacency list mapping upstream tasks to their downstream dependents.

Checks if any task depends on a task name that does not exist in tasks and raises an error.

Initializes a queue (zero_queue) with all tasks having an in-degree of 0 (tasks with no pending dependencies). Which means they are free to run at that time step.

Sequentially pop tasks from the queue, append them to the result list, and decrement the in-degrees of their downstream dependents. 
If a dependent's in-degree reaches 0, it is pushed onto the queue.

If there is still some node left with a non zero in-degree after going through all the nodes, it means a cycle is present.  

### 2. run_task_with_retry(task: Task, context: dict) -> int
Executes a single Task function with retry behavior and delays.

If an exception is caught:
If the current attempt is the final attempt (attempt == total_runs), it re-raises the exception without swallowing it.

Otherwise, it pauses execution for task.retry_delay_seconds using time.sleep() before trying again. 

### 3. run_dag(tasks: Dict[str, Task], context: dict) -> dict
Orchestrates the end-to-end execution of the entire pipeline.

Get the topological order of the tasks

Iterate through the names in that order

Pass the context dictionary common to all tasks into the function for each task

Do the above using run_task_with_retry()

Upon success record status and attempts, upon failure record status, attempts and the error message

return the task execution order and the task results recorded