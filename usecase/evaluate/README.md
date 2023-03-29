## Context:

```
in_transaction_subprocess:
[
    "${transaction_subprocess_id}"
]

# transaction_subprocess_id will be removed when it is inactive
```

```
number_of_cancel_events:
{
    "${transaction_subprocess_id}": {
        "end_event": ${number of cancel end event},
        "boundary_event": ${number of cancel boundary event}
    }
}
```

```
list_event_subprocess:
{
	"${code}": ${total_cycletime}
}

# code: code of send or receive message
# total_cycletime: total cycle time from sent message to received message
```

```
list_boundary_event:
{
	"${subprocess_id}": {
		"${code}": ${total_cycletime}
	}
}

# subprocess_id: subprocess' id
# code: code of send or receive event
# total_cycletime: total cycle time of boudary event
```

## Element:

```
id: id of element
name: name of element
incoming: activities toward element by sequence flow
outgoing: element forwards activities by sequence flow
incoming_messageflow: activities toward element by message flow
outgoing_messageflow: element forwards activities by message flow
type: type of element
className: className in design of element
linkCode: str
cycleTime: cycle time of element
timeDuration: cycle time of timer event
branchingProbabilities: list
taskType: int
eventType: int
isInterrupting: bool
parentId: str
boundary: list
percentage: int
isStart: bool
code: str
```

## Result:

``` 
participant_name: str
current_cycle_time: float
number_of_optional_tasks: int
number_of_total_tasks: int
flexibility: float
total_cycle_time_all_loops: float
logs_cycle_time: list
logs_quality: list
logs_flexibility: list
number_of_handled_exceptions: int
number_of_unhandled_exceptions: int
exception_handling: float
```