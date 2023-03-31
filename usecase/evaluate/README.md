## Context:

```
in_subprocess:
[
    "${subprocess_id}"
]

# in_subprocess is list of present subprocess (descending level)
# subprocess_id will be removed when it is inactive
```

```
number_of_exception_events:
{
    "${transaction_subprocess_id}": {
        "end_event": ${number of cancel end event},
        "catching_event": ${number of cancel catching event}
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
		"${code}": (${total_cycletime}, ${is_interupting})
	}
}

# subprocess_id: subprocess' id
# code: code of send or receive event
# total_cycletime: total cycle time of boudary event
# is_interupting: type of boundary event
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