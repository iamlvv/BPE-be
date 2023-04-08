from evaluation.views.utils import *


class EvaluateView:
    @staticmethod
    @api_view(['POST'])
    def evaluate(request, format=None):
        body = load_request_body(request)
        result = Evaluate.evaluate(body)
        json_response = [r.__dict__ for r in result]
        return JsonResponse(json_response, safe=False)

    @staticmethod
    @api_view(['POST'])
    def compare(request, format=None):
        body = load_request_body(request)
        result = Compare.compare(body)
        json_response = result.__dict__
        return JsonResponse(json_response, safe=False)

    @staticmethod
    @api_view(['GET'])
    def evaluate1(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 110.425,
                "totalCost": 8.834,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": {
                    "1": {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.308,
                    },
                    "2": {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.308,
                    },
                    "3": {
                        "view": "Customer View",
                        "numberOfExplicitTask": 5,
                        "transparency": 0.384,
                    },
                },
                "totalNumberExplicitTasks": 13,
                "quality": 0.76,
                "numberOfOptionalTasks": 3,
                "totalTasks": 13,
                "flexibility": 0.2307,
                "steps": [
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_1gwq4rz",
                        "rework": 0.7,
                    },
                    {
                        "activity": "Activity_18vspx4",
                        "cycleTime": 30,
                        "cost": 2.4,
                        "label": "Search flights"
                    },
                    {
                        "event": "End Loop",
                        "endGateway": "Gateway_1v8mhbs",
                    },
                    {
                        "activity": "Activity_0qr3vb0",
                        "cycleTime": 0.5,
                        "cost": 2.4,
                        "label": "Check ticket status"
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_1i9ffc9",
                        "branchingProbability": [0.2, 0.8]
                    },
                    {
                        "activity": "Activity_0qnumaw",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Notify customer"
                    },
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_0o2luuy",
                        "rework": 0.01,
                    },
                    {
                        "activity": "Activity_0wd0hnw",
                        "cycleTime": 10,
                        "cost": 0.8,
                        "label": "Submit customer information"
                    },
                    {
                        "event": "End loop",
                        "endGateway": "Gateway_1v8mhbs",
                    },
                    {
                        "activity": "Activity_1y0zxmo",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Check eWallet balance",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_1v8mhbs",
                        "branchingProbability": [0.01, 0.99]
                    },
                    {
                        "activity": "Activity_108sli3",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Top up eWallet"
                    },
                    {
                        "activity": "Activity_0g90l5p",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Warn customer"
                    },
                    {
                        "activity": "Activity_0qhqqfh",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Create payment instruction",
                    },
                    {
                        "event": "Start parallel gateway",
                        "startGateway": "Gateway_1n3qwia",
                    },
                    {
                        "activity": "Activity_0yh3440",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Update eWallet Information"
                    },
                    {
                        "activity": "Activity_1mhorxu",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Pay the airlines",
                    },
                    {
                        "activity": "Activity_1k4g8sl",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Send the ticket & result of payment"
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_02l0nhx",
                        "branchingProbability": [0.6, 0.4]
                    },
                    {
                        "activity": "Activity_03bj5rr",
                        "cycleTime": 10,
                        "cost": 0.8,
                        "label": "Refund Customer",
                    },
                    {
                        "event": "End exclusive gateway",
                        "endGateway": "Gateway_02l0nhx",
                    }
                ],
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1,
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate2(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 59.225,
                "totalCost": 4.378,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": {
                    "1": {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.333,
                    },
                    "2": {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.25,
                    },
                    "3": {
                        "view": "Customer View",
                        "numberOfExplicitTask": 5,
                        "transparency": 0.417,
                    },
                },
                "totalNumberExplicitTasks": 12,
                "quality": 0.76,
                "numberOfOptionalTasks": 2,
                "totalTasks": 12,
                "flexibility": 0.166,
                "steps": [
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_1gwq4rz",
                        "rework": 0.7,
                    },
                    {
                        "activity": "Activity_18vspx4",
                        "cycleTime": 30,
                        "cost": 2.4,
                        "label": "Search flights"
                    },
                    {
                        "event": "End Loop",
                        "endGateway": "Gateway_1v8mhbs",
                    },
                    {
                        "activity": "Activity_0qr3vb0",
                        "cycleTime": 0.5,
                        "cost": 2.4,
                        "label": "Check ticket status"
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_1i9ffc9",
                        "branchingProbability": [0.2, 0.8]
                    },
                    {
                        "activity": "Activity_0qnumaw",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Notify customer"
                    },
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_0o2luuy",
                        "rework": 0.01,
                    },
                    {
                        "activity": "Activity_0wd0hnw",
                        "cycleTime": 10,
                        "cost": 0.8,
                        "label": "Submit customer information"
                    },
                    {
                        "event": "End loop",
                        "endGateway": "Gateway_1v8mhbs",
                    },
                    {
                        "activity": "Activity_1y0zxmo",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Check eWallet balance",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_1v8mhbs",
                        "branchingProbability": [0.01, 0.99]
                    },
                    {
                        "activity": "Activity_108sli3",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Top up eWallet"
                    },
                    {
                        "activity": "Activity_0g90l5p",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Warn customer"
                    },
                    {
                        "activity": "Activity_0qhqqfh",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Create payment instruction",
                    },
                    {
                        "event": "Start parallel gateway",
                        "startGateway": "Gateway_1n3qwia",
                    },
                    {
                        "activity": "Activity_0yh3440",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Update eWallet Information"
                    },
                    {
                        "activity": "Activity_1mhorxu",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Pay the airlines",
                    },
                    {
                        "activity": "Activity_1k4g8sl",
                        "cycleTime": 5,
                        "cost": 0.4,
                        "label": "Send the ticket & result of payment"
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_02l0nhx",
                        "branchingProbability": [0.6, 0.4]
                    },
                    {
                        "activity": "Activity_03bj5rr",
                        "cycleTime": 10,
                        "cost": 0.8,
                        "label": "Refund Customer",
                    },
                    {
                        "event": "End exclusive gateway",
                        "endGateway": "Gateway_02l0nhx",
                    }
                ],
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate3(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 73.9,
                "totalCost": 5.921,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": {
                    "1": {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.4,
                    },
                    "2": {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.3,
                    },
                    "3": {
                        "view": "Customer View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.3,
                    },


                },
                "totalNumberExplicitTasks": 10,
                "quality": 0.2,
                "numberOfOptionalTasks": 8,
                "totalTasks": 10,
                "flexibility": 0.8,
                "step": [
                    {
                        "activity": "Activity_1v63p18",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Send a rescheduling request",
                    },
                    {
                        "activity": "Activity_1vgwzei",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Check rescheduling condition",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_0doview",
                        "branchingProbability": [0.3, 0.7]
                    },
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_0o2luuy",
                        "rework": 0.8,
                    },
                    {
                        "activity": "Activity_0h07wqh",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make a list of rescheduling option",
                    },
                    {
                        "activity": "Activity_19sixcn",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Pick a rescheduling option or not",
                    },
                    {
                        "event": "End loop",
                        "endGateway": "Gateway_1kpivk4",
                    },
                    {
                        "activity": "Activity_18zy42u",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make a list of rescheduling option",
                    },
                    {
                        "activity": "Activity_0tyj0jj",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make payment",
                    },
                    {
                        "activity": "Activity_0tw0m98",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Pay the airlines",
                    },
                    {
                        "activity": "Activity_1x7n5g3",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Send the result and ticket of payment",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_0doview",
                        "branchingProbability": [0.6, 0.4]
                    },
                    {
                        "activity": "Activity_1jf5diz",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Refund customer",
                    },
                    {
                        "event": "End exclusive gateway",
                        "endGateway": "Gateway_10scsjy",
                    },
                ],
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate4(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 32.5,
                "totalCost": 2.6,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": {
                    "1": {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.445,
                    },
                    "2": {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 2,
                        "transparency": 0.222,
                    },
                    "3": {
                        "view": "Customer View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.333,
                    },
                },
                "totalNumberExplicitTasks": 9,
                "quality": 0.7,
                "numberOfOptionalTasks": 7,
                "totalTasks": 9,
                "flexibility": 0.777,
                "step": [
                    {
                        "activity": "Activity_1v63p18",
                        "cycleTime": 1,
                        "cost": 0.08,
                        "label": "Send a rescheduling request",
                    },
                    {
                        "activity": "Activity_1vgwzei",
                        "cycleTime": 0.5,
                        "cost": 0.04,
                        "label": "Check rescheduling condition",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_0doview",
                        "branchingProbability": [0.3, 0.7]
                    },
                    {
                        "event": "Start loop",
                        "startGateway": "Gateway_0o2luuy",
                        "rework": 0.8,
                    },
                    {
                        "activity": "Activity_0h07wqh",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make a list of rescheduling option",
                    },
                    {
                        "activity": "Activity_19sixcn",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Pick a rescheduling option or not",
                    },
                    {
                        "event": "End loop",
                        "endGateway": "Gateway_1kpivk4",
                    },
                    {
                        "activity": "Activity_18zy42u",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make a list of rescheduling option",
                    },
                    {
                        "activity": "Activity_0tyj0jj",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Make payment",
                    },
                    {
                        "activity": "Activity_0tw0m98",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Pay the airlines",
                    },


                    {
                        "activity": "Activity_1x7n5g3",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Send the result and ticket of payment",
                    },
                    {
                        "event": "Start exclusive gateway",
                        "startGateway": "Gateway_0doview",
                        "branchingProbability": [0.6, 0.4]
                    },


                    {
                        "activity": "Activity_1jf5diz",
                        "cycleTime": 5,
                        "cost": 0.04,
                        "label": "Refund customer",
                    },
                    {
                        "event": "End exclusive gateway",
                        "endGateway": "Gateway_10scsjy",
                    },
                ],


                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }

        ]

        return JsonResponse(result, safe=False)
